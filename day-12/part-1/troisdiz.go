package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strconv"
    "strings"
	"time"
)

func applyOrder(orderType string, orderMagnitude int, startPosX int, startPosY int, direction int) (int, int, int) {

    // change F order into right move order to have single way of handling moves

    computedOrderType := orderType
    if orderType == "F" {
        switch direction {
        case 0:
            computedOrderType = "N"
        case 1:
            computedOrderType = "E"
        case 2:
            computedOrderType = "S"
        case 3:
            computedOrderType = "W"
        default:
            fmt.Printf("Direction : %d ERROR\n", direction)
        }
    }

    switch computedOrderType {
    case "N":
        return startPosX, startPosY + orderMagnitude, direction
    case "S":
        return startPosX, startPosY - orderMagnitude, direction
    case "E":
        return startPosX + orderMagnitude, startPosY, direction
    case "W":
        return startPosX - orderMagnitude, startPosY, direction
    case "L":
        return startPosX, startPosY, (4 + direction - (orderMagnitude / 90)) % 4
    case "R":
        return startPosX, startPosY, (4 + direction + (orderMagnitude / 90)) % 4
    case "F":
        fmt.Println("F move here : ERROR\n")
    }
    return -1, -1, -1
}

func abs(i int) int {
    if i < 0 {
        return -i
    } else {
        return i
    }
}

func displayApply(orderType string, orderMagnitude int, startPosX int, startPosY int, direction int) {
    x, y, dir := applyOrder(orderType, orderMagnitude, startPosX, startPosY, direction)
    fmt.Printf("%v%d => x : %d, y : %d, dir : %d\n", orderType, orderMagnitude, x, y, dir)
}

func run(s string) interface{} {
    var x,y, dir int
    x = 0
    y = 0
    dir = 1

    for _, line := range strings.Split(s, "\n") {
        orderType := string(line[0])
        orderMagnitude, _ := strconv.Atoi(string(line[1:]))
        x, y, dir = applyOrder(orderType, orderMagnitude, x, y, dir)
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
