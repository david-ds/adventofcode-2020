package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strconv"
    "strings"
	"time"
)

// result : x, y, dir, waypX, waypY
func applyOrder(orderType string, orderMagnitude int, startPosX int, startPosY int, wayPointX int, wayPointY int) (int, int, int, int) {

    switch orderType {
    case "N":
        return startPosX, startPosY, wayPointX, wayPointY + orderMagnitude
    case "S":
        return startPosX, startPosY, wayPointX, wayPointY - orderMagnitude
    case "E":
        return startPosX, startPosY, wayPointX + orderMagnitude, wayPointY
    case "W":
        return startPosX, startPosY, wayPointX - orderMagnitude, wayPointY
    case "L":
    	wayPointX, wayPointY = rotateVector(wayPointX, wayPointY, orderMagnitude)
        return startPosX, startPosY, wayPointX, wayPointY
    case "R":
		wayPointX, wayPointY = rotateVector(wayPointX, wayPointY, 360-orderMagnitude)
		return startPosX, startPosY, wayPointX, wayPointY
    case "F":
        return startPosX + orderMagnitude * wayPointX,
        	startPosY + orderMagnitude * wayPointY,
        	wayPointX,
        	wayPointY
    }
    return -1, -1, -1, -1
}

func rotateVector(x int, y int, counterClockWiseAngle int) (int, int) {
    var rotMatr = map[int][][]int {
        90: {
            {0, -1},
            {1, 0},
        },
		180: {
			{-1, 0},
			{0, -1},
		},
		270: {
			{0, 1},
			{-1, 0},
		},
    }
    matr := rotMatr[counterClockWiseAngle]
    return x * matr[0][0] + y * matr[0][1], x * matr[1][0] + y * matr[1][1]
}

func abs(i int) int {
    if i < 0 {
        return -i
    } else {
        return i
    }
}


func displayApply(orderType string, orderMagnitude int, startPosX int, startPosY int, wayPointX int, wayPointY int) {
    x, y, waypX, waypY := applyOrder(orderType, orderMagnitude, startPosX, startPosY, wayPointX, wayPointY)
    fmt.Printf("%v%d => x : %d, y : %d, wayp X : %d, wayp Y : %d\n", orderType, orderMagnitude, x, y, waypX, waypY)
}

func run(s string) interface{} {
    x := 0
    y := 0
	waypX := 10
	waypY := 1

    for _, line := range strings.Split(s, "\n") {
        orderType := string(line[0])
        orderMagnitude, _ := strconv.Atoi(string(line[1:]))
        x, y, waypX, waypY = applyOrder(orderType, orderMagnitude, x, y, waypX, waypY)
    }

    return abs(x) + abs(y)
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
