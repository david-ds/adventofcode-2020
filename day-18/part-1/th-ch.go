package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func evaluate(op string, currentVal int) int {
	start := strings.LastIndex(op, " ")
	if start == -1 {
		val, _ := strconv.Atoi(op)
		return val
	}

	firstPart := op[start+1:]

	if firstPart == "+" {
		return evaluate(op[:start], 0) + currentVal
	}

	if firstPart == "*" {
		firstVal := evaluate(op[:start], 0)
		return firstVal * currentVal
	}

	if firstPart[len(firstPart)-1] == ')' {
		countParenthesis := 0
		beginParenthesis := -1
		for i := len(op) - 1; i >= 0; i-- {
			if op[i] == ')' {
				countParenthesis++
			} else if op[i] == '(' {
				countParenthesis--
				if countParenthesis == 0 {
					beginParenthesis = i
					break
				}
			}
		}

		endVal := evaluate(op[beginParenthesis+1:len(op)-1], 0)

		rest := strings.TrimSpace(op[:beginParenthesis])
		if len(rest) == 0 {
			return endVal
		}
		return evaluate(rest, endVal)
	}

	val, _ := strconv.Atoi(firstPart)

	return evaluate(op[:start], val)
}

func run(s string) interface{} {
	sum := 0
	for _, line := range strings.Split(s, "\n") {
		sum += evaluate(line, 0)
	}

	return sum
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
