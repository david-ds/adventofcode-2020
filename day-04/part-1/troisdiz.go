package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strings"
	"time"
)

type PassportCandidate struct {
    byr string // (Birth Year)
    iyr string // (Issue Year)
    eyr string // (Expiration Year)
    hgt string // (Height)
    hcl string // (Hair Color)
    ecl string // (Eye Color)
    pid string // (Passport ID)
    cid string // (Country ID)
}

func (pc *PassportCandidate) isValid() bool {
    return (pc.byr != "") &&
        (pc.iyr != "") &&
        (pc.eyr != "") &&
        (pc.hgt != "") &&
        (pc.hcl != "") &&
        (pc.ecl != "") &&
        (pc.pid != "")
}

func (pc *PassportCandidate) set(key string, value string) {
    switch key {
	case "byr":
		pc.byr = value
	case "iyr":
		pc.iyr = value
	case "eyr":
		pc.eyr = value
	case "hgt":
		pc.hgt = value
	case "hcl":
		pc.hcl = value
	case "ecl":
		pc.ecl = value
	case "pid":
		pc.pid = value
	case "cid":
		pc.cid = value
	default:
        fmt.Printf("Unknown key %s (value : %s)\n", key, value)
	}
}

func parseData(input string) []PassportCandidate {
       
    var result [] PassportCandidate

    for _, pcLines := range strings.Split(input, "\n\n") {

        var pc PassportCandidate = PassportCandidate { }

        for _, listOfkvPAir := range strings.Split(pcLines, "\n") {
            for _, kvPair := range strings.Split(listOfkvPAir, " ") {
                kv := strings.Split(kvPair, ":")
                pc.set(kv[0], kv[1])
            }
        }
        result = append(result, pc)
    }
    return result
}

func puzzle(pcList []PassportCandidate) int {
    var count int
    for _, pc := range pcList {
        if pc.isValid() {
            count += 1
        }
    }
    return count
}

func run(s string) interface{} {
	// Your code goes here
    data := parseData(s)
    return puzzle(data)
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
