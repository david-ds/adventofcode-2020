package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strconv"
    "strings"
	"time"
)

type Entry struct {
    letter string
    minCount int
    maxCount int
    password string
}

func parseData(input string) []Entry {
    var entry_list []Entry


    for _, line := range strings.Split(input, "\n") {

        elts := strings.Split(line, " ")
        minMaxStr := strings.Split(elts[0], "-")
        min, _ := strconv.Atoi(minMaxStr[0])
        max, _ := strconv.Atoi(minMaxStr[1])
        letter := elts[1][0:1]

        entry := Entry { 
            letter: letter,
            minCount: min,
            maxCount: max,
            password: elts[2],
        }
        entry_list = append(entry_list, entry)
	}
    return entry_list
}

func validateEntry(entry Entry) bool {
    letterCount := 0

    for _, letter := range entry.password {
       if string(letter) == entry.letter {
           letterCount += 1
       }
    }
    return entry.minCount <= letterCount && letterCount <= entry.maxCount
}


func puzzle(entries []Entry) int {
    validated := 0
    for _, entry := range entries {
        if validateEntry(entry) {
            validated += 1
        }
    }
    // fmt.Printf("Result : %d\n", validated)
    return validated
}

func run(s string) interface{} {
    entries := parseData(s)
    //fmt.Printf("Entries count : %d\n", len(entries))
    //fmt.Printf("Entry[0] : %v\n", entries[0])
    return puzzle(entries)
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
