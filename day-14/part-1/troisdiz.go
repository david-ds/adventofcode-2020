package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

func applyMask(value uint64, orMask uint64, andMask uint64) uint64 {
	// fmt.Printf("Before mask : %v (%v)\n", disp36(value), value)
	value = value & orMask
	// fmt.Printf("After OR    : %v (%v)\n", disp36(value), value)
	value = value | andMask
	// fmt.Printf("After AND   : %v (%v)\n", disp36(value), value)
	return value
}

func parseMask(maskStr string) (uint64, uint64) {
	var andMask uint64 = 0// ones
	var orMask uint64 = math.MaxUint64// zeros
	for idx, ch := range maskStr {
		switch string(ch) {
		case "0":
			orMask -= 1 << (36-idx-1)
		case "1":
			andMask += 1 << (36-idx-1)
		}
	}
	return orMask, andMask
}

func disp36(value uint64) string {
	var result string = ""
	for i := 0; i < 36; i++ {
		// If there is a bit set at this position, write a 1.
		// ... Otherwise write a 0.
		if value & (1 << uint(i)) != 0 {
			result = "1" + result
		} else {
			result = "0" + result
		}
	}
	return result
}

func run(s string) interface{} {
	// Your code goes here
	var registers = make(map[int]uint64)

	var orMask, andMask uint64
	for _, line := range strings.Split(s, "\n") {
		if len(line) == 0 {
			// fmt.Printf("Skip\n")
			break
		}
		if line[0:7] == "mask = " {
			maskStr := line[7:7+36]
			//fmt.Printf("MASK :    %v\n", maskStr)
			orMask, andMask = parseMask(maskStr)
			//fmt.Printf("orMask :  %v (%v)\nandMask : %v (%v)\n", disp36(orMask), orMask, disp36(andMask), andMask)
		} else {
			memStr := strings.Split(line, " = ")
			regIdStr := memStr[0][4:len(memStr[0])-1]
			valueStr := memStr[1]

			regId, _ := strconv.Atoi(regIdStr)
			var value uint64
			value, _ = strconv.ParseUint(valueStr, 10, 64)
			registers[regId] = applyMask(value, orMask, andMask)
			//fmt.Printf("Value(%v) = %v => mem[%d] = %v\n", regIdStr, valueStr, regId, registers[regId])
		}
	}
	//fmt.Printf("Parse ok\n")

	var sum uint64
	for regKey := range registers {
		regVal := registers[regKey]
		// fmt.Printf("mem[%d] = %v\n", regKey, regVal)
		sum += regVal
	}
	return sum
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
