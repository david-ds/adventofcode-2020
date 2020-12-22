package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func applyMask(value uint64, mask uint64, floatingPositions []uint64) []uint64 {
	// fmt.Printf("Before mask :\n    M: %v (%v)\n    V: %v (%v)\n", disp36(mask), mask, disp36(value), value)
	value = value | mask
	// fmt.Printf("    R: %v (%v)\n", disp36(value), value)

	var values []uint64
	for i := 0; i < 1 << len(floatingPositions); i++ {
		for posIdx, pos := range floatingPositions {

			bitVal := uint64(1) & (uint64(i) >> posIdx)
			if bitVal == 0 {
				value = clearBit(value, pos)
			} else {
				value = setBit(value, pos)
			}
		}
		values = append(values, value)
	}
	// fmt.Printf("Possible values : %v\n", values)
	return values
}

func setBit(val uint64, pos uint64) uint64 {
	return val | (uint64(1) << pos)
}

func clearBit(val uint64, pos uint64) uint64 {
	return val & ^(uint64(1) << pos)
}

func parseMask(maskStr string) (uint64, []uint64) {
	var mask uint64 = 0
	var floatingPositions []uint64
	for idx, ch := range maskStr {
		switch string(ch) {
		case "X":
			floatingPositions = append(floatingPositions, uint64(36-idx-1))
		case "1":
			mask += 1 << (36-idx-1)
		}
	}
	return mask, floatingPositions
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
	var registers = make(map[uint64]uint64)

	var mask uint64
	var floatingPositions []uint64
	for _, line := range strings.Split(s, "\n") {
		if len(line) == 0 {
			// fmt.Printf("Skip\n")
			break
		}
		if line[0:7] == "mask = " {
			maskStr := line[7:7+36]
			//fmt.Printf("MASK :    %v\n", maskStr)
			mask, floatingPositions = parseMask(maskStr)
			// fmt.Printf("Mask :  %v (%v)\nfloatingPositions : %v\n", disp36(mask), mask, floatingPositions)
		} else {
			memStr := strings.Split(line, " = ")
			regIdStr := memStr[0][4:len(memStr[0])-1]
			valueStr := memStr[1]

			regId, _ := strconv.ParseUint(regIdStr, 10, 64)
			var value uint64
			value, _ = strconv.ParseUint(valueStr, 10, 64)
			regIds := applyMask(regId, mask, floatingPositions)

			for _, regId = range regIds {
				registers[regId] = value
			}
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
