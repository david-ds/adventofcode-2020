package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

// To compute x^y under modulo m
func power(x uint64, y uint64, m uint64) uint64 {
	if y == 0 {
		return 1
	}
	p := power(x, y/2, m) % m
	p = (p * p) % m

	if y%2 == 0 {
		return p
	}
	return (x * p) % m
}

// Function to find modular inverse of a under modulo m
// Assumption: m is prime
func modInverse(a uint64, m uint64) uint64 {
	return power(a, m-2, m)
}

// k is size of num[] and rem[].  Returns the smallest
// number x such that:
//  x % num[0] = rem[0],
//  x % num[1] = rem[1],
//  ..................
//  x % num[k-2] = rem[k-1]
// Assumption: Numbers in num[] are pairwise coprime
// (gcd for every pair is 1)
func findMinX(num []uint64, rem []uint64) uint64 {
	// Compute product of all numbers
	var prod uint64 = 1
	for i := 0; i < len(num); i++ {
		prod *= num[i]
	}

	// Initialize result
	var result uint64

	// Apply above formula
	for i := 0; i < len(num); i++ {
		var pp uint64 = prod / num[i]
		result += rem[i] * modInverse(pp, num[i]) * pp
	}

	return result % prod
}

func sanitizeModulo(x, y uint64) uint64 {
	return (y - (x % y)) % y
}

func run(s []byte) uint64 {
	var currP uint64
	f := make([]uint64, 0, 100)
	p := make([]uint64, 0, 100)

	i := 0
	for s[i] != byte('\n') {
		i++
	}
	i++
	for i < len(s) && s[i] != byte('\n') {
		if s[i] == 'x' {
			i++
			if s[i] == ',' {
				i++
			}
			currP++
			continue
		}
		if i == len(s) {
			break
		}
		n := len(f)
		p = append(p, currP)
		currP++
		f = append(f, 0)
		for i < len(s) && s[i] >= byte('0') && s[i] <= byte('9') {
			f[n] = f[n]*10 + uint64(s[i]-'0')
			i++
		}
		if i < len(s) && s[i] == ',' {
			i++
		}
		p[n] = sanitizeModulo(p[n], f[n])
	}

	return findMinX(f, p)
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
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
