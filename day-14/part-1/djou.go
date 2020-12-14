package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	inputs := strings.Split(s, "\n")

	memory := map[int]uint64{}
	var setBitmask uint64
	var unsetBitmask uint64

	for _, input := range inputs {
		if input[:4] == "mask" {
			setBitmask = 0
			unsetBitmask = 0
			for _, c := range input[7:] {
				setBitmask <<= 1
				unsetBitmask <<= 1
				if c == '1' {
					unsetBitmask += 1
					setBitmask += 1
				} else if c =='X' {
					unsetBitmask += 1
				}
			}
		} else {
			a := strings.Split(input, "] = ")
			addr, _ := strconv.Atoi(a[0][4:])
			value, _ := strconv.Atoi(a[1])
			memory[addr] = (uint64(value) | setBitmask) & unsetBitmask
		}
	}

	var tot uint64 = 0
	for _, val := range memory {
		tot += val
	}

	return tot
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
