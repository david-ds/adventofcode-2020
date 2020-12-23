package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type cup struct {
	Label int
	Prev  *cup
	Next  *cup
}

func (c cup) String() string {
	var buffer strings.Builder
	current := c

	for current.Prev.Label != 1 {
		current = *current.Next
	}

	for current.Label != 1 {
		buffer.WriteString(strconv.Itoa(current.Label))
		current = *current.Next
	}

	return buffer.String()
}

func run(s string, n int) string {
	// Parse first character of the input
	label, _ := strconv.Atoi(string(s[0]))
	current := &cup{
		Label: label,
		Prev:  nil,
		Next:  nil,
	}
	previous := current

	// Parse the remaining input
	for _, char := range s[1:] {
		label, _ = strconv.Atoi(string(char))
		next := &cup{
			Label: label,
			Prev:  previous,
			Next:  nil,
		}
		previous.Next = next
		previous = next
	}
	current.Prev = previous
	previous.Next = current

	for i := 0; i < n; i++ {
		// Extract the three cups that are immediately clockwise of current
		cup1, cup2, cup3 := current.Next, current.Next.Next, current.Next.Next.Next

		// Detach cups from the circle
		current.Next = cup3.Next
		cup3.Next.Prev = current

		// Find destination cup
		labels := map[int]struct{}{
			current.Label: {},
			cup1.Label:    {},
			cup2.Label:    {},
			cup3.Label:    {},
		}
		destinationLabel := current.Label
		for _, ok := labels[destinationLabel]; ok; _, ok = labels[destinationLabel] {
			destinationLabel = (destinationLabel+7)%9 + 1
		}
		destination := cup3.Next
		for destination.Label != destinationLabel {
			destination = destination.Next
		}

		// Attach cups back in the circle
		cup3.Next = destination.Next
		destination.Next.Prev = cup3
		cup1.Prev = destination
		destination.Next = cup1

		current = current.Next
	}

	return current.String()
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
	result := run(string(input), 100)

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
