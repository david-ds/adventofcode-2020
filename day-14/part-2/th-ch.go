package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	input := strings.Split(s, "\n")

	regex := regexp.MustCompile(`X`)

	var mask1 int64 = 1
	var floating []int
	memory := make(map[int64]int)

	for _, instruction := range input {
		split := strings.Split(instruction, " = ")

		if split[0] == "mask" {
			mask := split[1]
			allIndexes := regex.FindAllIndex([]byte(mask), -1)
			floating = make([]int, len(allIndexes))
			for i, index := range allIndexes {
				floating[i] = 35 - index[0]
			}
			mask1, _ = strconv.ParseInt(strings.Replace(mask, "X", "1", -1), 2, 0)
			continue
		}

		addrStr := strings.Replace(strings.Replace(split[0], "mem[", "", 1), "]", "", 1)
		addr, _ := strconv.ParseInt(addrStr, 10, 0)
		addr = addr | mask1 // Replace all X by 1 (last combination)
		value, _ := strconv.Atoi(split[1])

		for combination := 0; combination < 1<<len(floating); combination++ {
			addrBis := addr

			for i, pos := range floating {
				if combination&(1<<i) == (1 << i) {
					addrBis |= (1 << pos) // Set the bit to 1 at position
				} else {
					addrBis &= ^(1 << pos) // Set the bit to 0 at position
				}
			}

			memory[addrBis] = value
		}
	}

	sum := 0
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
