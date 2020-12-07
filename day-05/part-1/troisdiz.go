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

func decodeId(input string) int {
    row := decodeWithLetter(input[0:7], "F", "B", 128)
    col := decodeWithLetter(input[7:10], "L", "R", 8)
    return row * 8 + col
}

func run(s string) interface{} {

    maxSitId := 0
    for _, sit := range strings.Split(s, "\n") {
        sitId := decodeId(sit)
        if sitId > maxSitId {
            maxSitId = sitId
        }
    }
    return maxSitId
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
