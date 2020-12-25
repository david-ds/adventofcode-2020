package main

import (
	"fmt"
	"io/ioutil"
	"math/big"
	"os"
	"strconv"
	"strings"
	"time"
)

const modulo int64 = 20201227

func run(s string) interface{} {
	split := strings.Split(s, "\n")
	doorPubKey, _ := strconv.ParseInt(split[0], 10, 64)
	cardPubKey, _ := strconv.ParseInt(split[1], 10, 64)

	var val int64 = 1
	var loopSize int64 = 0
	for val != doorPubKey {
		val = (val * 7) % modulo
		loopSize++
	}

	encryptionKey := new(big.Int)
	encryptionKey.Exp(big.NewInt(cardPubKey), big.NewInt(loopSize), big.NewInt(modulo))

	return encryptionKey.String()
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
