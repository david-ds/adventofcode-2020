package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const nthNumber = 2020

func run(s string) interface{} {
	numbers := strings.Split(s, ",")
	lastSpoken := 0
	previousPosition := 0
	game := make([]int, nthNumber)

	for turn, number := range numbers {
		nb, _ := strconv.Atoi(number)
		game[nb] = turn + 1
		lastSpoken = nb
	}

	for turn := len(numbers); turn < nthNumber; turn++ {
		nbToSay := 0
		if game[lastSpoken] > 0 && previousPosition > 0 {
			nbToSay = game[lastSpoken] - previousPosition
		}
		previousPosition = game[nbToSay]

		lastSpoken = nbToSay
		game[lastSpoken] = turn + 1
	}

	return lastSpoken
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
