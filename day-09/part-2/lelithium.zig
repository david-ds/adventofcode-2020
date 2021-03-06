const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const PREAMBLE_SIZE: usize = 25;

fn check_valid(window: []?u64, target: u64) bool {
    for (window) |elt1_opt, idx| {
        if (elt1_opt) |elt1| {
            for (window[idx..]) |elt2| {
                if (elt1 + elt2.? == target) {
                    return true;
                }
            }
        }
    }
    return false;
}

fn run(input: [:0]u8) u64 {
    var all_lines_it = std.mem.tokenize(input, "\n");
    var parsed = [_]?u64{null} ** 1000;
    var counter: usize = 0;
    var i: usize = 0;
    while (i < 25) : (i += 1) {
        parsed[counter] = std.fmt.parseInt(u64, all_lines_it.next().?, 10) catch unreachable;
        counter += 1;
    }
    var target: u64 = 0;
    while (all_lines_it.next()) |line| {
        target = std.fmt.parseInt(u64, line, 10) catch unreachable;
        if (!check_valid(parsed[counter - PREAMBLE_SIZE .. counter], target)) {
            break;
        }
        parsed[counter] = target;
        counter += 1;
    }
    var sum: u64 = 0;
    var start_idx: usize = 0;
    var end_idx: usize = 0;
    for (parsed) |elt_opt, cur_idx| {
        if (elt_opt) |elt| {
            sum += elt;
            while (sum > target) {
                sum -= parsed[start_idx].?;
                start_idx += 1;
            }
            if (sum == target) {
                end_idx = cur_idx;
                break;
            }
        }
    }
    var min: u64 = parsed[start_idx].?;
    var max: u64 = parsed[start_idx].?;
    for (parsed[start_idx .. end_idx + 1]) |elt| {
        if (elt.? < min) {
            min = elt.?;
        } else if (elt.? > max) {
            max = elt.?;
        }
    }
    return min + max;
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

test "aoc input 1" {
    const i =
        \\1
        \\2
        \\3
        \\4
        \\5
        \\6
        \\7
        \\8
        \\9
        \\10
        \\11
        \\12
        \\13
        \\14
        \\15
        \\16
        \\17
        \\18
        \\19
        \\20
        \\21
        \\22
        \\23
        \\24
        \\25
        \\26
        \\49
        \\100
    ;
    var b = i.*;
    std.testing.expect(run(&b) == 25);
}
