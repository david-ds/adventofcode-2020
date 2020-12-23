package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"time"
)

type cup struct {
	Label int
	Next  *cup
}

func run(s string) int {
	// Prepare cup reverse-lookup map
	mapping := make(map[int]*cup)

	// Parse first character of the input
	label, _ := strconv.Atoi(string(s[0]))
	current := &cup{
		Label: label,
		Next:  nil,
	}
	mapping[label] = current
	previous := current

	// Parse the remaining input
	for _, char := range s[1:] {
		label, _ = strconv.Atoi(string(char))
		next := &cup{
			Label: label,
			Next:  nil,
		}
		mapping[label] = next
		previous.Next = next
		previous = next
	}

	// Append the many new cups
	for i := 10; i <= 1000000; i++ {
		next := &cup{
			Label: i,
			Next:  nil,
		}
		mapping[i] = next
		previous.Next = next
		previous = next
	}
	previous.Next = current

	for i := 0; i < 10000000; i++ {
		// Extract the three cups that are immediately clockwise of current
		cup1, cup2, cup3 := current.Next, current.Next.Next, current.Next.Next.Next

		// Detach cups from the circle
		current.Next = cup3.Next

		// Find destination cup
		destinationLabel := current.Label
		for destinationLabel == current.Label || destinationLabel == cup1.Label || destinationLabel == cup2.Label || destinationLabel == cup3.Label {
			destinationLabel--
			if destinationLabel <= 0 {
				destinationLabel = 1000000
			}
		}
		destination, _ := mapping[destinationLabel]

		// Attach cups back in the circle
		cup3.Next = destination.Next
		destination.Next = cup1

		current = current.Next
	}

	// Build expected result
	return mapping[1].Next.Label * mapping[1].Next.Next.Label
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
