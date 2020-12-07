package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strings"
	"time"
)

func decodeWithLetter(inputStr string, lowLetter string, upLetter string, nbOfItems int) int {

    lowerBound := 0
    upperBound := nbOfItems -1
    for _, letter := range inputStr {
        midLimit := lowerBound + (upperBound + 1 - lowerBound) / 2
        if string(letter) == lowLetter {
            upperBound = midLimit -1
        } else {
            lowerBound = midLimit
        }
    }
    return lowerBound
}

func decodeRowCol(input string) (int, int) {
    row := decodeWithLetter(input[0:7], "F", "B", 128)
    col := decodeWithLetter(input[7:10], "L", "R", 8)
    return row, col
}

func aroundCoords(row int, col int) (int, int, int, int) {
    if col > 0 && col < 7 {
        return row, col-1, row, col+1
    } else if col == 0 {
        return row-1, 7, row, 1
    } else if col == 7 {
        return row, 6, row+1, 0
    } else {
        return -1, -1, -1, -1
    }
}

func sitsOccupied(planeSits map[int]map[int]int, row int, col int) bool {
    rowMap, ok := planeSits[row]
    if ok {
        _, ok := rowMap[col]
        return ok
    }
    return false
}

func run(s string) interface{} {

    // maxSitId := 0
    planeSits := make(map[int]map[int]int)
    for i:= 0; i < 128; i++ {
        planeSits[i] = make(map[int]int)
        for j:= 0; j < 8; j++ {
            planeSits[i][j] = 1
        } 
    }
    for _, sit := range strings.Split(s, "\n") {
        row, col := decodeRowCol(sit)
        rowMap := planeSits[row]
        delete(rowMap, col)
        if len(rowMap) == 0 {
            delete(planeSits, row)
        }
    }
    delete(planeSits, 0)
    delete(planeSits, 127)
    var rowRes, colRes int
    for row := range planeSits {
        rowMap := planeSits[row]
        if len(rowMap) == 1 {
            var col int
            for c := range rowMap {
                col = c
            }
            //fmt.Printf("Sits  %d : \n  - %v\n  - %v\n  - %v\n", row, planeSits[row-1], planeSits[row], planeSits[row+1])
            prevRow, prevCol, nextRow, nextCol := aroundCoords(row, col)
            if !sitsOccupied(planeSits, prevRow, prevCol) && !sitsOccupied(planeSits, nextRow, nextCol) {
                rowRes = row
                colRes = col
                break
            }
        }
    }
    return rowRes * 8 + colRes
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
