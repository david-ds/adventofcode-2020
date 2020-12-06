package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	sum := 0
	for _, answerGroup := range strings.Split(s, "\n\n") {
		sum += countDifferentAnswer(answerGroup)
	}
	return sum
}

func countDifferentAnswer(answers string) int {
	questionList := make([]int, 26)
	for _, questionLetter := range answers {
		questionNumber := questionLetter - 97
		if questionNumber < 26 && questionNumber >= 0 {
			questionList[questionNumber] = 1
		}
	}
	sum := 0
	for _, i := range questionList {
		sum += i
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
