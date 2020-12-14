package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func parseBitMask(rawMask string) (int64, int64) {
	mask0, _ := strconv.ParseInt(strings.Replace(rawMask, "X", "0", -1), 2, 0)
	mask1, _ := strconv.ParseInt(strings.Replace(rawMask, "X", "1", -1), 2, 0)

	return mask0, mask1
}

func run(s string) interface{} {
	input := strings.Split(s, "\n")

	var mask0 int64 = 0
	var mask1 int64 = 1
	memory := make(map[string]int64)

	for _, instruction := range input {
		split := strings.Split(instruction, " = ")
		if split[0] == "mask" {
			mask0, mask1 = parseBitMask(split[1])
			continue
		}

		addr := strings.Replace(strings.Replace(split[0], "mem[", "", 1), "]", "", 1)
		value, _ := strconv.ParseInt(split[1], 10, 0)

		memory[addr] = (value & mask1) | mask0
	}

	var sum int64 = 0
	for _, value := range memory {
		sum += value
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
