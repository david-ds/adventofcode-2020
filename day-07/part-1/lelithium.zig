const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Type = enum {
    bright,
    clear,
    dark,
    dim,
    dotted,
    drab,
    dull,
    faded,
    light,
    mirrored,
    muted,
    pale,
    plaid,
    posh,
    shiny,
    striped,
    vibrant,
    wavy,
    invalid,
    pub fn init(ipt: []const u8) Type {
        if (std.mem.eql(u8, ipt, "bright")) {
            return Type.bright;
        } else if (std.mem.eql(u8, ipt, "clear")) {
            return Type.clear;
        } else if (std.mem.eql(u8, ipt, "dark")) {
            return Type.dark;
        } else if (std.mem.eql(u8, ipt, "dim")) {
            return Type.dim;
        } else if (std.mem.eql(u8, ipt, "dotted")) {
            return Type.dotted;
        } else if (std.mem.eql(u8, ipt, "drab")) {
            return Type.drab;
        } else if (std.mem.eql(u8, ipt, "dull")) {
            return Type.dull;
        } else if (std.mem.eql(u8, ipt, "faded")) {
            return Type.faded;
        } else if (std.mem.eql(u8, ipt, "light")) {
            return Type.light;
        } else if (std.mem.eql(u8, ipt, "mirrored")) {
            return Type.mirrored;
        } else if (std.mem.eql(u8, ipt, "muted")) {
            return Type.muted;
        } else if (std.mem.eql(u8, ipt, "pale")) {
            return Type.pale;
        } else if (std.mem.eql(u8, ipt, "plaid")) {
            return Type.plaid;
        } else if (std.mem.eql(u8, ipt, "posh")) {
            return Type.posh;
        } else if (std.mem.eql(u8, ipt, "shiny")) {
            return Type.shiny;
        } else if (std.mem.eql(u8, ipt, "striped")) {
            return Type.striped;
        } else if (std.mem.eql(u8, ipt, "vibrant")) {
            return Type.vibrant;
        } else if (std.mem.eql(u8, ipt, "wavy")) {
            return Type.wavy;
        }
        return Type.invalid;
    }
};

const Color = enum {
    aqua,
    beige,
    black,
    blue,
    bronze,
    brown,
    chartreuse,
    coral,
    crimson,
    cyan,
    fuchsia,
    gold,
    gray,
    green,
    indigo,
    lavender,
    lime,
    magenta,
    maroon,
    olive,
    orange,
    plum,
    purple,
    red,
    salmon,
    silver,
    tan,
    teal,
    tomato,
    turquoise,
    violet,
    white,
    yellow,
    invalid,
    pub fn init(ipt: []const u8) Color {
        if (std.mem.eql(u8, ipt, "aqua")) {
            return Color.aqua;
        } else if (std.mem.eql(u8, ipt, "beige")) {
            return Color.beige;
        } else if (std.mem.eql(u8, ipt, "black")) {
            return Color.black;
        } else if (std.mem.eql(u8, ipt, "blue")) {
            return Color.blue;
        } else if (std.mem.eql(u8, ipt, "bronze")) {
            return Color.bronze;
        } else if (std.mem.eql(u8, ipt, "brown")) {
            return Color.brown;
        } else if (std.mem.eql(u8, ipt, "chartreuse")) {
            return Color.chartreuse;
        } else if (std.mem.eql(u8, ipt, "coral")) {
            return Color.coral;
        } else if (std.mem.eql(u8, ipt, "crimson")) {
            return Color.crimson;
        } else if (std.mem.eql(u8, ipt, "cyan")) {
            return Color.cyan;
        } else if (std.mem.eql(u8, ipt, "fuchsia")) {
            return Color.fuchsia;
        } else if (std.mem.eql(u8, ipt, "gold")) {
            return Color.gold;
        } else if (std.mem.eql(u8, ipt, "gray")) {
            return Color.gray;
        } else if (std.mem.eql(u8, ipt, "green")) {
            return Color.green;
        } else if (std.mem.eql(u8, ipt, "indigo")) {
            return Color.indigo;
        } else if (std.mem.eql(u8, ipt, "lavender")) {
            return Color.lavender;
        } else if (std.mem.eql(u8, ipt, "lime")) {
            return Color.lime;
        } else if (std.mem.eql(u8, ipt, "magenta")) {
            return Color.magenta;
        } else if (std.mem.eql(u8, ipt, "maroon")) {
            return Color.maroon;
        } else if (std.mem.eql(u8, ipt, "olive")) {
            return Color.olive;
        } else if (std.mem.eql(u8, ipt, "orange")) {
            return Color.orange;
        } else if (std.mem.eql(u8, ipt, "plum")) {
            return Color.plum;
        } else if (std.mem.eql(u8, ipt, "purple")) {
            return Color.purple;
        } else if (std.mem.eql(u8, ipt, "red")) {
            return Color.red;
        } else if (std.mem.eql(u8, ipt, "salmon")) {
            return Color.salmon;
        } else if (std.mem.eql(u8, ipt, "silver")) {
            return Color.silver;
        } else if (std.mem.eql(u8, ipt, "tan")) {
            return Color.tan;
        } else if (std.mem.eql(u8, ipt, "teal")) {
            return Color.teal;
        } else if (std.mem.eql(u8, ipt, "tomato")) {
            return Color.tomato;
        } else if (std.mem.eql(u8, ipt, "turquoise")) {
            return Color.turquoise;
        } else if (std.mem.eql(u8, ipt, "violet")) {
            return Color.violet;
        } else if (std.mem.eql(u8, ipt, "white")) {
            return Color.white;
        } else if (std.mem.eql(u8, ipt, "yellow")) {
            return Color.yellow;
        }
        return Color.invalid;
    }
};

