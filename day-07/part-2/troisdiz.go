package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strconv"
    "strings"
	"time"
)

type BagRegister struct {
    bags map[string]*Bag
    count int
}

func (reg *BagRegister) getOrCreateBag(name string) *Bag {
    bagPtr, ok := reg.bags[name]
    if !ok {
        var bag = Bag { name: name }
        bagPtr = &bag
        reg.bags[name] = bagPtr
    }
    return bagPtr
}

type InsideBag struct {
    childBag *Bag
    quantity int
}

type Bag struct {
    name string
    mustContain []InsideBag
    possibleContainers []*Bag
}

func (bag *Bag) addContent(containedBag *Bag, quantity int) {
    bag.mustContain = append(bag.mustContain, InsideBag { childBag: containedBag, quantity: quantity })
    containedBag.possibleContainers = append(containedBag.possibleContainers, bag)
}

func parseRule(rule string) (string, []string, []int) {

    containSplit := strings.Split(rule, " bags contain ")
    containerName := containSplit[0]

    var subNames []string
    var subCounts []int
    for _, subBagStr := range strings.Split(containSplit[1], ", ") {
        //fmt.Printf("l51 : %v\n", subBagStr)
        subBagItemsStr := strings.Split(subBagStr, " ")
        //fmt.Printf("l53 : %v\n", subBagItemsStr)
        count, _ := strconv.Atoi(subBagItemsStr[0])
        name := subBagItemsStr[1] + " " + subBagItemsStr[2]

        subNames = append(subNames, name)
        subCounts = append(subCounts, count)
    }
    return containerName, subNames, subCounts
}


func computeSubBagCount(bag *Bag) int {

    var result int = 1
    for _, subInsideBag := range bag.mustContain {
        result += subInsideBag.quantity * computeSubBagCount(subInsideBag.childBag)
    }
    return result
}

func run(s string) interface{} {

    var reg BagRegister = BagRegister { bags: make(map[string]*Bag) }

    for _, rule := range strings.Split(s, "\n") {
        containerName, subNames, subCounts := parseRule(rule)
        containerBag := reg.getOrCreateBag(containerName)

        for idx, name := range subNames {
            subBag := reg.getOrCreateBag(name)
            containerBag.addContent(subBag, subCounts[idx])
        }
    }

    rootBag := reg.getOrCreateBag("shiny gold")

    return computeSubBagCount(rootBag) -1
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
