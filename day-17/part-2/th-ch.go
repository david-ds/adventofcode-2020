package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type Coord struct {
	x, y, z, w int
}

func (c Coord) getNeighbors() []Coord {
	return []Coord{
		Coord{c.x - 1, c.y - 1, c.z - 1, c.w - 1},
		Coord{c.x - 1, c.y - 1, c.z, c.w - 1},
		Coord{c.x - 1, c.y - 1, c.z + 1, c.w - 1},
		Coord{c.x - 1, c.y, c.z - 1, c.w - 1},
		Coord{c.x - 1, c.y, c.z, c.w - 1},
		Coord{c.x - 1, c.y, c.z + 1, c.w - 1},
		Coord{c.x - 1, c.y + 1, c.z - 1, c.w - 1},
		Coord{c.x - 1, c.y + 1, c.z, c.w - 1},
		Coord{c.x - 1, c.y + 1, c.z + 1, c.w - 1},
		Coord{c.x, c.y - 1, c.z - 1, c.w - 1},
		Coord{c.x, c.y - 1, c.z, c.w - 1},
		Coord{c.x, c.y - 1, c.z + 1, c.w - 1},
		Coord{c.x, c.y, c.z - 1, c.w - 1},
		Coord{c.x, c.y, c.z, c.w - 1},
		Coord{c.x, c.y, c.z + 1, c.w - 1},
		Coord{c.x, c.y + 1, c.z - 1, c.w - 1},
		Coord{c.x, c.y + 1, c.z, c.w - 1},
		Coord{c.x, c.y + 1, c.z + 1, c.w - 1},
		Coord{c.x + 1, c.y - 1, c.z - 1, c.w - 1},
		Coord{c.x + 1, c.y - 1, c.z, c.w - 1},
		Coord{c.x + 1, c.y - 1, c.z + 1, c.w - 1},
		Coord{c.x + 1, c.y, c.z - 1, c.w - 1},
		Coord{c.x + 1, c.y, c.z, c.w - 1},
		Coord{c.x + 1, c.y, c.z + 1, c.w - 1},
		Coord{c.x + 1, c.y + 1, c.z - 1, c.w - 1},
		Coord{c.x + 1, c.y + 1, c.z, c.w - 1},
		Coord{c.x + 1, c.y + 1, c.z + 1, c.w - 1},
		Coord{c.x - 1, c.y - 1, c.z - 1, c.w},
		Coord{c.x - 1, c.y - 1, c.z, c.w},
		Coord{c.x - 1, c.y - 1, c.z + 1, c.w},
		Coord{c.x - 1, c.y, c.z - 1, c.w},
		Coord{c.x - 1, c.y, c.z, c.w},
		Coord{c.x - 1, c.y, c.z + 1, c.w},
		Coord{c.x - 1, c.y + 1, c.z - 1, c.w},
		Coord{c.x - 1, c.y + 1, c.z, c.w},
		Coord{c.x - 1, c.y + 1, c.z + 1, c.w},
		Coord{c.x, c.y - 1, c.z - 1, c.w},
		Coord{c.x, c.y - 1, c.z, c.w},
		Coord{c.x, c.y - 1, c.z + 1, c.w},
		Coord{c.x, c.y, c.z - 1, c.w},
		// Coord{c.x, c.y, c.z, c.w},
		Coord{c.x, c.y, c.z + 1, c.w},
		Coord{c.x, c.y + 1, c.z - 1, c.w},
		Coord{c.x, c.y + 1, c.z, c.w},
		Coord{c.x, c.y + 1, c.z + 1, c.w},
		Coord{c.x + 1, c.y - 1, c.z - 1, c.w},
		Coord{c.x + 1, c.y - 1, c.z, c.w},
		Coord{c.x + 1, c.y - 1, c.z + 1, c.w},
		Coord{c.x + 1, c.y, c.z - 1, c.w},
		Coord{c.x + 1, c.y, c.z, c.w},
		Coord{c.x + 1, c.y, c.z + 1, c.w},
		Coord{c.x + 1, c.y + 1, c.z - 1, c.w},
		Coord{c.x + 1, c.y + 1, c.z, c.w},
		Coord{c.x + 1, c.y + 1, c.z + 1, c.w},
		Coord{c.x - 1, c.y - 1, c.z - 1, c.w + 1},
		Coord{c.x - 1, c.y - 1, c.z, c.w + 1},
		Coord{c.x - 1, c.y - 1, c.z + 1, c.w + 1},
		Coord{c.x - 1, c.y, c.z - 1, c.w + 1},
		Coord{c.x - 1, c.y, c.z, c.w + 1},
		Coord{c.x - 1, c.y, c.z + 1, c.w + 1},
		Coord{c.x - 1, c.y + 1, c.z - 1, c.w + 1},
		Coord{c.x - 1, c.y + 1, c.z, c.w + 1},
		Coord{c.x - 1, c.y + 1, c.z + 1, c.w + 1},
		Coord{c.x, c.y - 1, c.z - 1, c.w + 1},
		Coord{c.x, c.y - 1, c.z, c.w + 1},
		Coord{c.x, c.y - 1, c.z + 1, c.w + 1},
		Coord{c.x, c.y, c.z - 1, c.w + 1},
		Coord{c.x, c.y, c.z, c.w + 1},
		Coord{c.x, c.y, c.z + 1, c.w + 1},
		Coord{c.x, c.y + 1, c.z - 1, c.w + 1},
		Coord{c.x, c.y + 1, c.z, c.w + 1},
		Coord{c.x, c.y + 1, c.z + 1, c.w + 1},
		Coord{c.x + 1, c.y - 1, c.z - 1, c.w + 1},
		Coord{c.x + 1, c.y - 1, c.z, c.w + 1},
		Coord{c.x + 1, c.y - 1, c.z + 1, c.w + 1},
		Coord{c.x + 1, c.y, c.z - 1, c.w + 1},
		Coord{c.x + 1, c.y, c.z, c.w + 1},
		Coord{c.x + 1, c.y, c.z + 1, c.w + 1},
		Coord{c.x + 1, c.y + 1, c.z - 1, c.w + 1},
		Coord{c.x + 1, c.y + 1, c.z, c.w + 1},
		Coord{c.x + 1, c.y + 1, c.z + 1, c.w + 1},
	}
}

