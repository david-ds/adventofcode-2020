package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const JMP = 0
const NOP = 1
const ACC = 2

type Instruction struct {
	fun uint8
	val int64
}

func run(s string) interface{} {
	instructionsInput := strings.Split(s, "\n")
	instructionCount := len(instructionsInput)

	instructions := make([]Instruction, instructionCount)

	for i, instructionInput := range instructionsInput {
		instruction := Instruction{}

		switch instructionInput[0:3] {
		case "jmp":
			instruction.fun = JMP
		case "nop":
			instruction.fun = NOP
		case "acc":
			instruction.fun = ACC
		}

		instruction.val, _ = strconv.ParseInt(instructionInput[4:], 10, 16)
		instructions[i] = instruction
	}

	for i, instruction := range instructions {
		if instruction.fun == JMP || instruction.fun == NOP {
			out := runInstructionSet(&instructions, i)
			if out != 0 {
				return out
			}
		}
	}

	return 0
}

func runInstructionSet(instructions *[]Instruction, swapIndex int) int64 {
	i := 0
	var accumulator int64 = 0
	instructionCount := len(*instructions)
	visited := make([]int8, instructionCount)

	run := true
	for run {
		if visited[i] == 1 {
			return 0
		}
		fun := (*instructions)[i].fun
		if swapIndex == i {
			switch (*instructions)[i].fun {
			case NOP:
				fun = JMP
			case JMP:
				fun = NOP
			}
		}
		visited[i] = 1
		switch fun {
		case JMP:
			i += int((*instructions)[i].val)
			run = i < instructionCount
		case ACC:
			accumulator += (*instructions)[i].val
			i += 1
			run = i < instructionCount
		case NOP:
			i += 1
			run = i < instructionCount
		}
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
