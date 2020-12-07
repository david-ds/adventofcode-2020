package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Bag struct {
	color    string
	children map[*Bag]int
}
func run(s string) interface{} {
	shinyGoldBag := Bag {
		color:    "shinygold",
		children: make(map[*Bag]int),
	}
	bags := map[string]Bag{
		"shinygold": shinyGoldBag,
	}

	rules := strings.Split(s, "\n")
	for _, rule := range rules {
		containerContained := strings.Split(rule, "contain ")
		container := strings.Split(containerContained[0], " ")
		containerBag := getOrCreateBag(bags, container[0] + container[1] )

		for _, contained := range strings.Split(containerContained[1], ", ") {
			if contained == "no other bags." {
				continue
			}
			c := strings.Split(contained, " ")
			containedBag := getOrCreateBag(bags, c[1] + c[2])
			containerBag.children[&containedBag], _ = strconv.Atoi(c[0])
		}
	}

	metBags := make(map[*Bag]int)
	for bagAddr, val := range shinyGoldBag.children {
		metBags[bagAddr] += val
		registerBags(bagAddr, val, metBags)
	}

	count := 0
	for _, val := range metBags {
		count += val
	}

	return count
}

func getOrCreateBag(bags map[string]Bag, bagColor string) Bag {
	if _, ok := bags[bagColor]; ok {
		return bags[bagColor]
	}

	bag := Bag {
		color:    bagColor,
		children: make(map[*Bag]int),
	}
	bags[bagColor] = bag

	return bag
}

func registerBags(bag *Bag, factor int, metBags map[*Bag]int)  {
	for bagAddr, val := range bag.children {
		metBags[bagAddr] += factor * val
		registerBags(bagAddr, factor * val, metBags)
	}

	return
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
