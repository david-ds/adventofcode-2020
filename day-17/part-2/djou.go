package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const ACTIVE = 1
const INACTIVE = 0
const CYCLES = 6

var l int
func run(s string) interface{} {
	input := strings.Split(s, "\n")
	l = len(input)
	// [x][y][z]
	gridA := make([][][][]int, 1 + 2 * CYCLES)
	gridB := make([][][][]int, 1 + 2 * CYCLES)

	for w, _ := range gridA {
		gridA[w] = make([][][]int, 1 + 2 * CYCLES)
		gridB[w] = make([][][]int, 1 + 2 * CYCLES)
		for i, _ := range gridA[w] {
			gridA[w][i] = make([][]int, l + 2 * CYCLES)
			gridB[w][i] = make([][]int, l + 2 * CYCLES)
			for j, _ := range gridA[w][i] {
				gridA[w][i][j] = make([]int, l + 2 * CYCLES)
				gridB[w][i][j] = make([]int, l + 2 * CYCLES)
			}
		}
	}


	for i, row := range input {
		for j, char := range row {
			switch char {
			case '#':
				gridA[CYCLES][CYCLES][i + CYCLES][j+ CYCLES] = ACTIVE
				gridB[CYCLES][CYCLES][i + CYCLES][j+ CYCLES] = ACTIVE
			case '.':
				gridA[CYCLES][CYCLES][i + CYCLES][j+ CYCLES] = INACTIVE
				gridB[CYCLES][CYCLES][i + CYCLES][j+ CYCLES] = INACTIVE
			}
		}
	}

	source := &gridA
	target := &gridB
	var buffer *[][][][]int

	cycle := 0
	var activeCount int
	for {
		activeCount = runCycle(source, target)

		buffer = source
		source = target
		target = buffer

		cycle++
		if cycle > 5 {
			break
		}
	}

	return activeCount
}

func runCycle(source *[][][][]int, target *[][][][]int) int {
	activeCount := 0
	for k, cube := range *source {
		for w, slice := range cube {
			for i, row :=  range slice {
				for j, microcube := range row {
					activeNeighbors := checkActiveNeighbors(source, k, w, i, j)
					if activeNeighbors == 2 && microcube == ACTIVE {
						(*target)[k][w][i][j] = ACTIVE
						activeCount++
					} else if activeNeighbors == 3 {
						(*target)[k][w][i][j] = ACTIVE
						activeCount++
					} else {
						(*target)[k][w][i][j] = INACTIVE
					}
				}
			}
		}

	}

	return activeCount
}

func checkActiveNeighbors(source *[][][][]int, k int, w int, i int, j int) int {
	neighborCount := 0
	d := []int{-1, 0, 1}
	for _, di := range d {
		if (di == -1 && i <= 0) || (di == 1 && i >= l + 2 * CYCLES - 1) {
			continue
		}
		for _, dj := range d {
			if (dj == -1 && j <= 0) || (dj == 1 && j >= l + 2 * CYCLES - 1) {
				continue
			}
			for _, dk := range d {
				if (dk == -1 && k <= 0) || (dk == 1 && k >= 2 * CYCLES) {
					continue
				}
				for _, dw := range d {
					if (dw == -1 && w <= 0) || (dw == 1 && w >= 2 * CYCLES) {
						continue
					}

					if dk == 0 && di == 0 && dj == 0 && dw == 0{
						continue
					}

					if (*source)[k + dk][w + dw][i + di][j + dj] == ACTIVE {
						neighborCount++
						if neighborCount == 4 {
							return neighborCount
						}
					}
				}
			}
		}
	}

	return neighborCount
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
