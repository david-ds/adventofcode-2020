package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

type Conditions [][2]int

func (c Conditions) Len() int           { return len(c) }
func (c Conditions) Swap(i, j int)      { c[i], c[j] = c[j], c[i] }
func (c Conditions) Less(i, j int) bool { return c[i][1]-c[i][0] > c[j][1]-c[j][0] }

type SolutionsByIndex [][]int

func (c SolutionsByIndex) Len() int           { return len(c) }
func (c SolutionsByIndex) Swap(i, j int)      { c[i], c[j] = c[j], c[i] }
func (c SolutionsByIndex) Less(i, j int) bool { return len(c[i]) < len(c[j]) }

// Extracted from part 1
func getInvalidTickets(categories []string) []bool {
	// Suppose that a simple check against all conditions is enough, whatever their field
	conditions := make(Conditions, 0, 2*len(categories[0]))
	for _, line := range strings.Split(categories[0], "\n") {
		restrictions := strings.Split(line, ": ")[1]
		for _, restriction := range strings.Split(restrictions, " or ") {
			minMax := strings.Split(restriction, "-")
			min, _ := strconv.Atoi(minMax[0])
			max, _ := strconv.Atoi(minMax[1])
			conditions = append(conditions, [2]int{min, max})
		}
	}

	// Sort for efficiency
	sort.Sort(conditions)

	nearbyTickets := strings.Split(categories[2], "\n")[1:]
	invalidTickets := make([]bool, len(nearbyTickets))
	for i, nearbyTicket := range nearbyTickets {
		for _, value := range strings.Split(nearbyTicket, ",") {
			v, _ := strconv.Atoi(value)
			valueValid := false
			for _, condition := range conditions {
				if v >= condition[0] && v <= condition[1] {
					valueValid = true
					break
				}
			}
			if !valueValid {
				invalidTickets[i] = true
			}
		}
	}

	return invalidTickets
}

func run(s string) interface{} {
	categories := strings.Split(s, "\n\n")

	fieldsWithConditions := strings.Split(categories[0], "\n")
	nearbyTickets := strings.Split(categories[2], "\n")[1:]

	myTicketValues := strings.Split(strings.Split(categories[1], "\n")[1], ",")

	tickets := make([][]int, len(nearbyTickets))
	for i, nearbyTicket := range nearbyTickets {
		tickets[i] = make([]int, len(fieldsWithConditions))
		for j, value := range strings.Split(nearbyTicket, ",") {
			v, _ := strconv.Atoi(value)
			tickets[i][j] = v
		}
	}

	possibleIndexesByCondition := make(SolutionsByIndex, len(fieldsWithConditions))
	departureFields := []int{}
	invalidTickets := getInvalidTickets(categories) // Used to exclude invalid tickets

	for fieldIndex, line := range fieldsWithConditions {
		possibleIndexesByCondition[fieldIndex] = []int{fieldIndex}
		fieldWithConditions := strings.Split(line, ": ")
		if strings.HasPrefix(fieldWithConditions[0], "departure") {
			departureFields = append(departureFields, fieldIndex)
		}

		conditions := strings.Split(fieldWithConditions[1], " or ")
		ranges := make([][2]int, len(conditions))

		for i, restriction := range conditions {
			minMax := strings.Split(restriction, "-")
			min, _ := strconv.Atoi(minMax[0])
			max, _ := strconv.Atoi(minMax[1])
			ranges[i] = [2]int{min, max}
		}

		for i := 0; i < len(myTicketValues); i++ {
			allTicketsValid := true
			for j, ticket := range tickets {
				if invalidTickets[j] {
					continue
				}

				ticketValid := false
				for _, condition := range ranges {
					if condition[0] <= ticket[i] && ticket[i] <= condition[1] {
						ticketValid = true
						break
					}
				}

				if !ticketValid {
					allTicketsValid = false
					break
				}
			}

			if allTicketsValid {
				possibleIndexesByCondition[fieldIndex] = append(possibleIndexesByCondition[fieldIndex], i)
			}
		}
	}

	// Sort by length (shorter, so most restrictive, first)
	sort.Sort(possibleIndexesByCondition)

	// Use possible combinations to find out which field matches which column
	numberIndexToConditionIndex := make([]int, len(possibleIndexesByCondition))
	for i := range numberIndexToConditionIndex {
		numberIndexToConditionIndex[i] = -1
	}

	for _, possibleIndexes := range possibleIndexesByCondition {
		fieldIndex := possibleIndexes[0]
		for _, possibleIndex := range possibleIndexes[1:] {
			notAssigned := true
			for _, indexed := range numberIndexToConditionIndex {
				if indexed == possibleIndex {
					notAssigned = false
					break
				}
			}
			if notAssigned {
				numberIndexToConditionIndex[fieldIndex] = possibleIndex
			}
		}
	}

	// Multiply "departure" values from our own ticket
	result := 1
	for _, fieldIndex := range departureFields {
		index := numberIndexToConditionIndex[fieldIndex]
		v, _ := strconv.Atoi(myTicketValues[index])
		result *= v
	}

	return result
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// Read input from stdin
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