const BagProperties = struct {
    _type: Type, color: Color
};

const Bag = struct {
    definition: BagProperties, children: [10]?BagProperties, has_shiny_gold: bool = false, visited: bool = false
};

var all_bags: [600]?Bag = [_]?Bag{null} ** 600;

fn can_contain_shiny(bag: *Bag) bool {
    if (bag.visited) {
        return bag.has_shiny_gold;
    }
    var has_shiny_gold = false;
    for (bag.children) |*child_opt| {
        if (child_opt.*) |child| {
            if (child.color == Color.gold and child._type == Type.shiny) {
                has_shiny_gold = true;
                break;
            }
            // We need to dig into all bags to check for can_contain_shiny
            for (all_bags) |*cur_opt| {
                if (cur_opt.*) |*cur| {
                    if (child._type == cur.definition._type and child.color == cur.definition.color) {
                        // We've found the right bag ! Get the info, and GTFO
                        has_shiny_gold = can_contain_shiny(cur) or has_shiny_gold;
                        break;
                    }
                }
            }
        } else {
            break;
        }
    }
    bag.has_shiny_gold = has_shiny_gold;
    bag.visited = true;
    return has_shiny_gold;
}

fn run(input: [:0]u8) u32 {
    var out: u32 = 0;
    var all_lines_it = std.mem.split(input, "\n");

    var bag_number: u16 = 0;

    while (all_lines_it.next()) |line| {
        if (line.len == 0) {
            break;
        }
        var tokenizer = std.mem.tokenize(line, " ,");
        const _type: Type = Type.init(tokenizer.next().?);
        const color: Color = Color.init(tokenizer.next().?);
        var current: Bag = Bag{
            .definition = BagProperties{
                ._type = _type,
                .color = color,
            },
            .children = [_]?BagProperties{null} ** 10,
        };
        var children_counter: u8 = 0;

        _ = tokenizer.next(); // bags
        _ = tokenizer.next(); // contain

        while (tokenizer.next()) |token| {
            if (std.mem.eql(u8, token, "no")) {
                // no other children
                break;
            }
            //const c_count: u8 = @intParse(u8, token, 10) catch unreachable;
            const c_type: Type = Type.init(tokenizer.next().?);
            const c_color: Color = Color.init(tokenizer.next().?);
            var child: BagProperties = BagProperties{
                ._type = c_type,
                .color = c_color,
            };
            _ = tokenizer.next(); // bag(s)
            current.children[children_counter] = child;
            children_counter += 1;
        }
        all_bags[bag_number] = current;
        bag_number += 1;
    }
    run_loop: for (all_bags) |*bag_opt| {
        if (bag_opt.*) |*bag| {
            if (can_contain_shiny(bag)) {
                out += 1;
            }
        } else {
            break :run_loop;
        }
    }
    return out;
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

// TESTS

test "one bag" {
    all_bags = [_]?Bag{null} ** 600;
    var children: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children[0] = BagProperties{ .color = Color.gold, ._type = Type.shiny };
    var test_bag: Bag = Bag{
        .definition = BagProperties{
            .color = Color.red,
            ._type = Type.light,
        },
        .children = children,
    };
    const res = can_contain_shiny(&test_bag);
    std.testing.expect(can_contain_shiny(&test_bag));
}
test "two bags" {
    all_bags = [_]?Bag{null} ** 600;
    // light red bag contain 1 shiny cyan bag
    var children_1: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children_1[0] = BagProperties{ .color = Color.cyan, ._type = Type.shiny };
    var test_bag_1: Bag = Bag{
        .definition = BagProperties{
            .color = Color.red,
            ._type = Type.light,
        },
        .children = children_1,
    };
    // shiny cyan bag contain 1 shiny gold bag
    var children_2: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children_2[0] = BagProperties{ .color = Color.gold, ._type = Type.shiny };
    var test_bag_2: Bag = Bag{
        .definition = BagProperties{
            .color = Color.cyan,
            ._type = Type.shiny,
        },
        .children = children_2,
    };
    all_bags[0] = test_bag_1;
    all_bags[1] = test_bag_2;
    std.testing.expect(can_contain_shiny(&test_bag_1));
}

test "three bags" {
    all_bags = [_]?Bag{null} ** 600;
    // bright purple bag contain 1 light red bag
    var children_0: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children_0[0] = BagProperties{ .color = Color.red, ._type = Type.light };
    var test_bag_0: Bag = Bag{
        .definition = BagProperties{
            .color = Color.purple,
            ._type = Type.bright,
        },
        .children = children_0,
    };
    // light red bag contain 1 shiny cyan bag
    var children_1: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children_1[0] = BagProperties{ .color = Color.cyan, ._type = Type.shiny };
    var test_bag_1: Bag = Bag{
        .definition = BagProperties{
            .color = Color.red,
            ._type = Type.light,
        },
        .children = children_1,
    };
    // shiny cyan bag contain 1 shiny gold bag
    var children_2: [10]?BagProperties = [_]?BagProperties{null} ** 10;
    children_2[0] = BagProperties{ .color = Color.gold, ._type = Type.shiny };
    var test_bag_2: Bag = Bag{
        .definition = BagProperties{
            .color = Color.cyan,
            ._type = Type.shiny,
        },
        .children = children_2,
    };
    all_bags[0] = test_bag_1;
    all_bags[1] = test_bag_2;
    all_bags[2] = test_bag_0;
    std.testing.expect(can_contain_shiny(&test_bag_0));
}

test "run 1" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\light red bag contain 1 shiny gold bag
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 1);
}

