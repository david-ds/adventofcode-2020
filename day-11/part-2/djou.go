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
				tooMuchOccupied := countOccupied(source, i, j)
				if tooMuchOccupied {
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

func countOccupied(source *[][]uint8, i int, j int) bool {
	count := 0
	if checkInDirection(source, i, j, +1, 0) {
		count += 1
	}
	if checkInDirection(source, i, j, 0, +1) {
		count += 1
	}
	if checkInDirection(source, i, j, -1, 0) {
		count += 1
	}
	if checkInDirection(source, i, j, 0, -1) {
		count += 1
	}
	if checkInDirection(source, i, j, +1, +1) {
		count += 1
		if count >= 5 {
			return true
		}
	}
	if checkInDirection(source, i, j, +1, -1) {
		count += 1
		if count >= 5 {
			return true
		}
	}
	if checkInDirection(source, i, j, -1, +1) {
		count += 1
		if count >= 5 {
			return true
		}
	}
	if checkInDirection(source, i, j, -1, -1) {
		count += 1
		if count >= 5 {
			return true
		}
	}

	return false
}

func checkOccupiedForEmpty(source *[][]uint8, i int, j int) bool {
	if checkInDirection(source, i, j, +1, 0) {
		return true
	}
	if checkInDirection(source, i, j, 0, +1) {
		return true
	}
	if checkInDirection(source, i, j, -1, 0) {
		return true
	}
	if checkInDirection(source, i, j, 0, -1) {
		return true
	}
	if checkInDirection(source, i, j, +1, +1) {
		return true
	}
	if checkInDirection(source, i, j, +1, -1) {
		return true
	}
	if checkInDirection(source, i, j, -1, +1) {
		return true
	}
	if checkInDirection(source, i, j, -1, -1) {
		return true
	}

	return false
}

func checkInDirection(source *[][]uint8, i int, j int, iOffset int, jOffset int) bool {
	x := j + jOffset
	y := i + iOffset

	for {
		if x < 0 || x >= width || y < 0 || y >= depth {
			return false
		}

		if (*source)[y][x] == OCCUPIED {
			return true
		}

		if (*source)[y][x] == EMPTY {
			return false
		}

		x += jOffset
		y += iOffset
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
