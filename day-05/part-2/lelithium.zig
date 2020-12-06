const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

// Problem-specific
const ROW_BITSIZE: u8 = 7;
const COLUMN_BITSIZE: u8 = 3;

fn run(input: [:0]u8) u64 {
    var ids = [_]bool{false} ** 1024;
    var row: u32 = 0;
    var column: u32 = 0;
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
        ids[row * 8 + column] = true;
        row = 0;
        column = 0;
    }
    var past_past_seat: bool = false;
    var past_seat: bool = false;
    for (ids[2..]) |present, id| {
        if (!past_seat) {
            if (past_past_seat and present) {
                return id + 1;
            }
        }
        past_past_seat = past_seat;
        past_seat = present;
    }
    return 0;
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