const nbLoops = 6

type Cubes map[Coord]bool

func (cubes Cubes) shouldToggle(coord Coord) bool {
	nbNeighborsActive := 0
	for _, neighbor := range coord.getNeighbors() {
		if cubes[neighbor] {
			nbNeighborsActive++
			if nbNeighborsActive >= 4 {
				break
			}
		}
	}

	return (cubes[coord] && (nbNeighborsActive != 2 && nbNeighborsActive != 3)) ||
		(!cubes[coord] && nbNeighborsActive == 3)
}

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	cubes := make(Cubes, len(lines)*500)

	for y, line := range lines {
		for x, c := range line {
			if c == '#' {
				cubes[Coord{x, y, 0, 0}] = true
			}
		}
	}

	for cycle := 1; cycle <= nbLoops; cycle++ {
		seen := make(map[Coord]struct{})
		toggles := make(map[Coord]struct{})
		for coord := range cubes {
			if _, ok := seen[coord]; !ok && cubes.shouldToggle(coord) {
				toggles[coord] = struct{}{}
			}
			seen[coord] = struct{}{}

			for _, neighbor := range coord.getNeighbors() {
				if _, ok := seen[neighbor]; !ok && cubes.shouldToggle(neighbor) {
					toggles[neighbor] = struct{}{}
				}

				seen[neighbor] = struct{}{}
			}
		}

		for toggle := range toggles {
			if cubes[toggle] {
				delete(cubes, toggle)
			} else {
				cubes[toggle] = true
			}
		}
	}

	nbActive := 0
	for coord := range cubes {
		if cubes[coord] {
			nbActive++
		}
	}

	return nbActive
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
