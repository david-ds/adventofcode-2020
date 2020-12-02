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
    firstPlace int
    secondPlace int
    password string
}

func parseData(input string) []Entry {
    var entry_list []Entry


    for _, line := range strings.Split(input, "\n") {

        elts := strings.Split(line, " ")
        placesStr := strings.Split(elts[0], "-")
        min, _ := strconv.Atoi(placesStr[0])
        max, _ := strconv.Atoi(placesStr[1])
        letter := elts[1][0:1]

        entry := Entry { 
            letter: letter,
            firstPlace: min,
            secondPlace: max,
            password: elts[2],
        }
        entry_list = append(entry_list, entry)
	}
    return entry_list
}

func validateLetterInPassword(password string, letter string, position int) bool {
    index := position - 1
    if index < len(password) {
        if string(password[index]) == letter {
            return true
        }
    }
    return false
}

func validateEntry(entry Entry) bool {

    firstPlaceTest := validateLetterInPassword(entry.password, entry.letter, entry.firstPlace)
    secondPlaceTest := validateLetterInPassword(entry.password, entry.letter, entry.secondPlace)

    return firstPlaceTest != secondPlaceTest
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
