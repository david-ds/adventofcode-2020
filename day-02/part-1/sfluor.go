package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	var policies = strings.Split(s, "\n")

	count := 0
	valid := 0
	for _, policy := range policies {
		mini, maxi, char, passwd := parsePolicy(policy)

		for idx := range passwd {
			if char == passwd[idx] {
				count += 1
			}

			if count > maxi {
				break
			}
		}

		//fmt.Printf("count: %d, mini: %d, maxi: %d, char: %s, passwd: %s\n", count, mini, maxi, string(char), passwd)

		if count >= mini && count <= maxi {
			valid += 1
		}

		count = 0
	}

	return valid
}

// parsePolicy returns lower, upper, char, password
func parsePolicy(policy string) (int, int, byte, string) {
	var mini, maxi int

	i := 0

	for ; policy[i] != '-'; i++ {
	}

	mini, _ = strconv.Atoi(policy[:i])

	j := i
	for ; policy[j] != ' '; j++ {
	}

	maxi, _ = strconv.Atoi(policy[i+1 : j])

	return mini, maxi, policy[j+1], policy[j+4:]
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
