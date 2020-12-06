const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

// Problem-specific
const ROW_BITSIZE: u8 = 7;
const COLUMN_BITSIZE: u8 = 3;

test "aoc input 0" {
    // FBFBBFFRLR: row 44, col 5, id 357
    const t = "FBFBBFFRLR";
    var b = t.*;
    std.testing.expect(run(&b) == 357);
}

test "aoc input 1" {
    // BFFFBBFRRR: row 70, column 7, seat ID 567.
    const t = "BFFFBBFRRR";
    var b = t.*;
    std.testing.expect(run(&b) == 567);
}

test "aoc input 2" {
    // FFFBBBFRRR: row 14, column 7, seat ID 119.\
    const t = "FFFBBBFRRR";
    var b = t.*;
    std.testing.expect(run(&b) == 119);
}

test "aoc input 3" {
    // BBFFBBFRLL: row 102, column 4, seat ID 820.
    const t = "BBFFBBFRLL";
    var b = t.*;
    std.testing.expect(run(&b) == 820);
}

test "aoc all" {
    const t =
        \\FBFBBFFRLR
        \\BFFFBBFRRR
        \\FFFBBBFRRR
        \\BBFFBBFRLL
    ;
    var b = t.*;
    std.testing.expect(run(&b) == 820);
}

fn run(input: [:0]u8) u32 {
    var max_id: u32 = 0;
    var cur_id: u32 = 0;
    var row: u8 = 0;
    var column: u8 = 0;
    var all_lines = std.mem.tokenize(input, "\n");
    while (all_lines.next()) |line| {
        for (line[0..ROW_BITSIZE]) |char, i| {
            if (char == 'B') {
                row |= @as(u8, 1) << @intCast(u3, ROW_BITSIZE - i - 1);
            }
        }
        for (line[(ROW_BITSIZE)..(ROW_BITSIZE + COLUMN_BITSIZE)]) |char, i| {
            if (char == 'R') {
                column |= @as(u8, 1) << @intCast(u3, COLUMN_BITSIZE - i - 1);
            }
        }
        cur_id = @as(u32, row) * 8 + column;
        //std.debug.print("{}: row {} col {} ID {}\n", .{ line, row, column, cur_id });
        if (cur_id > max_id) {
            max_id = cur_id;
        }
        cur_id = 0;
        row = 0;
        column = 0;
    }
    return max_id;
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
