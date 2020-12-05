package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

func parse(s string) []int {
	lines := strings.Split(s, "\n")
	res := make([]int, len(lines))
	for i := 0; i < len(lines); i++ {
		res[i], _ = strconv.Atoi(lines[i])
	}
	return res
}

func run(s string) interface{} {
	inputs := parse(s)
	sort.Ints(inputs)

	n := len(inputs)

	i := 0
	j := n-1
	k := 0
	for {
		a := inputs[i] + inputs[j] + inputs[k]
		if a == 2020{
			return inputs[i] * inputs[j] * inputs[k]
		}
		if a > 2020 {
			j--
			k = i+1
		} else {
			k++
		}
		if k >= j {
			i++
			j = n-1
		}
	}
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
