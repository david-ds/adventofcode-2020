package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s []byte) int {
	var start int
	f := make([]int, 0, 100)

	i := 0
	for s[i] >= byte('0') && s[i] <= byte('9') {
		start = start*10 + int(s[i]-byte('0'))
		i++
	}
	i++
	for i < len(s) && s[i] != byte('\n') {
		if s[i] == 'x' {
			i++
			if s[i] == ',' {
				i++
			}
			continue
		}
		if i == len(s) {
			break
		}
		n := len(f)
		f = append(f, 0)
		for i < len(s) && s[i] >= byte('0') && s[i] <= byte('9') {
			f[n] = f[n]*10 + int(s[i]-'0')
			i++
		}
		if i < len(s) && s[i] == ',' {
			i++
		}
	}

	var min int = 1 << 30
	var x, r int
	for i = 0; i < len(f); i++ {
		x = start - (start % f[i])
		for x <= start {
			x += f[i]
		}
		if x < min {
			min = x
			r = (x - start) * f[i]
		}
	}

	return r
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
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
