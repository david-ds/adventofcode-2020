const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]u8) i64 {
    var parsed: [300]i64 = undefined;
    var parsed_total: usize = 0;
    var it = std.mem.tokenize(input, "\n");
    while (it.next()) |item| {
        parsed[parsed_total] = std.fmt.parseInt(i64, item, 10) catch unreachable; // we control the input type
        parsed_total += 1;
    }
    for (parsed[0..parsed_total]) |int1, idx1| {
        for (parsed[idx1..parsed_total]) |int2, idx2| {
            if (int1 + int2 > 2020) {
                continue;
            }
            for (parsed[idx2..parsed_total]) |int3| {
                if (int1 + int2 + int3 == 2020) {
                    return int1 * int2 * int3;
                }
            }
        }
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
