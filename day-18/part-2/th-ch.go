package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"go/types"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

var fs = token.NewFileSet()

func evaluate(op string) int {
	// Invert */+ to build the AST
	expr := strings.Replace(op, "+", "-", -1)
	expr = strings.Replace(expr, "*", "+", -1)
	expr = strings.Replace(expr, "-", "*", -1)

	// Parse into AST
	tree, _ := parser.ParseExprFrom(fs, "eval", expr, 0)

	// Re-invert */+ in the AST
	ast.Inspect(tree, func(n ast.Node) bool {
		node, ok := n.(*ast.BinaryExpr)
		if ok {
			// Operator found, invert +/*
			if node.Op == token.MUL {
				node.Op = token.ADD
			} else if node.Op == token.ADD {
				node.Op = token.MUL
			}
		}

		return true
	})

	// Evaluate the AST
	info := &types.Info{
		Types: make(map[ast.Expr]types.TypeAndValue),
	}
	types.CheckExpr(fs, nil, token.NoPos, tree, info)
	value, _ := strconv.Atoi(info.Types[tree].Value.String())

	return value
}

func run(s string) interface{} {
	sum := 0
	for _, op := range strings.Split(s, "\n") {
		sum += evaluate(op)
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
