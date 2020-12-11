package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const EMPTY = 1
const OCCUPIED = 2
const FLOOR = 3

var depth int
var width int

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	depth = len(lines)
	width = len(lines[0])
	mapA := make([][]uint8, depth)
	mapB := make([][]uint8, depth)

	for i := 0; i < depth; i++ {
		mapA[i] = make([]uint8, width)
		mapB[i] = make([]uint8, width)
		for j := 0; j < width; j++ {
			switch lines[i][j] {
			case 'L':
				mapA[i][j] = EMPTY
			case '#':
				mapA[i][j] = OCCUPIED
			case '.':
				mapA[i][j] = FLOOR
			}
			mapB[i][j] = mapA[i][j]
		}
	}

	var buffer *[][]uint8
	source := &mapA
	target := &mapB

	for {
		modified, occupiedCount := runMap(source, target)
		if !modified {
			return occupiedCount
		}

		buffer = source
		source = target
		target = buffer
	}
}

func runMap(source *[][]uint8, target *[][]uint8) (bool, int) {
	modified := false
	occupiedCount := 0
	for i := 0; i < depth; i++ {
		for j, val := range (*source)[i] {
			switch val {
			case EMPTY:
				hasOccupied := checkOccupiedForEmpty(source, i, j)
				if !hasOccupied {
					(*target)[i][j] = OCCUPIED
					modified = true
					occupiedCount += 1
				} else {
					(*target)[i][j] = EMPTY
				}
			case OCCUPIED:
				count := countOccupied(source, i, j)
				if count >= 4 {
					(*target)[i][j] = EMPTY
					modified = true
				} else {
					(*target)[i][j] = OCCUPIED
					occupiedCount += 1
				}
			}
		}
	}

	return modified, occupiedCount
}

func countOccupied(source *[][]uint8, i int, j int) int {
	count := 0
	if i - 1 >= 0 && (*source)[i - 1][j] == OCCUPIED {
		count += 1
	}
	if i + 1 < depth && (*source)[i + 1][j] == OCCUPIED {
		count += 1
	}
	if j - 1 >= 0 && (*source)[i][j - 1] == OCCUPIED {
		count += 1
	}
	if j + 1 < width && (*source)[i][j + 1] == OCCUPIED {
		count += 1
		if count >= 4 {
			return count
		}
	}
	if i - 1 >= 0 && j - 1 >= 0 && (*source)[i - 1][j - 1] == OCCUPIED {
		count += 1
		if count >= 4 {
			return count
		}
	}
	if i + 1 < depth && j - 1 >= 0 && (*source)[i + 1][j - 1] == OCCUPIED {
		count += 1
		if count >= 4 {
			return count
		}
	}
	if i - 1 >= 0 && j + 1 < width && (*source)[i - 1][j + 1] == OCCUPIED {
		count += 1
		if count >= 4 {
			return count
		}
	}
	if i + 1 < depth && j + 1 < width && (*source)[i + 1][j + 1] == OCCUPIED {
		count += 1
		if count >= 4 {
			return count
		}
	}

	return count
}

func checkOccupiedForEmpty(source *[][]uint8, i int, j int) bool {
	if i - 1 >= 0 && (*source)[i - 1][j] == OCCUPIED {
		return true
	}
	if i + 1 < depth && (*source)[i + 1][j] == OCCUPIED {
		return true
	}
	if j - 1 >= 0 && (*source)[i][j - 1] == OCCUPIED {
		return true
	}
	if j + 1 < width && (*source)[i][j + 1] == OCCUPIED {
		return true
	}
	if i - 1 >= 0 && j - 1 >= 0 && (*source)[i - 1][j - 1] == OCCUPIED {
		return true
	}
	if i + 1 < depth && j - 1 >= 0 && (*source)[i + 1][j - 1] == OCCUPIED {
		return true
	}
	if i - 1 >= 0 && j + 1 < width && (*source)[i - 1][j + 1] == OCCUPIED {
		return true
	}
	if i + 1 < depth && j + 1 < width && (*source)[i + 1][j + 1] == OCCUPIED {
		return true
	}

	return false
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
