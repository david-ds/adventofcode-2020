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

    return countPossibleRemoves(sortedNumbers, 1)
}

func countPossibleRemoves(numbers []int, startPoint int) int64 {
    // fmt.Printf("Possible removes of %v\n", numbers)
    if len(numbers) <= 1 {
        return 0
    }

    var count int64 = 1
    for i := startPoint; i < len(numbers)-1; i++ {
        
        previous := numbers[i-1]
        // current := numbers[i]
        next := numbers[i+1]

        if next - previous <= 3 {
            // current can be removed
            newNumbers := make([]int, len(numbers)-1)
            copy(newNumbers, numbers[0:i])
            copy(newNumbers[i:], numbers[i+1:])
            count += countPossibleRemoves(newNumbers, i)
        }
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
