package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Condition struct {
	busId int
	offset int
}

func run(s string) interface{} {
	input := strings.Split(s, "\n")
	inputIds := strings.Split(input[1], ",")
	n := 1
	var conditions []Condition
	for i, val := range inputIds {
		if val == "x" {
			continue
		}
		busId, _ := strconv.Atoi(val)
		n *= busId
		conditions = append(conditions, Condition{busId: busId, offset: -i})
	}

	sol := 0
	for _, condition := range conditions {
		// Credits to enizor, parce que je bitais pas ce que je faisais
		ni := n / condition.busId
		// Credits to enizor, parce que je bitais pas ce que je faisais
		_, u, _ := euclide(ni, condition.busId)

		// Credits to enizor, parce que je bitais pas ce que je faisais
		ei := u * ni
		// Credits to enizor, parce que je bitais pas ce que je faisais
		sol += ei * condition.offset
	}

	for sol < 0 {
		sol += n
	}

	return sol % n
}

// Credits to enizor, parce que je bitais pas ce que je faisais
func euclide(a int, b int) (int, int, int) {
	if b == 0 {
		return a, 1, 0
	}
	d, u, v := euclide(b, a % b)
	return d, v, u - (a/b)*v
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
