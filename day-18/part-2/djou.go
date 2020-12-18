package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const LEFT_PARENTHESIS = '('
const RIGHT_PARENTHESIS = ')'
const SUM = '+'
const MULTIPLY = '*'
const NONE = '\\'

func run(s string) interface{} {
	input := strings.Split(s, "\n")
	tot:= 0
	for _, formulae := range input {
		tot += evaluateMember(strings.ReplaceAll(formulae, " ", ""))
	}

	return tot
}

func evaluateMember(member string) int {
	tot := 0
	lastOperator := NONE
	for i := 0; i < len(member); i++ {
		c := member[i]
		switch c {
		case SUM:
			lastOperator = SUM
		case MULTIPLY:
			inBetweenMultiplicationsMemberThatAreToBeCalculatedPrioritarily := tilNextMultiplicationBruh(member[i+1:])
			i += len(inBetweenMultiplicationsMemberThatAreToBeCalculatedPrioritarily)
			val := evaluateMember(inBetweenMultiplicationsMemberThatAreToBeCalculatedPrioritarily)
			tot *= val
		case LEFT_PARENTHESIS:
			parenthesisMember := tilNextParenthesisM8(member[i+1:])
			i += len(parenthesisMember)
			val := evaluateMember(parenthesisMember)
			switch lastOperator {
			case SUM:
				tot += val
			case NONE:
				tot = val
			}
		case RIGHT_PARENTHESIS:
			continue
		default:
			val, _ := strconv.Atoi(string(member[i]))
			switch lastOperator {
			case SUM:
				tot += val
			case NONE:
				tot = val
			}
		}
	}

	return tot
}

func tilNextParenthesisM8(member string) string {
	depth := 1
	for i, c := range member {
		switch c {
		case LEFT_PARENTHESIS:
			depth++
		case RIGHT_PARENTHESIS:
			depth--
		}

		if depth == 0 {
			return member[:i]
		}
	}

	return member
}

func tilNextMultiplicationBruh(member string) string {
	depth := 0
	for i, c := range member {
		switch c {
		case LEFT_PARENTHESIS:
			depth++
		case RIGHT_PARENTHESIS:
			depth--
		case MULTIPLY:
			if depth == 0 {
				return member[:i]
			}
		}
	}

	return member
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
