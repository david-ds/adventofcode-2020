package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
	"time"
)

const(
	rune1 = uint8('-')
	rune2 = uint8(' ')
	rune3 = uint8('\n')
)

func run(s string) interface{} {
	res := 0
	i := -1
	for i != len(s) {
		lastSep := i+1
		for i = lastSep; ; i++ {
			if s[i] == rune1 {
				break
			}
		}
		min, _ := strconv.Atoi(s[lastSep:i])
		lastSep = i + 1
		for i = lastSep; ; i++ {
			if s[i] == rune2 {
				break
			}
		}
		max, _ := strconv.Atoi(s[lastSep:i])
		carac := s[i+1]
		lastSep = i+4
		occ := 0
		for i = lastSep; i < len(s); i++ {
			if s[i] == rune3 {
				break
			}
			if s[i] == carac {
				occ++
			}
		}

		if occ >= min && occ <= max {
			res++
		}
	}
	return res
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
