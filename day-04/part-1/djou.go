package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s string) interface{} {
	phase := 1
	valid := 0
	check := [7]int{0}

	for i, c := range s {

		if phase == 4 {
			phase = 1
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
				check[0] = 1
				phase = 2
				break
			case "iyr":
				check[1] = 1
				phase = 2
				break
			case "eyr":
				check[2] = 1
				phase = 2
				break
			case "hgt":
				check[3] = 1
				phase = 2
				break
			case "hcl":
				check[4] = 1
				phase = 2
				break
			case "ecl":
				check[5] = 1
				phase = 2
				break
			case "pid":
				check[6] = 1
				phase = 2
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
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
