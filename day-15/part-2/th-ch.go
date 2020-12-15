package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
	"strings"
	"time"
)

const nthNumber = 30000000

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

	for turn := len(numbers) + 1; turn < nthNumber+1; turn++ {
		if game[lastSpoken] > 0 && previousPosition > 0 {
			lastSpoken = game[lastSpoken] - previousPosition
		} else {
			lastSpoken = 0
		}
		previousPosition = game[lastSpoken]
		game[lastSpoken] = turn
	}

	return lastSpoken
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
