const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

//   ---> x axis
//  |
//  | y axis
//  v

const LINE_LEN: usize = 31; // ....#...#####..##.#..##..#....#
//const LINE_LEN: usize = 11; // test case only

test "slopes" {
    const input =
        \\..##.......
        \\#...#...#..
        \\.#....#..#.
        \\..#.#...#.#
        \\.#...##..#.
        \\..#.##.....
        \\.#.#.#....#
        \\.#........#
        \\#.##...#...
        \\#...##....#
        \\.#..#...#.#
    ;
    var buf = input.*;
    std.testing.expect(run_for_slope(&buf, 1, 1) == 2);
    std.testing.expect(run_for_slope(&buf, 3, 1) == 7);
    std.testing.expect(run_for_slope(&buf, 5, 1) == 3);
    std.testing.expect(run_for_slope(&buf, 7, 1) == 4);
    std.testing.expect(run_for_slope(&buf, 1, 2) == 2);
    std.testing.expect(run(&buf) == 336);
}

fn run_for_slope(input: [:0]u8, skip_x: usize, skip_y: usize) i32 {
    var all_lines_it = std.mem.tokenize(input, "\n");
    var trees: i32 = 0;

    var cur_x: usize = 0;
    var cur_y: usize = 0;

    while (all_lines_it.next()) |line| {
        if (@mod(cur_y, skip_y) == 0) {
            if (line[@mod(cur_x, LINE_LEN)] == '#') {
                trees += 1;
            }
            cur_x += skip_x;
        }
        cur_y += 1;
    }
    return trees;
}

fn run(input: [:0]u8) i64 {
    var total_trees: i64 = 1;
    const test_slopes = [5][2]usize{
        [_]usize{ 1, 1 },
        [_]usize{ 3, 1 },
        [_]usize{ 5, 1 },
        [_]usize{ 7, 1 },
        [_]usize{ 1, 2 },
    };
    for (test_slopes) |slopes| {
        total_trees *= run_for_slope(input, slopes[0], slopes[1]);
    }
    return total_trees;
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
