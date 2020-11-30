const std = @import("std");

const testing = std.testing;
const process = std.process;
const fs = std.fs;
const ChildProcess = std.ChildProcess;

var a: *std.mem.Allocator = undefined;

fn run(input: [:0]u8) i64 {
    var out: i64 = 0;
    return out;
}

pub fn main() !void {
    const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory

    var arg_it = process.args();

    _ = arg_it.skip(); // skip over exe name
    a = &arena.allocator; // get ref to allocator
    const input: [:0]u8 = try (arg_it.next(a)).?; // get the first argument

    const start: i128 = std.time.nanoTimestamp(); // start time
    const answer = run(input); // compute answer
    const elapsed: i128 = (std.time.nanoTimestamp() - start); // compute function duration
    try stdout.print("_duration:{}\n{}", .{ elapsed, answer }); // emit actual lines parsed by AOC
}
