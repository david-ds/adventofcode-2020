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

type MaskPair struct {
	or uint64
	and uint64
}

var memory = map[uint64]int{}

func run(s string) interface{} {
	inputs := strings.Split(s, "\n")

	var mask uint64
	var maskPairs []MaskPair
	for _, input := range inputs {
		if input[:4] == "mask" {
			mask = 0
			maskPairs = make([]MaskPair, 0)
			for i, c := range input[7:] {
				mask <<= 1
				if c == '1' {
					mask += 1
				} else if c == 'X' {
					bit := uint64(math.Pow(2, float64(35 - i)))
					maskPairs = append(maskPairs, MaskPair{
						or: bit,
						and: 0b111111111111111111111111111111111111 ^ bit,
					})
				}
			}
		} else {
			a := strings.Split(input, "] = ")
			addr, _ := strconv.Atoi(a[0][4:])
			value, _ := strconv.Atoi(a[1])
			applyMasks(&maskPairs, uint64(addr) | mask, 0, value)
		}
	}

	tot := 0
	for _, val := range memory {
		tot += val

	}

	return tot
}

func applyMasks(maskPairs *[]MaskPair, addr uint64, i int, value int) {
	if i >= len(*maskPairs) {
		memory[addr] = value
		return
	}

	applyMasks(maskPairs, addr | (*maskPairs)[i].or, i+1, value)
	applyMasks(maskPairs, addr & (*maskPairs)[i].and, i+1, value)
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
