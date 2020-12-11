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

func puzzle(numbers []int) (int, int) {
    sort.Ints(numbers)
   
    sortedNumbers := make([]int, len(numbers)+2)
    sortedNumbers[0] = 0
    copy(sortedNumbers[1:], numbers)
    sortedNumbers[len(sortedNumbers)-1] = sortedNumbers[len(sortedNumbers)-2] + 3

    var count1, count3 int

    for i := 1; i < len(sortedNumbers); i++ {

        previous := sortedNumbers[i-1]
        current := sortedNumbers[i]
        diff := current - previous
        switch diff {
        case 1:
            count1 += 1
        case 2:
        case 3:
            count3 += 1
        default:
            fmt.Printf("Diff is %d at pos %d\n", diff, i)
        }
    }

    return count1, count3
}

func run(s string) interface{} {
    inputStr := strings.Split(s, "\n")
    var numbers []int = make([]int, len(inputStr))

    for idx, val := range inputStr {
        valInt, _ := strconv.Atoi(val)
        numbers[idx] = valInt
    }

    count1, count3 := puzzle(numbers)
    return count1 * count3
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
