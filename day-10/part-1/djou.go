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

func run(s string) interface{} {
	ptn := strings.Split(s, "\n")
	l := len(ptn)
	jpp := make([]int, l)
	for i, v := range ptn {
		jpp[i], _ = strconv.Atoi(v)
	}

	sort.Ints(jpp)

	domi := 0
	nique := 1
	if jpp[0] == 1 {
		domi += 1
	} else {
		nique += 1
	}

	for i, v := range jpp[:l - 1] {
		if jpp[i + 1] - v == 1 {
			domi += 1
		} else if jpp[i + 1] - v == 3 {
			nique += 1
		}

	}

	return domi * nique
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
