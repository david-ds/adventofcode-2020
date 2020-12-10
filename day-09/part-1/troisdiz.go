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


func run(s string) interface{} {
    inputStr := strings.Split(s, "\n")
    var numbers []int = make([]int, len(inputStr))

    for idx, val := range inputStr {
        valInt, _ := strconv.Atoi(val)
        numbers[idx] = valInt
    }

    for idx := 25; idx < len(numbers); idx++ {
        ok := validateNumber(numbers[idx], numbers[idx-25:idx])
        if !ok {
            return numbers[idx]
        }
    }
    return -1
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
