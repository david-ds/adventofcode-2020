package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	lines := strings.Split(s, "\n")
	startTS, _ := strconv.Atoi(lines[0])
	busIdsStr := strings.Split(lines[1], ",")
	var busIds []int
	for _, busIdStr := range busIdsStr {
		if busIdStr != "x" {
			busId, _ := strconv.Atoi(busIdStr)
			busIds = append(busIds, busId)
		}
	}
	sort.Ints(busIds)
	minDepTs := startTS + busIds[len(busIds) - 1]
	minDepBusId := busIds[len(busIds) - 1]

	for _, busId := range busIds {
		depTs := startTS + busId - (startTS % busId)
		if depTs < minDepTs {
			minDepTs = depTs
			minDepBusId = busId
		}
	}
	return (minDepTs - startTS) * minDepBusId
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
