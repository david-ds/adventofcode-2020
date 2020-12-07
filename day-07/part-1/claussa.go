package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	bagCanBeContainBy := make(map[string][]string, len(lines))
	for _, line := range lines {
		match := strings.Split(line, " bags contain")
		bagContainer := match[0]
		if match[1] != " no other bags." {
			for _, matchBag := range strings.Split(match[1], " bag") {
				if len(matchBag) < 3 {
					continue
				}
				i := 0
				for index, letter := range matchBag {
					if letter == ' ' {
						i = index
						break
					}
				}
				if bagCanBeContainBy[matchBag[i+3:]] == nil {
					bagCanBeContainBy[matchBag[i+3:]] = []string{bagContainer}
				} else {
					bagCanBeContainBy[matchBag[i+3:]] = append(bagCanBeContainBy[matchBag[i+3:]], bagContainer)
				}
			}
		}
	}
	countBag := make(map[string]int, len(lines))
	return computeLength("shiny gold", &bagCanBeContainBy, &countBag) - 1
}

func computeLength(containedBag string, bagCanBeContainBy *map[string][]string, countBag *map[string]int) int {
	if v, _ := (*countBag)[containedBag]; v == 1 {
		return 0
	}
	(*countBag)[containedBag] = 1
	sum := 1
	for _, bag := range (*bagCanBeContainBy)[containedBag] {
		sum += computeLength(bag, bagCanBeContainBy, countBag)
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
