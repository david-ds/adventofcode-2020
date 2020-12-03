const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

//   ---> x axis
//  |
//  | y axis
//  v

const SKIP_X: usize = 3;
const SKIP_Y: usize = 1;

const LINE_LEN: usize = 31; // ....#...#####..##.#..##..#....#

fn run(input: [:0]u8) i64 {
    var all_lines_it = std.mem.tokenize(input, "\n");
    var trees: i32 = 0;

    var cur_x: usize = 0;
    var cur_y: usize = 0;

    while (all_lines_it.next()) |line| {
        cur_y += 1;
        if (@mod(cur_y, SKIP_Y) == 0) {
            if (line[@mod(cur_x, LINE_LEN)] == '#') {
                trees += 1;
            }
        }
        cur_x += SKIP_X;
    }
    return trees;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory

    var arg_it = std.process.args();

    _ = arg_it.skip(); // skip over exe name
    a = &arena.allocator; // get ref to allocator
    const input: [:0]u8 = try (arg_it.next(a)).?; // get the first argument

    const start: i128 = std.time.nanoTimestamp(); // start time
    const answer = run(input); // compute answer
    const elapsed_nano: f128 = @intToFloat(f128, std.time.nanoTimestamp() - start);
    const elapsed_milli: f64 = @floatCast(f64, @divFloor(elapsed_nano, 1_000_000));
    try stdout.print("_duration:{d}\n{}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}
