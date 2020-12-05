package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	occupiedSeats := make([]uint64, 975)
	var min = ^uint64(0)
	for index, pass := range strings.Split(s, "\n") {
		seatId := calculateSeatIn(pass)
		occupiedSeats[index] = seatId
		if seatId < min {
			min = seatId
		}
	}

	for {
		if contains(occupiedSeats, min) {
			min += 1
			continue
		} else {
			return min
		}
	}
}

func contains(array []uint64, value uint64) bool {
	for _, a := range array {
		if a == value {
			return true
		}
	}
	return false
}

func calculateSeatIn(pass string) uint64 {
	rowString, err := convertToBinary(pass[:7], 'F', 'B')
	if err != nil {
		println(err)
	}
	colString, err := convertToBinary(pass[7:], 'L', 'R')
	if err != nil {
		println(err)
	}
	row, _ := strconv.ParseUint(rowString, 2, 16)
	col, _ := strconv.ParseUint(colString, 2, 16)
	return row * 8 + col
}

func convertToBinary(s string, zero rune, one rune) (string, error) {
	binaryString := make([]rune, len(s))
	for index, letter := range s {
		if letter == zero {
			binaryString[index] = '0'
		} else if letter == one {
			binaryString[index] = '1'
		} else {
			return "", errors.New("Letter " + string(letter) + " cannot be convert to 0 or 1")
		}
	}
	return string(binaryString), nil
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
