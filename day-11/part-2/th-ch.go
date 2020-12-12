package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

// Flipping empty/occupied with + 1 % 2
const empty uint8 = 0 // uint8 smaller type available
const occupied uint8 = 1
const notASeat uint8 = 2

var seats [][]uint8 // Faster than a map
var nbSeats = 0

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Neighbor functions to detect if there is an occupied seat
func left(x, y int) uint8 {
	for offset := 1; offset <= x; offset++ {
		if seats[y][x-offset] == occupied {
			return occupied
		}
		if seats[y][x-offset] == empty {
			return empty
		}
	}
	return notASeat
}

func leftTop(x, y int) uint8 {
	for offset := -1; offset >= max(-x, -y); offset-- {
		if seats[y+offset][x+offset] == occupied {
			return occupied
		}
		if seats[y+offset][x+offset] == empty {
			return empty
		}
	}
	return notASeat
}

func top(x, y int) uint8 {
	for offset := -1; offset >= -y; offset-- {
		if seats[y+offset][x] == occupied {
			return occupied
		}
		if seats[y+offset][x] == empty {
			return empty
		}
	}
	return notASeat
}

func topRight(x, y int) uint8 {
	for offset := 1; offset <= min(y, len(seats[y])-1-x); offset++ {
		if seats[y-offset][x+offset] == occupied {
			return occupied
		}
		if seats[y-offset][x+offset] == empty {
			return empty
		}
	}
	return notASeat
}

func right(x, y int) uint8 {
	for offset := 1; offset <= len(seats[y])-1-x; offset++ {
		if seats[y][x+offset] == occupied {
			return occupied
		}
		if seats[y][x+offset] == empty {
			return empty
		}
	}
	return notASeat
}

func bottomRight(x, y int) uint8 {
	for offset := 1; offset <= min(len(seats)-1-y, len(seats[y])-1-x); offset++ {
		if seats[y+offset][x+offset] == occupied {
			return occupied
		}
		if seats[y+offset][x+offset] == empty {
			return empty
		}
	}
	return notASeat
}

func bottom(x, y int) uint8 {
	for offset := 1; offset <= len(seats)-1-y; offset++ {
		if seats[y+offset][x] == occupied {
			return occupied
		}
		if seats[y+offset][x] == empty {
			return empty
		}
	}
	return notASeat
}

func leftBottom(x, y int) uint8 {
	for offset := 1; offset <= min(len(seats)-1-y, x); offset++ {
		if seats[y+offset][x-offset] == occupied {
			return occupied
		}
		if seats[y+offset][x-offset] == empty {
			return empty
		}
	}
	return notASeat
}

// End of neighbor functions

func nbOccupied() int {
	nbOccupied := 0
	for y := range seats {
		for x := range seats[y] {
			if seats[y][x] == occupied {
				nbOccupied++
			}
		}
	}
	return nbOccupied
}

var adjacent = [](func(x, y int) uint8){
	left, leftTop, top, topRight, right, bottomRight, bottom, leftBottom,
}

func loop() bool {
	flip := make([][2]int, 0, nbSeats)

	for y := range seats {
		for x := range seats[y] {
			if seats[y][x] == empty {
				toOccupy := true
				for _, neighbor := range adjacent {
					if neighbor(x, y) == occupied {
						toOccupy = false
						break
					}
				}
				if toOccupy {
					flip = append(flip, [2]int{x, y})
				}
			} else if seats[y][x] == occupied {
				nbOccupied := 0
				for _, neighbor := range adjacent {
					if neighbor(x, y) == occupied {
						nbOccupied++
						if nbOccupied >= 5 {
							break
						}
					}
				}
				if nbOccupied >= 5 {
					flip = append(flip, [2]int{x, y})
				}
			}
		}
	}

	for _, toFlip := range flip {
		seats[toFlip[1]][toFlip[0]] = (seats[toFlip[1]][toFlip[0]] + 1) % 2
	}

	return len(flip) > 0
}

func run(s string) interface{} {
	input := strings.Split(s, "\n")
	seats = make([][]uint8, len(input))

	// Parse
	for y, line := range input {
		seats[y] = make([]uint8, len(line))
		for x, seat := range strings.Split(line, "") {
			if seat == "." {
				seats[y][x] = notASeat
			} else if seat == "#" {
				nbSeats++
				seats[y][x] = occupied
			} else {
				nbSeats++
				seats[y][x] = empty
			}
		}
	}

	for {
		if !loop() {
			break
		}
	}

	return nbOccupied()
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
