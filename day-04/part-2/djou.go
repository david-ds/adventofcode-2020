package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"time"
)

func run(s string) interface{} {
	phase := 1
	valid := 0
	check := [7]int{0}
	end := len(s)

	for i, c := range s {
		if i + 1 == end {
			break
		}

		if phase == 4 {
			phase = 1
			continue
		}

		if phase == 5 {
			if s[i:i+2] == "\n\n" {
				phase = 4
			}
			continue
		}

		switch c {
		case '\n':
			if s[i+1] == '\n' {
				if validate(&check) {
					valid += 1
				}
				reset(&check)
				phase = 4
			} else {
				phase = 1
			}
			break
		case ' ':
			phase = 1
			break
		case ':':
			phase = 3
			break
		default:
			if phase != 1 {
				break
			}

			switch s[i:i+3] {
			case "byr":
				if i+8 <= end && checkByr(s[i+4: i+8]) {
					check[0] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "iyr":
				if i+8 <= end && checkIyr(s[i+4: i+8]) {
					check[1] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "eyr":
				if i+8 <= end && checkEyr(s[i+4: i+8]) {
					check[2] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "hgt":
				if i+9 <= end && checkHgt(s[i+4: i+9]) {
					check[3] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "hcl":
				if i+11 <= end && checkHcl(s[i+4: i+11]) {
					check[4] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "ecl":
				if i+7 <= end && checkEcl(s[i+4: i+7]) {
					check[5] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			case "pid":
				if i+14 <= end && checkPid(s[i+4: i+13], s[i+13]) {
					check[6] = 1
					phase = 2
				} else {
					reset(&check)
					phase = 5
				}
				break
			}
		}
	}

	// Last passport
	if validate(&check) {
		valid += 1
	}

	return valid
}

func checkByr(s string) bool {
	year, err := strconv.Atoi(s)
	if err != nil {
		return false
	}

	return year >= 1920 && year <= 2002
}

func checkIyr(s string) bool {
	year, err := strconv.Atoi(s)
	if err != nil {
		return false
	}

	return year >= 2010 && year <= 2020
}

func checkEyr(s string) bool {
	year, err := strconv.Atoi(s)
	if err != nil {
		return false
	}

	return year >= 2020 && year <= 2030
}

func checkHgt(s string) bool {
	if s[2:4] == "in" {
		hgt, err := strconv.Atoi(s[0:2])
		if err != nil {
			return false
		}
		return hgt >= 59 && hgt <= 76
	}
	if s[3:5] == "cm" {
		hgt, err := strconv.Atoi(s[0:3])
		if err != nil {
			return false
		}
		return hgt >= 150 && hgt <= 193
	}

	return false
}

func checkHcl(s string) bool {
	if s[0] != '#' {
		return false
	}
	for i := 1; i < 7; i ++ {
		if (s[i] < '0' || s[i] > '9') && (s[i] < 'a' || s[i] > 'f') {
			return false
		}
	}

	return true
}

func checkEcl(s string) bool {
	return s == "amb" || s == "blu" || s == "brn" || s == "gry" || s == "grn" || s == "hzl" || s == "oth"
}



func checkPid(s string, e uint8) bool {
	if e >= '0' && e <= '9' {
		return false
	}
	for _, c := range s {
		if c < '0' || c > '9' {
			return false
		}
	}

	return true
}

func reset(check *[7]int) {
	check[0] = 0
	check[1] = 0
	check[2] = 0
	check[3] = 0
	check[4] = 0
	check[5] = 0
	check[6] = 0
}

func validate(check *[7]int) bool {
	for _, i := range check {
		if i != 1 {
			return false
		}
	}

	return true
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
	// S'agirait pas de devoir trop réfléchir à la gestion de la termination ¯\_(ツ)_/¯.
	result := run(string(input) + "\n\n\n\n\n\n")

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
