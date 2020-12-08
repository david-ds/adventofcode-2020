package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	instructions := strings.Split(s, "\n")
	instructionsNumber := len(instructions)
	doneInstructions := make([]int, instructionsNumber)
	accumulator := 0
	index := 0
	for {
		instruction := instructions[index]
		if doneInstructions[index] == 1 {
			break
		}
		doneInstructions[index] = 1
		switch instruction[:3] {
		case "nop":
			index += 1
		case "acc":
			value, _ := strconv.Atoi(instruction[4:])
			accumulator += value
			index += 1
		case "jmp":
			value, _ := strconv.Atoi(instruction[4:])
			index += value
		}
		index = index % instructionsNumber
	}
	return accumulator
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
