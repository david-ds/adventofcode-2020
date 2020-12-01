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
	var ts = strings.Split(s, "\n")
	var l = len(ts)
	ti := make([]int, l)
	for i, t := range ts {
		ti[i], _ = strconv.Atoi(t)
	}
	for i := 0; i < l; i++ {
		for j := i + 1; j < l; j++ {
			for k := j + 1; k < l; k++ {
				if ti[i] + ti[j] + ti[k] == 2020 {
					return ti[i] * ti[j] * ti[k]
				}
			}
		}
	}
	return 0
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
