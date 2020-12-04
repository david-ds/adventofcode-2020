const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

// byr (Birth Year)
// iyr (Issue Year)
// eyr (Expiration Year)
// hgt (Height)
// hcl (Hair Color)
// ecl (Eye Color)
// pid (Passport ID)
// cid (Country ID) (Optional)

test "short input" {
    const input =
        \\ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        \\byr:1937 iyr:2017 cid:147 hgt:183cm
        \\
        \\iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        \\hcl:#cfa07d byr:1929
        \\
        \\hcl:#ae17e1 iyr:2013
        \\eyr:2024
        \\ecl:brn pid:760753108 byr:1931
        \\hgt:179cm
        \\
        \\hcl:#cfa07d eyr:2025 pid:166559648
        \\iyr:2011 ecl:brn hgt:59in
    ;
    var buf = input.*;
    std.testing.expect(run(&buf) == 2);
}

fn run(input: [:0]u8) u16 {
    var all_lines_it = std.mem.split(input, "\n");
    var valid_passwords: u16 = 0;
    var correct_fields: std.meta.Vector(7, bool) = [_]bool{false} ** 7; // Vectors allows SIMD reduce.
    while (all_lines_it.next()) |line| {
        if (line.len == 0) {
            if (@reduce(.And, correct_fields)) { // This allows an attacker to specify fields multiple times. Not an attack surface.
                valid_passwords += 1;
            }
            correct_fields = [_]bool{false} ** 7;
        } else {
            var tokenizer = std.mem.tokenize(line, " ");
            while (tokenizer.next()) |token| {
                if (token.len < 4) {
                    // Don't crash on malformed input
                    break;
                }
                if (token[3] != ':') {
                    break;
                }
                const _type = token[0..3];
                //const value = token[4..];  // no need to parse this for now
                if (std.mem.eql(u8, _type, "byr")) {
                    correct_fields[0] = true;
                } else if (std.mem.eql(u8, _type, "iyr")) {
                    correct_fields[1] = true;
                } else if (std.mem.eql(u8, _type, "eyr")) {
                    correct_fields[2] = true;
                } else if (std.mem.eql(u8, _type, "hgt")) {
                    correct_fields[3] = true;
                } else if (std.mem.eql(u8, _type, "hcl")) {
                    correct_fields[4] = true;
                } else if (std.mem.eql(u8, _type, "ecl")) {
                    correct_fields[5] = true;
                } else if (std.mem.eql(u8, _type, "pid")) {
                    correct_fields[6] = true;
                }
                // we don't fail on extra fields, as some passports might have them;
            }
        }
    }
    if (@reduce(.And, correct_fields)) {
        valid_passwords += 1;
    }
    return valid_passwords;
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