test "run 2" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\light red bags contain 1 shiny cyan bag.
        \\vibrant plum bags contain no other bags.
        \\shiny cyan bag contain 1 shiny gold bag
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 2);
}

test "run 3" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\bright purple bags contain 1 light red bag.
        \\light red bags contain 1 shiny cyan bag.
        \\vibrant plum bags contain no other bags.
        \\shiny cyan bag contain 1 shiny gold bag
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 3);
}

test "run 4" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\bright purple bags contain 1 shiny gold bag, 1 light red bag.
        \\light red bags contain 1 vibrant olive bag, 1 shiny cyan bag.
        \\vibrant plum bags contain no other bags.
        \\shiny cyan bag contain 1 shiny gold bag
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 3);
}

test "aoc input" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\light red bags contain 1 bright white bag, 2 muted yellow bags.
        \\dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        \\bright white bags contain 1 shiny gold bag.
        \\muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        \\shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        \\dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        \\vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        \\faded blue bags contain no other bags.
        \\dotted black bags contain no other bags.
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 4);
}

test "error 1" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\muted blue bags contain 3 mirrored tan bags.
        \\dark black bags contain 5 dotted purple bags, 3 dotted orange bags, 5 shiny gold bags, 3 wavy brown bags.
        \\shiny violet bags contain 4 muted blue bags, 2 light purple bags, 5 striped magenta bags, 3 dark black bags.
        \\
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 2);
}

test "error 2" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\dark black bags contain 1 shiny gold bags
        \\shiny violet bags contain 1 dark black bags.
        \\striped crimson bags contain 1 shiny violet bags, 1 striped beige bags
        \\striped beige bags contain no other bags
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 3);
}

test "error 3 - missing dull" {
    all_bags = [_]?Bag{null} ** 600;
    const i =
        \\striped beige bags contain 3 shiny violet bags, 3 striped aqua bags, 3 muted blue bags, 3 shiny gold bags.
        \\dim black bags contain 3 dull tan bags, 2 striped beige bags
        \\
    ;
    var b = i.*;
    const ans = run(&b);
    std.testing.expect(ans == 2);
}
