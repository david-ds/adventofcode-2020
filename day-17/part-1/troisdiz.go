package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type Coord struct {
	x, y, z int
}

type Map struct {
	minX, maxX int
	minY, maxY int
	minZ, maxZ int
	values map[Coord]bool
}

func createMap() *Map {
	var result Map = Map { values: make(map[Coord]bool)}
	return &result
}

func (mp *Map) set(x int, y int, z int, value bool) {
	if mp.minX > x {
		mp.minX = x
	}
	if mp.maxX < x {
		mp.maxX = x
	}
	if mp.minY > y {
		mp.minY = y
	}
	if mp.maxY < y {
		mp.maxY = y
	}
	if mp.minZ > z {
		mp.minZ = z
	}
	if mp.maxZ < z {
		mp.maxZ = z
	}
	mp.values[Coord{x, y, z}] = value
}

func (mp *Map) get(x int, y int, z int) bool {
	value, exists := mp.values[Coord{x, y, z}]
	return exists && value
}

func (mp *Map) size() int {
	return len(mp.values)
}

func (mp *Map) getOccupiedNeighborsCount(x int, y int, z int) int {
	var count int
	// generate neighbors coordinates
	for _, dz := range []int { z-1, z, z+1 } {
		for _, dy := range []int { y-1, y, y+1 } {
			for _, dx := range []int { x-1, x, x+1 } {
				// fmt.Printf("  - (%d, %d, %d) : ", dx, dy, dz)
				if !(dx == x && dy == y && dz == z) {
					if mp.get(dx, dy, dz) {
						// fmt.Printf(" - (%d, %d, %d)", dx, dy, dz)
						// fmt.Println()
						count++
					} else {
						//fmt.Println("0")
					}
				} else {
					//fmt.Println("-")
				}
			}
		}
	}
	//fmt.Printf("Neighbors for (%d, %d, %d) : %d\n", x, y, z, count)
	return count
}

func (mp *Map) display() {
	fmt.Printf("x (%d, %d), y (%d, %d), z (%d ,%d)", mp.minX, mp.maxX, mp.minY, mp.maxY, mp.minZ, mp.maxZ)
	fmt.Println()
	for dz := mp.minZ; dz < mp.maxZ+1; dz++ {
		fmt.Printf("z = %d\n", dz)
		for dx := mp.minX; dx < mp.maxX+1; dx++ {
			fmt.Printf("%2d | ", dx)
			for dy := mp.minY; dy < mp.maxY+1; dy++ {
				if mp.get(dx, dy, dz) {
					fmt.Print("#")
				} else {
					fmt.Print(".")
				}
			}
			fmt.Println()
		}
	}
}


func run(s string) interface{} {

	// Your code goes here
	mp := createMap()
	for lineNb, line := range strings.Split(s, "\n") {
		// fmt.Print(line)
		if len(line) != 0 {
			for colNb, cell := range strings.Split(line, "") {
				// fmt.Printf("(%d, %d) : %v\n", lineNb, colNb, cell)
				if cell == "#" {
					mp.set(lineNb, colNb, 0, true)
				}
			}
		}
	}
	fmt.Println("Initial state")
	mp.display()

	fmt.Println("Tests")
	fmt.Println(mp.getOccupiedNeighborsCount(2,0,0))

	var nbRounds int = 6
	for r:= 0; r < nbRounds; r++ {
		newMap := createMap()
		for dz := mp.minZ-1; dz <= mp.maxZ+1; dz++ {
			for dy := mp.minY-1; dy <= mp.maxY+1; dy++ {
				for dx := mp.minX-1; dx <= mp.maxX+1; dx++ {
					nbOccupiedNeighbors := mp.getOccupiedNeighborsCount(dx, dy, dz)
					if mp.get(dx, dy, dz) {
						if nbOccupiedNeighbors == 2 || nbOccupiedNeighbors == 3 {
							// fmt.Printf("Set(%d, %d, %d)\n", dx, dy, dz)
							newMap.set(dx, dy, dz, true)
						}
					} else {
						if nbOccupiedNeighbors == 3 {
							// fmt.Printf("Set(%d, %d, %d)\n", dx, dy, dz)
							newMap.set(dx, dy, dz, true)
						}
					}
				}
			}
		}
		fmt.Println("End of round ", r+1)
		newMap.display()
		mp = newMap
	}
	return mp.size()
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	argsWithProg := os.Args
	var input []byte
	var err error
	if len(argsWithProg) > 1 {
		input,err = ioutil.ReadFile(argsWithProg[1])
		if err != nil {
			panic(err)
		}
	} else {
		// Read input from stdin
		input, err = ioutil.ReadAll(os.Stdin)
		if err != nil {
			panic(err)
		}
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
