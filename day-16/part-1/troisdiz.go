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

func parseTicket(input string) []int {
	var result []int
	for _, itemStr := range strings.Split(input, ",") {
		item, _ := strconv.Atoi(itemStr)
		result = append(result, item)
	}
	return result
}

func run(s string) interface{} {
	// Your code goes here
	parts := strings.Split(s, "\n\nyour ticket:\n")
	fieldsStr := parts[0]

	parts = strings.Split(parts[1], "\n\nnearby tickets:\n")
	//yourTicketStr := parts[0]
	nearbyTicketsStr := parts[1]

	var ticketRules []TicketRule
	for _, fieldStr := range strings.Split(fieldsStr, "\n") {
		tr := parseTicketRules(fieldStr)
		ticketRules = append(ticketRules, tr)
	}
	//yourTicket := parseTicket(yourTicketStr)

	var nearbyTickets [][]int
	for _, line := range strings.Split(nearbyTicketsStr, "\n") {
		nearbyTickets = append(nearbyTickets, parseTicket(line))
	}

	//fmt.Printf("Ticket rules : %v\n", ticketRules)
	//fmt.Printf("Nearby tickets : %v\n", nearbyTickets)

	var sum int
	for _, ticket := range nearbyTickets {
		for _, number := range ticket {
			validates := false
			for _, tr := range ticketRules {
				if tr.validate(number) {
					validates = true
					break
				}
			}
			if !validates {
				sum += number
				//fmt.Printf("%d not ok\n", number)
			}
		}
	}

	return sum
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
