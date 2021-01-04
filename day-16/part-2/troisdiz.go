package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type RuleBounds struct {
	low int
	high int
}

func (rb *RuleBounds) validate(value int) bool {
	return rb.low <= value && value <= rb.high
}

type TicketRule struct {
	name string
	ruleBounds []RuleBounds
}

func (tr *TicketRule) validate(value int) bool {

	for _, rb := range tr.ruleBounds {
		if rb.validate(value) {
			return true
		}
	}
	return false
}

func parseTicketRules(input string) TicketRule {
	parts := strings.Split(input, ": ")
	name := parts[0]
	result := TicketRule{
		name: name,
	}
	rules := strings.Split(parts[1], " or ")
	for _, rule := range rules {
		elems := strings.Split(rule, "-")
		low, _ := strconv.Atoi(elems[0])
		high, _ := strconv.Atoi(elems[1])
		result.ruleBounds = append(result.ruleBounds, RuleBounds{ low: low, high: high })
	}
	return result
}

type Ticket struct {
	numbers []int
}
func (t *Ticket) validateRuleForCol(tr *TicketRule, col int) bool{
	return tr.validate(t.numbers[col])
}

func (t *Ticket) validateRules(trs *[]TicketRule) (bool, int){
	sum := 0
	var validatesAll bool = true
	for _, number := range t.numbers {
		validates := false
		for _, tr := range *trs {
			if tr.validate(number) {
				validates = true
				break
			}
		}
		if !validates {
			sum += number
			//fmt.Printf("%d not ok\n", number)
			validatesAll = false
		}
	}
	return validatesAll, sum
}

func (t *Ticket) size() int {
	return len(t.numbers)
}

func parseTicket(input string) Ticket {
	var result Ticket = Ticket{}
	for _, itemStr := range strings.Split(input, ",") {
		item, _ := strconv.Atoi(itemStr)
		result.numbers = append(result.numbers, item)
	}
	return result
}

func run(s string) interface{} {
	// Your code goes here
	parts := strings.Split(s, "\n\nyour ticket:\n")
	fieldsStr := parts[0]

	parts = strings.Split(parts[1], "\n\nnearby tickets:\n")
	yourTicketStr := parts[0]
	nearbyTicketsStr := parts[1]

	var ticketRules []TicketRule
	var ticketRulesByName map[string]*TicketRule = map[string]*TicketRule{}
	for _, fieldStr := range strings.Split(fieldsStr, "\n") {
		tr := parseTicketRules(fieldStr)
		ticketRules = append(ticketRules, tr)
		ticketRulesByName[tr.name] = &tr
	}
	yourTicket := parseTicket(yourTicketStr)

	var nearbyTickets []Ticket
	for _, line := range strings.Split(nearbyTicketsStr, "\n") {
		if len(line) > 1 {
			nearbyTickets = append(nearbyTickets, parseTicket(line))
		}
	}

	//fmt.Printf("Ticket rules : %v\n", ticketRules)
	//fmt.Printf("Nearby tickets : %v\n", nearbyTickets)

	var okTickets []Ticket
	for _, ticket := range nearbyTickets {
		ok, _ := ticket.validateRules(&ticketRules)
		if ok {
			okTickets = append(okTickets, ticket)
		}
	}

	//fmt.Printf("Rules : %d / Nearby tickets : %d / OK tickets : %d\n", len(ticketRules), len(nearbyTickets), len(okTickets))

	// rule => possible tickets
	var possibleMappings []map[string]int = make([]map[string]int, yourTicket.size())

	for i := 0; i < len(possibleMappings); i++ {
		possibleMappings[i] = map[string]int{}
		for x := range ticketRulesByName {
			possibleMappings[i][x] = 0
		}
	}
	// var responsibleTickets = map[int][]int{}
	for _, ticket := range okTickets {
		// fmt.Printf("Tickets(%d) : %v\n", ticketIdx, ticket)
		for idx, possibleMapping := range possibleMappings {
			for name := range possibleMapping {
				if !ticket.validateRuleForCol(ticketRulesByName[name], idx) {
					//fmt.Printf("    Delete %v for pos %d\n", name, idx)
					delete(possibleMappings[idx], name)
					// responsibleTickets[idx] = append(responsibleTickets[idx], ticketIdx)
				}
			}
		}
	}
	/*
	for idx := range responsibleTickets {
		fmt.Printf("Position %-4d = %v\n", idx, responsibleTickets[idx])
	}
	for idx, posMap := range possibleMappings {
		fmt.Printf("%d => %v\n", idx, posMap)
	}
	*/
	posOneCount := 0
	for posOneCount < len(ticketRules) {
		// fmt.Printf("Loop (posCount = %d)\n", posOneCount)
		for i := 0; i < yourTicket.size(); i++ {
			if len(possibleMappings[i]) == 1 {
				var nameToDelete string
				for key := range possibleMappings[i] {
					nameToDelete = key
				}
				if v, _ := possibleMappings[i][nameToDelete]; v == 0 {
					possibleMappings[i][nameToDelete] = 1
					// fmt.Printf("    Delete %20v (single at %2d) in other posMaps\n", nameToDelete, i)
					posOneCount += 1
					for j := 0; j < yourTicket.size(); j++ {
						if j != i {
							delete(possibleMappings[j], nameToDelete)
						}
					}
				}
			}
		}
		/*
		for idx, posMap := range possibleMappings {
			fmt.Printf("%d => %v\n", idx, posMap)
		}
		fmt.Println()
		*/
	}
	/*

	 */
	product := 1
	for i := 0; i < yourTicket.size(); i++ {
		var name string
		for key := range possibleMappings[i] {
			name = key
		}
		if strings.HasPrefix(name, "departure") {
			//fmt.Printf("YourTicket : %d => %d\n", i, yourTicket.numbers[i])
			product *= yourTicket.numbers[i]
		}
	}

	return product
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	argsWithProg := os.Args
	var input []byte
	var err error
	if len(argsWithProg) > 1 {
		input,err = ioutil.ReadFile(argsWithProg[1])
		if err != nil {
			panic(err)
		}
	} else {
		// Read input from stdin
		input, err = ioutil.ReadAll(os.Stdin)
		if err != nil {
			panic(err)
		}
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
