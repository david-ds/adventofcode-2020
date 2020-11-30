import os
#include <time.h> // The Vlib time library only supports second precision

fn C.clock() f64

fn get_time() f64{
	return C.clock()
}

fn run(input string) int{
	// Your code here
	return 0
}

fn main() {
	start := get_time()
	answer := run(os.args[1])
	elapsed := ((get_time() - start) * 1000) / C.CLOCKS_PER_SEC
	println("_duration:$elapsed\n$answer")
}
