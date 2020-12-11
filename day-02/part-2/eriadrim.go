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
		ind1, _ := strconv.Atoi(s[lastSep:i])
		lastSep = i + 1
		for i = lastSep; ; i++ {
			if s[i] == rune2 {
				break
			}
		}
		ind2, _ := strconv.Atoi(s[lastSep:i])
		carac := s[i+1]
		lastSep = i+3

		if s[lastSep+ind1] == carac && s[lastSep+ind2] != carac {
			res++
		}
		if s[lastSep+ind2] == carac && s[lastSep+ind1] != carac {
			res++
		}

		for i = lastSep+ind2+1; i < len(s); i++ {
			if s[i] == rune3 {
				break
			}
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
