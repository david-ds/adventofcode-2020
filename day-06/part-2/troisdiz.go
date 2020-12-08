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
    var sumQuestions int
    for _, group := range strings.Split(s, "\n\n") {
        groupSize := 0
        groupQuestions := make(map[string]int)
        for _, line := range strings.Split(group, "\n") {
            groupSize += 1
            for _, question := range line {
                qStr := string(question)
                count, _ := groupQuestions[qStr]
                groupQuestions[qStr] = count + 1
            }
        }
        for question := range groupQuestions {
           if groupQuestions[question] == groupSize {
               sumQuestions += 1
           }
        }
    }
    return sumQuestions
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
