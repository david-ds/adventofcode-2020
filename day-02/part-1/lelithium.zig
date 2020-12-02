const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]u8) i64 {
    var all_lines_it = std.mem.tokenize(input, "\n");
    var valid: i16 = 0;
    while (all_lines_it.next()) |line| {
        var line_it = std.mem.tokenize(line, "- :");
        var min_len: i16 = std.fmt.parseInt(i16, line_it.next().?, 10) catch unreachable;
        var max_len: i16 = std.fmt.parseInt(i16, line_it.next().?, 10) catch unreachable;
        var target_char: u8 = (line_it.next().?)[0];
        var counter: i16 = 0;
        for (line_it.next().?) |cur_char| {
            if (cur_char == target_char) {
                counter += 1;
            }
        }
        if (min_len <= counter and counter <= max_len) {
            valid += 1;
        }
    }

    return valid;
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
