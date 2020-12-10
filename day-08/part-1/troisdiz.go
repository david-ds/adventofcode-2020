package main

import (
	"fmt"
	"io/ioutil"
	"os"
    "strconv"
    "strings"
	"time"
)

type Instr struct {
    opCode string
    val int
}

func parseData(input string) []Instr {
    var result []Instr
    for idx, line := range strings.Split(input, "\n") {
        decodedOp := strings.Split(line, " ")
        opCode := decodedOp[0]
        val, _ := strconv.Atoi(decodedOp[1])
        // resolve jump destination now since there is no condition
        if opCode == "jmp" {
            val += idx
        }
        result = append(result, Instr { opCode: opCode, val: val })
    }
    return result 
}

func interpreter(opCodes []Instr) int {
    var acc int
    var current int
    var alreadyExecuted []bool = make([]bool, len(opCodes))
    for {
        if alreadyExecuted[current] {
            break
        }
        alreadyExecuted[current] = true

        currentOp := opCodes[current]
        switch currentOp.opCode {
        case "acc":
            acc += currentOp.val
            current += 1
        case "jmp":
            current = currentOp.val
        case "nop":
            current += 1
        }
    }
    return acc
}

func run(s string) interface{} {
    ops := parseData(s)
    return interpreter(ops)
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
