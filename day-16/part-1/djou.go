package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Range struct {
	low int
	high int
}

func run(s string) interface{} {
	input := strings.Split(s, "\n\n")
	fields := strings.Split(input[0], "\n")
	passports := strings.Split(input[2], "\n")[1:]
	ranges := make([]Range, 0)

	for _, field := range fields {
		info := strings.Split(field, ": ")
		for _, r := range strings.Split(info[1], " or ") {
			lowHigh := strings.Split(r, "-")
			low, _ := strconv.Atoi(lowHigh[0])
			high, _ := strconv.Atoi(lowHigh[1])
			ranges = append(ranges, Range{
				low: low,
				high: high,
			})
		}
	}

	total := 0
	for _, passport := range passports {
		values := strings.Split(passport, ",")
		for _, val := range values {
			intVal, _ := strconv.Atoi(val)
			if !isInRange(&ranges, intVal) {
				total += intVal
			}
		}
	}

	return total
}


func isInRange(ranges *[]Range, value int) bool {
	for _, r := range *ranges {
		if r.includes(value) {
			return true
		}
	}

	return false
}

func (r Range) includes(value int) bool {
	return value >= r.low && value <= r.high
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
