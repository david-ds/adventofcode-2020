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

func puzzle2(input []int, target int) (int, int) {

    sorted_input := input

    // fmt.Printf("    Puzzle2 Size of data %d, first elt : %d, last elt : %d, target : %d\n", len(sorted_input), sorted_input[0], sorted_input[len(sorted_input)-1], target)

    i := 0
    j := len(sorted_input) - 1

    sum := sorted_input[i] + sorted_input[j]

    for sum != target && i < j {
        // fmt.Printf("Sum = %d | %d -- %d\n", sum, sorted_input[i], sorted_input[j])
        if sum > target {
            j = j - 1
        } else {
            i = i + 1
        }
        sum = sorted_input[i] + sorted_input[j]
    }
    int_i := sorted_input[i]
    int_j := sorted_input[j]
    if int_i + int_j == target {
        // fmt.Printf("    Target = %d, Sum = %d | %d -- %d (%d, %d)\n", target, sum, sorted_input[i], sorted_input[j], i, j)
        return i, j
    } else {
        // fmt.Printf("    Target = %d, Sum = %d | %d -- %d (%d, %d)\n", target, sum, sorted_input[i], sorted_input[j], -1, -1)
        return -1, -1
    }
}

func puzzle(input []int, target int) int {
  
    sorted_input := input
    sort.Ints(sorted_input)

    // fmt.Printf("Size of sorted data %d, first elt : %d, last elt : %d\n", len(sorted_input), sorted_input[0], sorted_input[len(sorted_input)-1])

    i := 0
    j := 1
    k := len(sorted_input) - 1

    sum := 0

    for j < k {
        ti, tj := puzzle2(sorted_input[i:k], target - sorted_input[k])
        if ti == -1 {
            // fmt.Printf("No ok sum for k = %d\n", k)
            k = k - 1
        } else {
            j = i + tj
            i = i + ti
            sum = sorted_input[i] + sorted_input[j] + sorted_input[k]
            // fmt.Printf("Sum = %d | %d -- %d -- %d (%d, %d, %d)\n", sum, sorted_input[i], sorted_input[j], sorted_input[k], i, j, k)
            break
        }
    }

    // fmt.Printf("Sum = %d | %d -- %d -- %d (%d, %d, %d)\n", sum, sorted_input[i], sorted_input[j], sorted_input[k], i, j, k)
    if sum == target {
        return sorted_input[i] * sorted_input[j] * sorted_input[k]
    } else {
        return -1
    }
}

func parseData(input string) []int {

    var data []int

    for _, line := range strings.Split(input, "\n") {
		parsed, _ := strconv.Atoi(line)
        if parsed != 0 {
            data = append(data, parsed)
        }
	}

    return data
}

func run(s string) interface{} {
    data := parseData(s)
    // fmt.Printf("Size of data %d, first elt : %d, last elt : %d\n", len(data), data[0], data[len(data)-1])
    sol := puzzle(data, 2020)
    return sol

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
