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
	for i := 0; i < instructionsNumber; i++ {
		switch instructions[i][:3] {
		case "acc":
			continue
		case "nop":
			instructions[i] = "jm" + instructions[i][2:]
			sucess, value := runProgram(&instructions, instructionsNumber)
			if sucess {
				return value
			} else {
				instructions[i] = "no" + instructions[i][2:]
			}
		case "jmp":
			instructions[i] = "no" + instructions[i][2:]
			sucess, value := runProgram(&instructions, instructionsNumber)
			if sucess {
				return value
			} else {
				instructions[i] = "jm" + instructions[i][2:]
			}
		}
	}
	return nil
}

func runProgram(instructions *[]string, instructionsNumber int) (bool, int) {
	doneInstructions := make([]int, instructionsNumber)
	accumulator := 0
	index := 0
	for {
		instruction := (*instructions)[index]
		if doneInstructions[index] == 1 {
			return false, 0
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
		if index == instructionsNumber {
			return true, accumulator
		}
		index = index % instructionsNumber
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
