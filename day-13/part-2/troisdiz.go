package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type BusIdPos struct {
	pos int64
	busId int64
}

func testTS(ts int64, busIdPosList []BusIdPos) bool {
	var result = true
	for _, busIdPos := range busIdPosList {
		if (ts + busIdPos.pos) % busIdPos.busId != 0 {
			result = false
			break
		}
	}
	//fmt.Printf("testTS(%d, %v) -> %v\n", ts, busIdPosList, result)
	return result
}

func lcm(a int64, b int64) int64 {
	// it seems a and b are always prime ;-)
	return a * b
}

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	busIdsStr := strings.Split(lines[1], ",")
	var busIdPosList []BusIdPos
	for idx, busIdStr := range busIdsStr {
		if busIdStr != "x" {
			busId, _ := strconv.Atoi(busIdStr)
			busIdPosList = append(busIdPosList, BusIdPos{ pos: int64(idx), busId: int64(busId)})
		}
	}

	var ts int64
	var currentPos int = 0
	var lastPos int = len(busIdPosList)-1
	var incr int64 = 1
	for  {
		if testTS(ts, busIdPosList[0:currentPos+1]) {
			if currentPos == lastPos {
				break
			} else {
				// fmt.Printf("pos : %d ok, -> pos : %d (ts = %v)\n", currentPos, currentPos+1, ts)
				incr = lcm(incr, busIdPosList[currentPos].busId)
				currentPos += 1
			}
		} else {
			ts += incr
		}
	}
	return ts
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
