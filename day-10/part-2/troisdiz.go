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

    return countPossibleRemoves(sortedNumbers)
}

func countPossibleRemoves(numbers []int) int64 {
    if len(numbers) <= 1 {
        return 0
    }

    var count int64 = 1
    var currentLength int64

    var count1, count7 int64

    for i := 1; i < len(numbers)-1; i++ {
        
        previous := numbers[i-1]
        next := numbers[i+1]

        diff := next - previous

        if diff == 2 {
            currentLength += 1
        } else {
            if currentLength == 1 || currentLength == 2 {
                count1 += currentLength 
                count *= (2 * currentLength)
            } else if currentLength == 3 {
                count7 += 1
                count *= 7
            }
            currentLength = 0
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
