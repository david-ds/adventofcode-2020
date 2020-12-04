const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

test "simple" {
    const input = "byr:1944 iyr:2010 eyr:2021 hgt:158cm hcl:#b6652a ecl:blu pid:093154719 gar:coucou";
    var buf = input.*;
    std.testing.expect(run(&buf) == 1);
}

test "AoC examples" {
    const input =
        \\pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
        \\hcl:#623a2f
        \\
        \\eyr:2029 ecl:blu cid:129 byr:1989
        \\iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
        \\
        \\hcl:#888785
        \\hgt:164cm byr:2001 iyr:2015 cid:88
        \\pid:545766238 ecl:hzl
        \\eyr:2022
        \\
        \\iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
        \\
        \\eyr:1972 cid:100
        \\hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
        \\
        \\iyr:2019
        \\hcl:#602927 eyr:1967 hgt:170cm
        \\ecl:grn pid:012533040 byr:1946
        \\
        \\hcl:dab227 iyr:2012
        \\ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
        \\
        \\hgt:59cm ecl:zzz
        \\eyr:2038 hcl:74454a iyr:2023
        \\pid:3556412378 byr:2007
    ;
    var buf = input.*;
    std.testing.expect(run(&buf) == 4);
}

fn run(input: [:0]u8) u32 {
    var all_lines_it = std.mem.split(input, "\n");
    var valid_passwords: u32 = 0;
    var correct_fields: std.meta.Vector(7, bool) = [_]bool{false} ** 7; // Vectors allows SIMD reduce.
    var all_fields_valid: bool = true;
    while (all_lines_it.next()) |line| {
        if (line.len == 0) {
            // Empty lines are passport delimiters.
            if (@reduce(.And, correct_fields) and all_fields_valid) {
                // Check that we have the right 7 fields (or more, as long as they're all valid, who cares ?)
                valid_passwords += 1;
            }
            correct_fields = [_]bool{false} ** 7;
            all_fields_valid = true;
        } else {
            if (!all_fields_valid) {
                // Don't waste time parsing a line if we know this passport is invalid
                continue;
            }
            var tokenizer = std.mem.tokenize(line, " ");
            while (tokenizer.next()) |token| {
                if (token.len < 4) {
                    // Don't crash on malformed input
                    all_fields_valid = false;
                    break;
                }
                if (token[3] != ':') {
                    all_fields_valid = false;
                    break;
                }
                const _type = token[0..3];
                const value = token[4..];
                if (std.mem.eql(u8, _type, "byr")) {
                    // byr (Birth Year) - four digits; at least 1920 and at most 2002.
                    correct_fields[0] = true;
                    const value_int: u16 = std.fmt.parseInt(u16, value, 10) catch {
                        // this block is executed if parseInt throws an error
                        all_fields_valid = false;
                        continue;
                    };
                    if (value_int < 1920 or value_int > 2002) {
                        all_fields_valid = false;
                    }
                } else if (std.mem.eql(u8, _type, "iyr")) {
                    // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
                    correct_fields[1] = true;
                    const value_int: u16 = std.fmt.parseInt(u16, value, 10) catch {
                        all_fields_valid = false;
                        continue;
                    };
                    if (value_int < 2010 or value_int > 2020) {
                        all_fields_valid = false;
                    }
                } else if (std.mem.eql(u8, _type, "eyr")) {
                    // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
                    correct_fields[2] = true;
                    const value_int: u16 = std.fmt.parseInt(u16, value, 10) catch {
                        all_fields_valid = false;
                        continue;
                    };
                    if (value_int < 2020 or value_int > 2030) {
                        all_fields_valid = false;
                    }
                } else if (std.mem.eql(u8, _type, "hgt")) {
                    // hgt (Height) - a number followed by either cm or in:
                    // If cm, the number must be at least 150 and at most 193.
                    // If in, the number must be at least 59 and at most 76.
                    correct_fields[3] = true;
                    const len = value.len;
                    switch (value[len - 1]) {
                        'm' => {
                            if (value[value.len - 2] == 'c') {
                                const hgt = std.fmt.parseInt(u8, value[0 .. len - 2], 10) catch {
                                    all_fields_valid = false;
                                    continue;
                                };
                                if (150 > hgt or hgt > 193) { // On a pas le droit de faire plus d'1m93 askip
                                    all_fields_valid = false;
                                }
                            }
                        },
                        'n' => {
                            if (value[value.len - 2] == 'i') {
                                const hgt = std.fmt.parseInt(u8, value[0 .. len - 2], 10) catch {
                                    all_fields_valid = false;
                                    continue;
                                };
                                if (59 > hgt or hgt > 76) {
                                    all_fields_valid = false;
                                }
                            }
                        },
                        else => {
                            all_fields_valid = false;
                            continue;
                        },
                    }
                } else if (std.mem.eql(u8, _type, "hcl")) {
                    // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
                    correct_fields[4] = true;
                    if (value[0] != '#') {
                        all_fields_valid = false;
                        continue;
                    }
                    if (value[1..].len != 6) {
                        all_fields_valid = false;
                        continue;
                    }
                    for (value[1..]) |char| {
                        if (char < '0' or (char > '9' and (char < 'a' or char > 'z'))) {
                            all_fields_valid = false;
                            break;
                        }
                    }
                } else if (std.mem.eql(u8, _type, "ecl")) {
                    // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
                    correct_fields[5] = true;
                    if (!(std.mem.eql(u8, value, "amb") or std.mem.eql(u8, value, "blu") or std.mem.eql(u8, value, "brn") or std.mem.eql(u8, value, "gry") or std.mem.eql(u8, value, "grn") or std.mem.eql(u8, value, "hzl") or std.mem.eql(u8, value, "oth"))) {
                        all_fields_valid = false;
                    }
                } else if (std.mem.eql(u8, _type, "pid")) {
                    // pid (Passport ID) - a nine-digit number, including leading zeroes.
                    correct_fields[6] = true;
                    var digits: i8 = 0;
                    for (value) |char| {
                        if (char >= '0' and char <= '9') {
                            digits += 1;
                        } else {
                            all_fields_valid = false;
                            break;
                        }
                    }
                    if (digits != 9) {
                        all_fields_valid = false;
                    }
                }
                // cid (Country ID) - ignored, missing or not.
                // all extra fields are ignored as well, in case passports contain country-specific extra items
            }
        }
    }
    if (@reduce(.And, correct_fields) and all_fields_valid) {
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
