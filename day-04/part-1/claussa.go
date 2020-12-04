package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	valid := 0
	i := 0
	lines := strings.Split(s, "\n")
	for index, line := range lines {
		if line == "" {
			if validatePassport(strings.Join(lines[i:index], " ")) {
				valid += 1
			}
			i = index + 1
		}
	}
	if validatePassport(strings.Join(lines[i:], " ")) {
		valid += 1
	}
	return valid
}

// Password is a string of all the field separate by spaces
func validatePassport(password string) bool {
	fields := strings.Split(password, " ")
	requiredFields := 0
	// 0: byr  1: iyr  2: eyr  3: hgt  4:hcl  5: ecl  6:pid
	for _, field := range fields {
		if field[0:3] != "cid" {
			requiredFields += 1
		}
	}
	return requiredFields == 7
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
