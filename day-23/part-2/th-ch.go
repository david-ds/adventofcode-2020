package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

const nbCups = 1000000   // 9
const nbMoves = 10000000 // 10

func run(s string) interface{} {
	// linked list where index = cup-1 and value is the next cup
	// e.g. cups "1 3 2" are represented as [3 1 2]
	cups := [nbCups]int{}

	// Fill in values from s
	for c := range s {
		cup := int(s[c] - '0')
		nextCup := int(s[(c+1)%len(s)] - '0')
		cups[cup-1] = nextCup
	}

	// Fill in missing values
	if nbCups > len(s) {
		lastCup := int(s[len(s)-1] - '0')
		firstCup := cups[lastCup-1]

		for cup := len(s); cup < nbCups; cup++ {
			cups[cup] = cup + 2
		}

		cups[lastCup-1] = (len(s) + 1) % nbCups
		cups[nbCups-1] = firstCup
	}

	minCup := 1
	maxCup := nbCups
	currentCup := int(s[0] - '0')

	for move := 1; move <= nbMoves; move++ {
		// Pick 3 cups
		pickedCups := [3]int{
			cups[currentCup-1],
			cups[cups[currentCup-1]-1],
			cups[cups[cups[currentCup-1]-1]-1],
		}
		cupAfterPickedCups := cups[cups[cups[cups[currentCup-1]-1]-1]-1]

		// Destination cup
		destinationCup := currentCup - 1
		for {
			if destinationCup < minCup {
				destinationCup = maxCup
			}
			if destinationCup != pickedCups[0] &&
				destinationCup != pickedCups[1] &&
				destinationCup != pickedCups[2] {
				break
			}
			destinationCup--
		}

		// Move picked cups
		cups[destinationCup-1],
			cups[pickedCups[2]-1],
			cups[currentCup-1] = pickedCups[0], cups[destinationCup-1], cupAfterPickedCups

		// Update current cup
		currentCup = cups[currentCup-1]
	}

	// Multiply the 2 cups after cup 1
	return cups[0] * cups[cups[0]-1]
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
