package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

type Bag struct {
	color   string
	contain int
}

var linePattern = regexp.MustCompile(`^(?P<bag>\w+ \w+) bags? contain((?: \d+ \w+ \w+ bags?,?)+| no other bags?).$`)
var bagPattern = regexp.MustCompile(`(\d+) (\w+ \w+) bags?`)

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	bagCanBeContainBy := make(map[string][]Bag, len(lines))
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
				canContain, _ := strconv.Atoi(matchBag[i+1:i+2])
				bag := Bag{matchBag[i+3:], canContain}
				if bagCanBeContainBy[bagContainer] == nil {
					bagCanBeContainBy[bagContainer] = []Bag{bag}
				} else {
					bagCanBeContainBy[bagContainer] = append(bagCanBeContainBy[bagContainer], bag)
				}
			}
		}
	}
	count := 0
	for _, child := range bagCanBeContainBy["shiny gold"] {
		count += computeLength(child.color, child.contain, &bagCanBeContainBy)
	}
	return count
}

func computeLength(containedBag string, factor int, bagCanBeContainBy *map[string][]Bag) int {
	sum := 1
	for _, bag := range (*bagCanBeContainBy)[containedBag] {
		sum += computeLength(bag.color, bag.contain, bagCanBeContainBy)
	}
	return sum * factor
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
