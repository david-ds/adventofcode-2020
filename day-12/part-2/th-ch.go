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

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func run(s string) interface{} {
	shipX := 0
	shipY := 0
	wayPointX := 10
	wayPointY := -1

	for _, instr := range strings.Split(s, "\n") {
		action := instr[0]
		value, _ := strconv.Atoi(instr[1:])
		switch action {
		case 'N':
			wayPointY -= value
		case 'S':
			wayPointY += value
		case 'E':
			wayPointX += value
		case 'W':
			wayPointX -= value
		case 'L':
			switch value {
			case 90:
				wayPointX, wayPointY = wayPointY, -wayPointX
			case 180:
				wayPointX, wayPointY = -wayPointX, -wayPointY
			case 270:
				wayPointX, wayPointY = -wayPointY, wayPointX
			}
		case 'R':
			switch value {
			case 90:
				wayPointX, wayPointY = -wayPointY, wayPointX
			case 180:
				wayPointX, wayPointY = -wayPointX, -wayPointY
			case 270:
				wayPointX, wayPointY = wayPointY, -wayPointX
			}
		case 'F':
			shipX += value * wayPointX
			shipY += value * wayPointY
		}
	}

	return abs(shipX) + abs(shipY)
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
