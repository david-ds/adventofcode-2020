package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "regexp"
    "strconv"
    "strings"
	"time"
)

var hclRegex = regexp.MustCompilePOSIX("^#[0-9a-f]{6}$")
var eye_colors = map[string]int{
    "amb": 1,
    "blu": 1,
    "brn": 1,
    "gry": 1,
    "grn": 1,
    "hzl": 1,
    "oth": 1,
}

var pidRegex = regexp.MustCompilePOSIX("^[0-9]{9}$")

type PassportCandidate struct {
    byr string // (Birth Year)
    byrOK bool
    iyr string // (Issue Year)
    iyrOK bool
    eyr string // (Expiration Year)
    eyrOK bool
    hgt string // (Height)
    hgtOK bool
    hcl string // (Hair Color)
    hclOK bool
    ecl string // (Eye Color)
    eclOK bool
    pid string // (Passport ID)
    pidOK bool
    cid string // (Country ID)
}

func check4DigitInterval(value string, lower int, upper int) bool {
    if len(value) != 4 {
        return false
    }
    intValue, err := strconv.Atoi(value)
    return err == nil && intValue >= lower && intValue <= upper

}

func checkHeight(value string) bool {

    var result bool

    lgth := len(value)
    if lgth < 3 {
        return false
    }

    unit := string(value[lgth-2:])
    height, err := strconv.Atoi(value[:lgth-2])
    switch unit {
    case "in":
        result = err == nil && height >= 59 && height <= 76
    case "cm":
        result =  err == nil && height >= 150 && height <= 193
    default:
        result = false
    }
    return result
}

func (pc *PassportCandidate) isValid() bool {
    return pc.byrOK  &&
        pc.iyrOK &&
        pc.eyrOK &&
        pc.hgtOK &&
        pc.hclOK &&
        pc.eclOK &&
        pc.pidOK
}

func (pc *PassportCandidate) set(key string, value string) {
    switch key {
	case "byr":
		pc.byr = value
        pc.byrOK = check4DigitInterval(value, 1920, 2002)
	case "iyr":
		pc.iyr = value
        pc.iyrOK = check4DigitInterval(value, 2010, 2020)
	case "eyr":
		pc.eyr = value
        pc.eyrOK = check4DigitInterval(value, 2020, 2030)
	case "hgt":
		pc.hgt = value
        pc.hgtOK = checkHeight(value)
	case "hcl":
		pc.hcl = value
        pc.hclOK = hclRegex.MatchString(value)
	case "ecl":
		pc.ecl = value
        _, pc.eclOK = eye_colors[value]
	case "pid":
		pc.pid = value
        pc.pidOK = pidRegex.MatchString(value)
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
