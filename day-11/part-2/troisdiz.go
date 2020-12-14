package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strings"
	"time"
)

func parseData(input string) ([][]int, int, int) {

    var result [][]int
    for _, line := range strings.Split(input, "\n") {
        resultLine := make([]int, len(line))
        for i, seat := range line {
            switch string(seat) {
            case ".":
                resultLine[i] = -1
            case "L":
                resultLine[i] = 0
            case "#":
                resultLine[i] = 1
            }
        }
        result = append(result, resultLine)
    }
    return result, len(result), len(result[0])
}

func occupiedAround(grid *[][]int, sizeX int, sizeY int, i int, j int) int {
    var count int

    var directions =  map[string][]int{
        "N": { -1, 0 },
        "NE": { -1, 1 },
        "E": { 0, 1 },
        "SE": { 1, 1 },
        "S": { 1, 0 },
        "SW": { 1, -1 },
        "W": { 0, -1 },
        "NW": { -1, -1 },
    }

    // fmt.Printf("Debug occ(%d, %d) \n", i, j)
    for key := range directions {
        x:= i
        y := j

        for {
            incrX := directions[key][0]
            x += incrX
            incrY := directions[key][1]
            y += incrY

            // fmt.Printf("    %v: x = %d (%d), y = %d (%d) | ", key, x, incrX, y, incrY)
            if x < 0 || x >= sizeX || y < 0 || y >= sizeY {
                // border reached
                // fmt.Printf("Border\n")
                break
            }
            // fmt.Printf(" grid = %d\n", (*grid)[x][y])
            if (*grid)[x][y] == 1 {
                count += 1
                break
            }
            if (*grid)[x][y] == 0 {
                break
            }
        }
    }
    return count
}

func playRound(grid [][]int, sizeX int, sizeY int) ([][]int, bool) {
    
    var changeOccurred bool

    result := make([][]int, sizeX)
    for i, oldLine := range grid {
        //fmt.Println("Loop line")
        result[i] = make([]int, sizeY)
        for j, oldSeat := range oldLine {
            //fmt.Println("Loop cell")
            switch oldSeat {
            case -1:
                result[i][j] = -1
            case 0:
                if occupiedAround(&grid, sizeX, sizeY, i, j) == 0 {
                    result[i][j] = 1
                    changeOccurred = true
                } else {
                    result[i][j] = 0
                }
            case 1:
                if occupiedAround(&grid, sizeX, sizeY, i, j) >= 5 {
                    result[i][j] = 0
                    changeOccurred = true
                } else {
                    result[i][j] = 1
                }
            }
        }
    }
    return result, changeOccurred
}

func countOccupied(grid *[][]int) int {
    count := 0
    for _, line :=  range *grid {
        for _, seat := range line {
            switch seat {
            case 1:
                count += 1
            }
        }
    }
    return count
}


func displayGrid(grid *[][]int) {
    for _, line :=  range *grid {
        for _, seat := range line {
            switch seat {
            case -1:
                fmt.Print(".")
            case 0:
                fmt.Print("L")
            case 1:
                fmt.Print("#")
            }
        }
        fmt.Println()
    }
    fmt.Println()
}

func run(s string) interface{} {
	// Your code goes here
    grid, sizeX, sizeY := parseData(s)
    //displayGrid(&grid)

    newGrid := grid
    changeHappen := true
    count := 0
    for changeHappen {

        newGrid, changeHappen = playRound(newGrid, sizeX, sizeY)

        count += 1
    }
    //fmt.Printf("\nAfter %d rounds\n\n", count)

    return countOccupied(&newGrid) 
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
