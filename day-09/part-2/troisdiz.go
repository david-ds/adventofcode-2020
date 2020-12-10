package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "sort"
    "strconv"
    "strings"
	"time"
)

func validateNumber(toCheck int, previousOnes []int) bool {
    prevCopy := make([]int, len(previousOnes))
    copy(prevCopy, previousOnes)
    sort.Ints(prevCopy) 

    i := 0
    j := len(prevCopy) - 1

    sum := prevCopy[i] + prevCopy[j]

    for sum != toCheck && i < j {
        if sum > toCheck {
            j = j - 1
        } else {
            i = i + 1
        }
        sum = prevCopy[i] + prevCopy[j]
    }
    if sum != toCheck {
        return false
    }
    if prevCopy[i] == prevCopy[j] {
        return false
    }
    return true
}

var PREAMBLE_LENGTH int = 25

func findInvalidNumber(numbers []int) (int, int) {

    for idx := PREAMBLE_LENGTH; idx < len(numbers); idx++ {
        ok := validateNumber(numbers[idx], numbers[idx-PREAMBLE_LENGTH:idx])
        if !ok {
            return idx, numbers[idx]
        }
    }
    return -1, -1
}

func findSumRange(numbers []int, invalidNb int) (int, int) {
    for i := 0; i < len(numbers)-1; i++ {
        sum := 0
        for j:= i; j < len(numbers)-1; j++ {
            sum += numbers[j]
            if sum == invalidNb {
                return i, j
            }
            if sum > invalidNb {
                break
            }
        }
    }
    return -1, -1
}

func run(s string) interface{} {
    inputStr := strings.Split(s, "\n")
    var numbers []int = make([]int, len(inputStr))

    for idx, val := range inputStr {
        valInt, _ := strconv.Atoi(val)
        numbers[idx] = valInt
    }
     
    _, invalidNb := findInvalidNumber(numbers)

    // fmt.Printf("Invalid Nb : %d\n", invalidNb)

    minIdx, maxIdx := findSumRange(numbers, invalidNb)
    minVal := numbers[minIdx]
    maxVal := numbers[minIdx]
    for i := minIdx; i <= maxIdx; i++ {
        if numbers[i] < minVal {
            minVal = numbers[i]
        }
        if numbers[i] > maxVal {
            maxVal = numbers[i]
        }
    }
    return minVal + maxVal
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
