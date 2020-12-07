const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

test "aoc example" {
    const in =
        \\abc
        \\
        \\a
        \\b
        \\c
        \\
        \\ab
        \\ac
        \\
        \\a
        \\a
        \\a
        \\a
        \\
        \\z
        \\
    ;
    var b = in.*;
    const ans = run(&b);
    std.debug.print("{}", .{ans});
    std.testing.expect(ans == 11);
}

fn run(input: [:0]u8) u32 {
    var out: u32 = 0;
    var questions = [_]bool{false} ** 255;
    var all_lines_it = std.mem.split(input, "\n\n");
    while (all_lines_it.next()) |line| {
        for (line) |char| {
            questions[char] = true;
        }
        for (questions['a' .. 'z' + 1]) |q| {
            if (q) {
                out += 1;
            }
        }
        questions = [_]bool{false} ** 255;
    }
    for (questions['a' .. 'z' + 1]) |q| {
        if (q) {
            out += 1;
        }
    }
    return out;
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
