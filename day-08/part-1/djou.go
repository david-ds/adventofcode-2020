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
	instructions := strings.Split(s, "\n")
	instructionCount := len(instructions)
	run := true
	i := 0
	accumulator := 0
	for run {
		switch instructions[i][0:3] {
		case "end":
			return accumulator
		case "jmp":
			jmp, _ := strconv.Atoi(instructions[i][4:])
			instructions[i] = "end"
			i += jmp
			run = i < instructionCount
		case "acc":
			acc, _ := strconv.Atoi(instructions[i][4:])
			accumulator += acc
			instructions[i] = "end"
			i += 1
			run = i < instructionCount
		case "nop":
			instructions[i] = "end"
			i += 1
			run = i < instructionCount
		}
	}

	return 0
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
