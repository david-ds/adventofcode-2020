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
    var minI, maxI, minJ, maxJ int
    if i == 0 {
        minI = 0
    } else {
        minI = i - 1
    }
    if i == sizeX - 1 {
        maxI = i
    } else {
        maxI = i + 1
    }
    if j == 0 {
        minJ = 0
    } else {
        minJ = j - 1
    }
    if j == sizeY - 1 {
        maxJ = j
    } else {
        maxJ = j + 1
    }
    // fmt.Printf("debug(%d, %d) => minI = %d; maxI = %d, minJ = %d, maxJ = %d\n", i, j, minI, maxI, minJ, maxJ)
    for x := minI; x <= maxI; x++ {
        for y := minJ; y <= maxJ; y++ {
            if x != i || y != j {
                if (*grid)[x][y] == 1 {
                    // fmt.Printf("    (%d, %d) = 1\n", x, y)
                    count += 1
                } else {
                    // fmt.Printf("    (%d, %d) = -1/0\n", x, y)
                }
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
                if occupiedAround(&grid, sizeX, sizeY, i, j) >= 4 {
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
    // displayGrid(&grid)

    newGrid := grid
    changeHappen := true
    count := 0
    for changeHappen {
        newGrid, changeHappen = playRound(newGrid, sizeX, sizeY)
        // fmt.Print("\n\n\n")
        // fmt.Printf("occ(0, 2) : %d\n", occupiedAround(&newGrid, sizeX, sizeY, 0, 2))
        // fmt.Printf("occ(2, 0) : %d\n", occupiedAround(&newGrid, sizeX, sizeY, 2, 0))
        // displayGrid(&newGrid)

        count += 1
        /*if count == 2 {
            changeHappen = false
        }*/
    }

    // fmt.Printf("\nAfter %d rounds\n\n", count)
    // displayGrid(&newGrid)

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
