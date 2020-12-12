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

func run(s string) interface{} {
	inputs := strings.Split(s, "\n")
	x := 0
	y := 0
	wpX := 10
	wpY := 1

	for _, input := range inputs {
		distance, _ := strconv.Atoi(input[1:])
		switch input[0] {
		case 'N':
			wpY += distance
		case 'S':
			wpY -= distance
		case 'E':
			wpX += distance
		case 'W':
			wpX -= distance
		case 'L':
			switch (distance / 90) % 4 {
			case 1:
				wpX, wpY = -wpY, wpX
			case 2:
				wpX = -wpX
				wpY = -wpY
			case 3:
				wpX, wpY = wpY, -wpX
			}
		case 'R':
			switch (distance / 90) % 4 {
			case 1:
				wpX, wpY = wpY, -wpX
			case 2:
				wpX = -wpX
				wpY = -wpY
			case 3:
				wpX, wpY = -wpY, wpX
			}
		case 'F':
			x += distance * wpX
			y += distance * wpY
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
