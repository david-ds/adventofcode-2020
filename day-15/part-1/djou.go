package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const NUMBER = 2021

func run(s string) interface{} {
	input := strings.Split(s, ",")
	memory := [NUMBER]int32{0}

	var i int32 = 1
	var lastSpoken int32 = 0
	var newNumber int32 = 0
	for _, in := range input {
		val, _ := strconv.Atoi(in)
		if memory[val] == 0 {
			newNumber = int32(val)
		} else {
			newNumber = i - memory[val] - 1
		}

		memory[lastSpoken] = i - 1
		lastSpoken = newNumber
		i++
	}

	for {
		if memory[lastSpoken] == 0 {
			newNumber = 0
		} else {
			newNumber = i - memory[lastSpoken] - 1
		}
		memory[lastSpoken] = i - 1
		lastSpoken = newNumber
		i++
		if i == NUMBER {
			return lastSpoken
		}
	}
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
