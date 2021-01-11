const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const asc = std.sort.asc(u8);

fn run(input: [:0]u8) u32 {
    var parsed = [_]u8{0} ** 1000;
    var p_counter: usize = 0;

    var all_lines_it = std.mem.tokenize(input, "\n");
    while (all_lines_it.next()) |line| {
        const elt = std.fmt.parseInt(u8, line, 10) catch unreachable;
        parsed[p_counter] = elt;
        p_counter += 1;
    }
    std.sort.sort(u8, parsed[0..p_counter], {}, asc);
    var onediff: u32 = 0;
    var threediff: u32 = 0;
    var last: u8 = 0;
    for (parsed[0..p_counter]) |i| {
        if (i - last == 1) {
            onediff += 1;
        } else if (i - last == 3) {
            threediff += 1;
        }
        last = i;
    }
    threediff += 1;
    return onediff * threediff;
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

test "aoc simple" {
    const i =
        \\16
        \\10
        \\15
        \\5
        \\1
        \\11
        \\7
        \\19
        \\6
        \\12
        \\4
    ;
    var b = i.*;
    std.testing.expect(run(&b) == 35);
}

test "aoc long" {
    const i =
        \\28
        \\33
        \\18
        \\42
        \\31
        \\14
        \\46
        \\20
        \\48
        \\47
        \\24
        \\23
        \\49
        \\45
        \\19
        \\38
        \\39
        \\11
        \\1
        \\32
        \\25
        \\35
        \\8
        \\17
        \\7
        \\9
        \\4
        \\2
        \\34
        \\10
        \\3
    ;
    var b = i.*;
    std.testing.expect(run(&b) == 220);
}
