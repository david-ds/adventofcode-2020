package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Field struct {
	ranges []Range
	name string
	rank int
}

type Range struct {
	low int
	high int
}

func run(s string) interface{} {
	input := strings.Split(s, "\n\n")

	fields := parseFields(strings.Split(input[0], "\n"))
	myPassport := strings.Split(strings.Split(input[1], "\n")[1], ",") // lol
	l := len(myPassport)
	passports := strings.Split(input[2], "\n")[1:]

	// Matrice de vérification
	check := make([][]bool, l)
	for i, _ := range check {
		check[i] = make([]bool, l)
		for j, _ := range check[i] {
			check[i][j] = true
		}
	}

	for _, passport := range passports {
		exclude := false
		splitPassword := strings.Split(passport, ",")
		for _, valStr := range splitPassword {
			valInt, _ := strconv.Atoi(valStr)
			if !isInRange(&fields, valInt) {
				exclude = true
				break
			}
		}

		if !exclude {
			for i, valStr := range splitPassword {
				valInt, _ := strconv.Atoi(valStr)
				for j, field := range fields {
					includes := false
					for _, r := range field.ranges {
						if r.includes(valInt) {
							includes = true
						}
					}
					if !includes {
						check[i][j] = false
					}
				}
			}
		}
	}

	k := 0
	for {
		var rowA *[]bool
		var rowB *[]bool
		var valueIndex int

		for i, _ := range check {
			rowSize := rowSize(&check[i])
			if rowSize == l - k {
				rowA = &check[i]
				valueIndex = i
			}
			if rowSize == l - k - 1 {
				rowB = &check[i]
			}
		}

		var fieldIndex int
		for i, val := range diffRows(rowA, rowB) {
			if val {
				fieldIndex = i
				break
			}
		}

		fields[fieldIndex].rank = valueIndex

		k++
		if k == l - 1 {
			break
		}
	}

	// Last row
	for i, row := range check {
		if rowSize(&row) == 1 {
			for j, val := range row {
				if val {
					fields[j].rank = i
					break
				}
			}
		}
	}

	tot := 1
	for _, field := range fields {
		if field.name[:3] == "dep" {
			fact, _ := strconv.Atoi(myPassport[field.rank])
			tot *= fact
		}
	}

	return tot
}

func parseFields(fieldInputs []string) []Field {
	fields := make([]Field, len(fieldInputs))
	for k, field := range fieldInputs {
		info := strings.Split(field, ": ")

		rangeStrings := strings.Split(info[1], " or ")
		ranges := make([]Range, len(rangeStrings))
		for i, r := range rangeStrings {
			lowHigh := strings.Split(r, "-")
			low, _ := strconv.Atoi(lowHigh[0])
			high, _ := strconv.Atoi(lowHigh[1])
			ranges[i] = Range{
				low: low,
				high: high,
			}
		}

		fields[k] = Field {
			name: info[0],
			ranges: ranges,
		}
	}

	return fields
}

func isInRange(fields *[]Field, value int) bool {
	for _,  field := range *fields {
		for _, r := range field.ranges {
			if r.includes(value) {
				return true
			}
		}
	}

	return false
}

func rowSize(row *[]bool) int {
	tot := 0
	for _, cell := range *row {
		if cell {
			tot += 1
		}
	}

	return tot
}

func diffRows(rowA *[]bool, rowB *[]bool) []bool {
	row := make([]bool, len(*rowA))
	for i, _ := range row {
		row[i] = (*rowA)[i] && !(*rowB)[i]
	}

	return row
}


func (r Range) includes(value int) bool {
	return value >= r.low && value <= r.high
}

func printCheck(check [][]bool) {
	l := len(check)
	checkStr := make([][]string, l)
	for i, _ := range check {
		checkStr[i] = make([]string, l)
		for j, val := range check[i] {
			if val {
				checkStr[i][j] = "1"
			} else {
				checkStr[i][j] = "0"
			}
		}
	}

	println("==============")
	for _, row := range checkStr {
		println(strings.Join(row, ","))
	}
	println("==============")
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
