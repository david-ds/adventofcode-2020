const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const asc = std.sort.asc(u8);

fn run(input: [:0]u8) u64 {
    var parsed = [_]u8{0} ** 1000;
    var cache = [_]u64{0} ** 1000;
    var p_counter: usize = 1; // set initial value to 0

    var all_lines_it = std.mem.tokenize(input, "\n");
    while (all_lines_it.next()) |line| {
        const elt = std.fmt.parseInt(u8, line, 10) catch unreachable;
        parsed[p_counter] = elt;
        p_counter += 1;
    }
    std.sort.sort(u8, parsed[0..p_counter], {}, asc);
    parsed[p_counter] = parsed[p_counter - 1] + 3;
    p_counter += 1;
    cache[0] = 1;
    for (parsed[0..p_counter]) |elt, i| {
        if (i == 0) {
            // Flemme de réindexer
            continue;
        }
        if (i >= 1 and parsed[i] - parsed[i - 1] <= 3) {
            cache[i] += cache[i - 1];
        }
        if (i >= 2 and parsed[i] - parsed[i - 2] <= 3) {
            cache[i] += cache[i - 2];
        }
        if (i >= 3 and parsed[i] - parsed[i - 3] <= 3) {
            cache[i] += cache[i - 3];
        }
    }
    return cache[p_counter - 1];
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
    std.testing.expect(run(&b) == 8);
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
    std.testing.expect(run(&b) == 19208);
}
