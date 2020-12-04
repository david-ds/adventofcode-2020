package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
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
		switch key, field := field[0:3], field[4:]; key {
		case "byr":
			if validateByr(field) {
				requiredFields += 1
			}
		case "iyr":
			if validateIyr(field) {
				requiredFields += 1
			}
		case "eyr":
			if validateEyr(field) {
				requiredFields += 1
			}
		case "hgt":
			if validateHgt(field) {
				requiredFields += 1
			}
		case "hcl":
			if validateHcl(field) {
				requiredFields += 1
			}
		case "ecl":
			if validateEcl(field) {
				requiredFields += 1
			}
		case "pid":
			if validatePid(field) {
				requiredFields += 1
			}
		}
	}
	return requiredFields == 7
}

func validatePid(field string) bool {
	if len(field) != 9 {
		return false
	}
	_, err := strconv.Atoi(field)
	return err == nil
}

func validateEcl(field string) bool {
	if len(field) != 3 {
		return false
	}
	colors := [7]string{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
	for _, color := range colors {
		if color == field {
			return true
		}
	}
	return false
}

func validateHcl(field string) bool {
	if field[0] != '#' {
		return false
	}
	_, err := strconv.ParseUint(field[1:], 16, 64)
	return err == nil
}

func validateHgt(field string) bool {
	if len(field) < 3 {
		return false
	}
	min, max := 0, 0
	lenNumber := 0
	lenInput := len(field)
	if field[lenInput-2:] == "cm" {
		min, max = 150, 193
		lenNumber = 3
	} else if field[lenInput-2:] == "in" {
		min, max = 59, 76
		lenNumber = 2
	} else {
		return false
	}
	v, err := strconv.Atoi(field[:lenNumber])
	if err != nil {
		return false
	}
	return v >= min && v <= max
}

func validateEyr(field string) bool {
	v, err := strconv.Atoi(field)
	if err != nil {
		return false
	}
	return v >= 2020 && v <= 2030
}

func validateIyr(field string) bool {
	v, err := strconv.Atoi(field)
	if err != nil {
		return false
	}
	return v >= 2010 && v <= 2020
}

func validateByr(field string) bool {
	v, err := strconv.Atoi(field)
	if err != nil {
		return false
	}
	return v >= 1920 && v <= 2002
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
