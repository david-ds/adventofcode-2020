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
        if opCode == "jmp" || opCode == "nop" {
            val += idx
        }
        result = append(result, Instr { opCode: opCode, val: val })
    }
    return result 
}

func interpreter(opCodes []Instr, patchLine int) (int, bool) {
    var acc int
    var current int
    var nbOps int = len(opCodes)
    var alreadyExecuted []bool = make([]bool, nbOps)
    for {
        if current == nbOps { 
            return acc, true
        }
        if current < 0 || current > nbOps {
            return acc, false
        }
        if alreadyExecuted[current] {
            return acc, false
        }
        alreadyExecuted[current] = true

        currentOp := opCodes[current]
        currentOpCode := currentOp.opCode
        if current == patchLine {
           if currentOpCode == "jmp" {
               currentOpCode = "nop"
           } else {
               currentOpCode = "jmp"
           }
        }

        switch currentOpCode {
        case "acc":
            acc += currentOp.val
            current += 1
        case "jmp":
            current = currentOp.val
        case "nop":
            current += 1
        }
    }
    return acc, false
}

func run(s string) interface{} {
    ops := parseData(s)

    for idx, op := range ops {
        if op.opCode == "jmp" || op.opCode == "nop" {
            acc, terminate := interpreter(ops, idx)
            if terminate {
                return acc
            }
        }
    }
    return 0
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
