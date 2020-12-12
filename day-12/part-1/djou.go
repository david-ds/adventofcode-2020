package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

const E = 0
const S = 1
const W = 2
const N = 3

func run(s string) interface{} {
	inputs := strings.Split(s, "\n")
	x := 0
	y := 0
	facing := E

	for _, input := range inputs {
		distance, _ := strconv.Atoi(input[1:])
		switch input[0] {
		case 'N':
			y += distance
		case 'S':
			y -= distance
		case 'E':
			x += distance
		case 'W':
			x -= distance
		case 'L':
			facing -= distance / 90
			for facing < 0 {
				facing += 4
			}
		case 'R':
			facing += distance / 90
		case 'F':
			switch facing % 4 {
			case N:
				y += distance
			case S:
				y -= distance
			case E:
				x += distance
			case W:
				x -= distance
			}
		}
	}

	return math.Abs(float64(x)) + math.Abs(float64(y))
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
