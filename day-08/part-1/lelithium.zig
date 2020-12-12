const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Op = enum {
    acc,
    jmp,
    nop,
    invalid,
    pub fn init(op: []const u8) Op {
        if (std.mem.eql(u8, op, "acc")) {
            return Op.acc;
        } else if (std.mem.eql(u8, op, "jmp")) {
            return Op.jmp;
        } else if (std.mem.eql(u8, op, "nop")) {
            return Op.nop;
        }
        return Op.invalid;
    }
};

const Instruction = struct {
    op: Op, arg: i32
};

fn run_code(program: [700]?Instruction) i64 {
    var seen_pc: [700]bool = [_]bool{false} ** 700;
    var PC: usize = 0;
    var ACC: i64 = 0;
    while (true) {
        //std.debug.print("PC: {}\t", .{PC});
        if (seen_pc[PC]) {
            break;
        }
        seen_pc[PC] = true;
        if (program[PC]) |instruction| {
            //std.debug.print("{}\n", .{instruction});
            switch (instruction.op) {
                .acc => {
                    ACC += instruction.arg;
                    PC += 1;
                },
                .jmp => {
                    PC = @intCast(usize, @intCast(i32, PC) + instruction.arg);
                },
                .nop => {
                    PC += 1;
                },
                .invalid => {
                    break;
                },
            }
        } else {
            break;
        }
    }
    //std.debug.print("RETURNING {}\n", .{ACC});
    return ACC;
}

fn run(input: [:0]u8) i64 {
    var instructions = [_]?Instruction{null} ** 700;
    var instruction_counter: usize = 0;
    var all_lines_it = std.mem.split(input, "\n");
    while (all_lines_it.next()) |line| {
        var tokenizer = std.mem.tokenize(line, " ");
        instructions[instruction_counter] = Instruction{
            .op = Op.init(tokenizer.next().?),
            .arg = std.fmt.parseInt(i32, tokenizer.next().?, 10) catch unreachable, // I like to live dangerously
        };
        instruction_counter += 1;
    }
    return run_code(instructions);
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
        \\nop +0
        \\acc +1
        \\jmp +4
        \\acc +3
        \\jmp -3
        \\acc -99
        \\acc +1
        \\jmp -4
        \\acc +6
    ;
    var b = i.*;
    std.testing.expect(run(&b) == 5);
}
