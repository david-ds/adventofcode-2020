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

func neighborOk(x int, y int) bool {
	return x >= 0 && y >= 0 && y < len(seats) && x < len(seats[0])
}

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

func loop() bool {
	flip := make([][2]int, 0, nbSeats)

	for y := range seats {
		for x := range seats[y] {
			adjacent := [][2]int{
				[2]int{x - 1, y - 1},
				[2]int{x - 1, y},
				[2]int{x - 1, y + 1},
				[2]int{x, y - 1},
				[2]int{x, y + 1},
				[2]int{x + 1, y - 1},
				[2]int{x + 1, y},
				[2]int{x + 1, y + 1},
			}

			if seats[y][x] == empty {
				toOccupy := true
				for _, neighbor := range adjacent {
					if neighborOk(neighbor[0], neighbor[1]) && seats[neighbor[1]][neighbor[0]] == occupied {
						toOccupy = false
						break
					}
				}
				if toOccupy {
					flip = append(flip, [2]int{x, y})
				}
			} else if seats[y][x] == occupied {
				neighborsOccupied := 0
				for _, neighbor := range adjacent {
					if neighborOk(neighbor[0], neighbor[1]) && seats[neighbor[1]][neighbor[0]] == occupied {
						neighborsOccupied++
						if neighborsOccupied >= 4 {
							flip = append(flip, [2]int{x, y})
							break
						}
					}
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
