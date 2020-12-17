package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"sort"
	"strconv"
	"strings"
	"time"
)

type Conditions [][2]int

func (c Conditions) Len() int           { return len(c) }
func (c Conditions) Swap(i, j int)      { c[i], c[j] = c[j], c[i] }
func (c Conditions) Less(i, j int) bool { return c[i][1]-c[i][0] > c[j][1]-c[j][0] }

func run(s string) interface{} {
	categories := strings.Split(s, "\n\n")

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

	scanningErrorRate := 0
	nearbyTickets := strings.Split(categories[2], "\n")[1:]
	for _, nearbyTicket := range nearbyTickets {
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
				scanningErrorRate += v
			}
		}
	}

	return scanningErrorRate
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
