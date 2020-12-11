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

func puzzle(numbers []int) int64 {
    sort.Ints(numbers)
   
    sortedNumbers := make([]int, len(numbers)+2)
    sortedNumbers[0] = 0
    copy(sortedNumbers[1:], numbers)
    sortedNumbers[len(sortedNumbers)-1] = sortedNumbers[len(sortedNumbers)-2] + 3

    var diffs []int

    for i := 1; i < len(sortedNumbers); i++ {
        previous := sortedNumbers[i-1]
        current := sortedNumbers[i]
        diffs = append(diffs, current - previous)
    }

    return 1 + countPossibleRemoves(diffs)
}

func countPossibleRemoves(numbers []int) int64 {
    fmt.Printf("count from diffs : %v\n", numbers)
    if len(numbers) <= 1 {
        return 0
    }
    var count int64 = 0
    for i := 1; i < len(numbers); i++ {
        previous := numbers[i-1]
        current := numbers[i]

        if (current == 1 && previous == 2) || (current == 2 && previous == 1) {
            
            newNumbers := make([]int, len(numbers)-1)
            if i > 2 {
                copy(newNumbers, numbers[:i-1])
            }
            newNumbers[i-1] = previous + current
            copy(newNumbers[i:], numbers[i:])
            count += 1
            //fmt.Printf("Merge %d and %d at current = %d\n", previous, current, i)
            count += countPossibleRemoves(newNumbers)
        }
    }
    for i := 2; i < len(numbers); i++ {
        previous := numbers[i-1]
        current := numbers[i]

        if (current == 1 && previous == 2) || (current == 2 && previous == 1) {
            
            newNumbers := make([]int, len(numbers)-1)
            if i > 2 {
                copy(newNumbers, numbers[:i-1])
            }
            newNumbers[i-1] = previous + current
            copy(newNumbers[i:], numbers[i:])
            //fmt.Printf("Merge %d and %d at current = %d\n", previous, current, i)
            count += countPossibleRemoves(newNumbers)
        }
    }
    if count == 1 {
        fmt.Printf("No more remove : %v\n", numbers)
    }
    return count
}

func run(s string) interface{} {
    inputStr := strings.Split(s, "\n")
    var numbers []int = make([]int, len(inputStr))

    for idx, val := range inputStr {
        valInt, _ := strconv.Atoi(val)
        numbers[idx] = valInt
    }

    return puzzle(numbers)
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
