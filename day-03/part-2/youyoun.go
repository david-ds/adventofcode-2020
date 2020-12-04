package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type pos struct {
	x int
	y int
}

func run(s string) interface{} {
	map_ := strings.Split(s, "\n")
	h := len(map_)
	w := len(map_[0])

	positions := map[int]pos{
		0: pos{0, 0},
		1: pos{0, 0},
		2: pos{0, 0},
		3: pos{0, 0},
		4: pos{0, 0},
	}

	mvts := map[int]pos{
		0: pos{1, 1},
		1: pos{3, 1},
		2: pos{5, 1},
		3: pos{7, 1},
		4: pos{1, 2},
	}

	counters := map[int]int{
		0: 0,
		1: 0,
		2: 0,
		3: 0,
		4: 0,
	}
	for i := 0; i < h; i++ {
		for k, v := range positions {
			if v.y < h && map_[v.y][v.x] == '#' {
				counters[k] += 1
			}
			positions[k] = pos{(v.x + mvts[k].x) % w, v.y + mvts[k].y}

		}
	}
	res := 1
	for _, v := range counters {
		res *= v
	}
	return res
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
