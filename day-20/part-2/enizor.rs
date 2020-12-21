#![allow(dead_code)]
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut pos = 5;
    let bytes = input.as_bytes();
    let mut tiles = Vec::new();
    while pos < bytes.len() {
        let mut tile = Tile::from_str(bytes, &mut pos);
        match_sides(&mut tiles, &mut tile);
        tiles.push(tile);
        pos += 7;
    }
    let img = Image::from_tiles(&mut tiles);
    let count_mstr = img.find_monsters();
    img.count_water() - count_mstr
}

// Sides:
//  1
// 2 1 rotating direct
//  3
#[derive(PartialEq, Eq)]
struct Tile {
    number: i16,
    sides: [(u16, Option<i16>); 4],
    photo: Photo,
}

impl Tile {
    fn from_str(input: &[u8], pos: &mut usize) -> Self {
        // let mut pos = 5;
        let mut number = 0;
        while *pos < input.len() {
            let c = input[*pos];
            if (b'0'..=b'9').contains(&c) {
                number *= 10;
                number += (c - b'0') as i16;
                *pos += 1;
            } else {
                break;
            }
        }
        let mut sides = [(0, None); 4];
        *pos += 2;
        let mut line_length = 0;
        let mut line = 0;
        // Parse top line
        loop {
            if input[*pos] == b'\n' {
                sides[0].0 = sides[1].0 & 0b10;
                line += 1;
                break;
            } else if input[*pos] == b'#' {
                sides[1].0 += 1;
            }
            if line_length == 0 {
                sides[2].0 = sides[1].0;
                sides[2].0 <<= 1;
            }
            sides[1].0 <<= 1;
            line_length += 1;
            *pos += 1;
        }
        assert!(line_length == 10);
        sides[1].0 <<= 2;
        sides[1].0 = reverse_u16(sides[1].0);
        *pos += 1;
        let mut photo = Photo([0; 8]);
        let mut line_pos = 0;
        while line < line_length - 1 {
            if input[*pos] == b'#' {
                sides[2].0 += 1;
            }
            sides[2].0 <<= 1;
            line_pos += 1;
            *pos += 1;
            while line_pos < line_length - 1 {
                if input[*pos] == b'#' {
                    photo.0[line - 1] |= 1 << (8 - line_pos);
                }
                *pos += 1;
                line_pos += 1;
            }
            if input[*pos] == b'#' {
                sides[0].0 += 1;
            }
            sides[0].0 <<= 1;

            line += 1;
            *pos += 2;
            line_pos = 0;
        }
        // Parse last line
        let mut line_pos = 0;
        while *pos < input.len() {
            if input[*pos] == b'\n' {
                break;
            }
            if input[*pos] == b'#' {
                sides[3].0 += 1;
            }
            sides[3].0 <<= 1;
            if line_pos == 0 {
                if input[*pos] == b'#' {
                    sides[2].0 += 1;
                }
                sides[2].0 <<= 1;
            }
            if line_pos == line_length - 1 {
                if input[*pos] == b'#' {
                    sides[0].0 += 1;
                }
                sides[0].0 <<= 1;
            }
            line_pos += 1;
            *pos += 1;
        }
        sides[0].0 <<= 2;
        sides[2].0 <<= 2;
        sides[3].0 <<= 2;
        sides[0].0 = reverse_u16(sides[0].0);
        Self {
            number,
            sides,
            photo,
        }
    }

    fn flip_x(&mut self) {
        self.sides.swap(1, 3);
        for s in self.sides.iter_mut() {
            s.1 = s.1.map(|x| -x);
            s.0 = reverse_u16(s.0);
        }
        self.photo.flip_x();
    }

    fn flip_y(&mut self) {
        self.sides.swap(0, 2);
        for s in self.sides.iter_mut() {
            s.1 = s.1.map(|x| -x);
            s.0 = reverse_u16(s.0);
        }
        self.photo.flip_y();
    }

    fn rotate_direct(&mut self) {
        self.sides.rotate_right(1);
        self.photo.rotate_direct();
    }

    fn rotate_indirect(&mut self) {
        self.sides.rotate_left(1);
        self.photo.rotate_indirect();
    }
}

impl std::fmt::Debug for Tile {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt.debug_struct("Tile")
            .field("number", &self.number)
            .field(
                "side 0",
                &format!("{:b} {:?}", self.sides[0].0, self.sides[0].1),
            )
            .field(
                "side 1",
                &format!("{:b} {:?}", self.sides[1].0, self.sides[1].1),
            )
            .field(
                "side 2",
                &format!("{:b} {:?}", self.sides[2].0, self.sides[2].1),
            )
            .field(
                "side 3",
                &format!("{:b} {:?}", self.sides[3].0, self.sides[3].1),
            )
            .field("photo", &self.photo)
            .finish()
    }
}

fn match_sides(tiles: &mut [Tile], new_tile: &mut Tile) {
    let mut sides_rev: Vec<u16> = new_tile.sides.iter().map(|&b| reverse_u16(b.0)).collect();
    let mut count = 0;
    for tile in tiles.iter_mut() {
        for side in tile.sides.iter_mut() {
            if side.1.is_none() {
                for (new_side, new_side_rev) in new_tile.sides.iter_mut().zip(sides_rev.iter_mut())
                {
                    if new_side.0 == side.0 {
                        side.1 = Some(-new_tile.number);
                        new_side.1 = Some(tile.number);
                        count += 1;
                        break;
                    } else if *new_side_rev == side.0 {
                        side.1 = Some(new_tile.number);
                        new_side.1 = Some(tile.number);
                        count += 1;
                        break;
                    }
                }
                if count == 4 {
                    return;
                }
            }
        }
    }
}

fn reverse_u16(mut b: u16) -> u16 {
    let mut s = 16;
    let mut r = 0;
    while b > 0 {
        r <<= 1;
        r |= b & 1;
        s -= 1;
        b >>= 1;
    }
    r <<= s;
    r
}

fn reverse_u8(mut b: u8) -> u8 {
    let mut s = 8;
    let mut r = 0;
    while b > 0 {
        r <<= 1;
        r |= b & 1;
        s -= 1;
        b >>= 1;
    }
    r <<= s;
    r
}

#[derive(Clone, Copy, PartialEq, Eq)]
// A 8*8 bitmap
struct Photo([u8; 8]);

impl Photo {
    // flips top and bottom
    fn flip_x(&mut self) {
        for i in 0..4 {
            self.0.swap(i, 8 - i - 1);
        }
    }

    // flips left and right
    fn flip_y(&mut self) {
        for x in self.0.iter_mut() {
            *x = reverse_u8(*x);
        }
    }

    // rotate 90, direct
    // .......#  #...#...
    // ......#.  .#..#...
    // .....#..  ..#.#...
    // ....#...  ...##...
    // ########  ....#...
    // ..#.....  ....##..
    // .#......  ....#.#.
    // #.......  ....#..#
    fn rotate_direct(&mut self) {
        let mut new = [0; 8];
        for (j, &b) in self.0.iter().enumerate() {
            for (i, newb) in new.iter_mut().enumerate() {
                *newb |= ((b >> i) & 1) << (7 - j);
            }
        }
        self.0 = new;
    }

    // rotate 90, indirect
    // .......#  #...#...
    // ......#.  .#..#...
    // .....#..  ..#.#...
    // ....#...  ...##...
    // ########  ....#...
    // ..#.....  ....##..
    // .#......  ....#.#.
    // #.......  ....#..#
    fn rotate_indirect(&mut self) {
        let mut new = [0; 8];
        for (j, &b) in self.0.iter().enumerate() {
            for (i, newb) in new.iter_mut().enumerate() {
                *newb |= ((b >> (7 - i)) & 1) << j;
            }
        }
        self.0 = new;
    }
}

impl std::fmt::Debug for Photo {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for line in &self.0 {
            fmt.write_str(
                &format!("\n{:08b}", line)
                    .replace('0', ".")
                    .replace('1', "#"),
            )?
        }
        Ok(())
    }
}

struct Image {
    length: usize,
    width: usize,
    inner: Vec<Photo>,
}

impl Image {
    fn from_tiles(tiles: &mut [Tile]) -> Self {
        let mut corners = [(0, 0); 4];
        let mut corners_count = 0;
        let mut length = 0;
        let mut width = 0;
        let mut photos = Vec::with_capacity(tiles.len());
        // Find corners
        for (i, tile) in tiles.iter().enumerate() {
            if tile.sides.iter().filter(|&&s| s.1.is_none()).count() == 2 {
                corners[corners_count] = (i, tile.number);
                corners_count += 1;
            }
            if corners_count == 4 {
                break;
            }
        }
        // Orientate first corner
        let first_corner = &mut tiles[corners[0].0];
        if first_corner.sides[1].1.is_some() {
            if first_corner.sides[0].1.is_some() {
                first_corner.rotate_indirect();
            } else {
                first_corner.flip_x();
                first_corner.flip_y();
            }
        } else if first_corner.sides[2].1.is_some() {
            first_corner.rotate_direct();
        }
        assert!(first_corner.sides[0].1.is_some());
        assert!(first_corner.sides[1].1.is_none());
        assert!(first_corner.sides[2].1.is_none());
        assert!(first_corner.sides[3].1.is_some());
        // TODO: matching example to help debug
        first_corner.rotate_direct();
        first_corner.flip_x();

        assert!(first_corner.sides[0].1.is_some());
        assert!(first_corner.sides[1].1.is_none());
        assert!(first_corner.sides[2].1.is_none());
        assert!(first_corner.sides[3].1.is_some());

        photos.push(first_corner.photo);
        let mut next_place;
        let mut previous_place = corners[0].0;
        let mut leftmost_place = previous_place;
        let mut direction = 0;
        // got right
        let mut i = 1;
        loop {
            next_place = find_matching_tile(tiles, &tiles[previous_place], direction);
            place_tile(tiles, previous_place, next_place, direction);
            photos.push(tiles[next_place].photo);
            if i == 0 {
                leftmost_place = next_place;
            }
            previous_place = next_place;
            i += 1;
            if i != 1 && (i == width || corners.iter().any(|(place, _)| *place == previous_place)) {
                if i == width && corners.iter().any(|(place, _)| *place == previous_place) {
                    break;
                }
                // Comput width & length at first line
                if width == 0 {
                    width = i;
                    length = tiles.len() / width;
                }
                // go downward once
                direction = 3;
                previous_place = leftmost_place;
                i = 0;
            } else {
                direction = 0;
            }
        }
        Self {
            width,
            length,
            inner: photos,
        }
    }

    fn find_monsters(&self) -> usize {
        // let mut new_img = Image{
        //     width: self.width,
        //     length: self.length,
        //     inner: vec![Photo([0;8]); self.width*self.length],
        // };
        let monsters = Monster::generate();
        for m in monsters[..].iter() {
            // let mut found = false;
            let mut count = 0;
            for line in 0..=(self.length * 8 - m.length) {
                for width in 0..=(self.width * 8 - m.width) {
                    if self.test_for_monster(line, width, &m) {
                        count += 1;
                        // found = true;
                        // new_img.place_monster(line, width, &m);
                    }
                }
            }
            if count > 0 {
                // if found {
                return count * monsters[0].size();
                // return new_img.count_water()
            }
        }
        0
    }

    fn test_for_monster(&self, line: usize, width: usize, mon: &Monster) -> bool {
        let offset = width % 8;
        for l in 0..mon.length {
            let to_match = mon.value[l * mon.inner_width] >> offset;
            let photo = self.inner[(width / 8) + ((l + line) / 8) * self.length].0[(l + line) % 8];
            if photo & to_match != to_match {
                return false;
            }
            for w in 1..mon.inner_width {
                let mut to_match = if offset == 0 {
                    0
                } else {
                    mon.value[w - 1 + l * mon.inner_width] << (8 - offset)
                };
                to_match |= mon.value[w + l * mon.inner_width] >> offset;
                let photo =
                    self.inner[w + (width / 8) + ((l + line) / 8) * self.length].0[(l + line) % 8];
                if photo & to_match != to_match {
                    return false;
                }
            }
            if offset > 8 - mon.width {
                let to_match = mon.value[(l + 1) * mon.inner_width - 1] << (8 - offset);
                let photo = self.inner
                    [mon.inner_width + (width / 8) + ((l + line) / 8) * self.length]
                    .0[(l + line) % 8];
                if photo & to_match != to_match {
                    return false;
                }
            }
        }
        true
    }

    #[allow(dead_code)]
    // Use if monsters can overlap
    // Apparently they don't
    fn place_monster(&mut self, line: usize, width: usize, mon: &Monster) {
        let offset = width % 8;
        for l in 0..mon.length {
            let to_match = mon.value[l * mon.inner_width] >> offset;
            let photo =
                &mut self.inner[(width / 8) + ((l + line) / 8) * self.length].0[(l + line) % 8];
            *photo |= to_match;
            for w in 1..mon.inner_width {
                let mut to_match = if offset == 0 {
                    0
                } else {
                    mon.value[w - 1 + l * mon.inner_width] << (8 - offset)
                };
                to_match |= mon.value[w + l * mon.inner_width] >> offset;
                let photo = &mut self.inner[w + (width / 8) + ((l + line) / 8) * self.length].0
                    [(l + line) % 8];
                *photo |= to_match;
            }
            if offset > 8 - mon.width {
                let to_match = mon.value[(l + 1) * mon.inner_width - 1] << (8 - offset);
                let photo = &mut self.inner
                    [mon.inner_width + (width / 8) + ((l + line) / 8) * self.length]
                    .0[(l + line) % 8];
                *photo |= to_match;
            }
        }
    }

    fn count_water(&self) -> usize {
        self.inner.iter().fold(0, |acc, p| {
            acc + p.0.iter().fold(0, |c, b| c + b.count_ones())
        }) as usize
    }
}

impl std::fmt::Debug for Image {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt.write_str("\n")?;
        fmt.write_fmt(format_args!(
            "width: {}\nlength: {}\n",
            self.width, self.length
        ))?;
        for line in 0..self.length {
            let photos = &self.inner[line * self.width..(line + 1) * self.width];
            for subline in 0..8 {
                for &p in photos {
                    fmt.write_str(
                        &format!("{:08b}", p.0[subline])
                            .replace('0', ".")
                            .replace('1', "#"),
                    )?;
                }
                fmt.write_str("\n")?;
            }
        }
        Ok(())
    }
}

fn find_matching_tile(tiles: &[Tile], tile: &Tile, direction: usize) -> usize {
    let next_id = tile.sides[direction]
        .1
        .unwrap_or_else(|| panic!("No possible tiles in this direction {}", direction));
    let next_tile = tiles
        .iter()
        .enumerate()
        .find(|(_i, t)| t.number == next_id.abs())
        .expect("No matching tile")
        .0;
    next_tile
}

// Reorient the tile for the given direction
// Only works for rightwards & downward
fn place_tile(tiles: &mut [Tile], previous_place: usize, next_place: usize, direction: usize) {
    let previous_id = tiles[previous_place].number;
    let previous_link = tiles[previous_place].sides[direction].1.unwrap();
    let next_tile = &mut tiles[next_place];
    let side = next_tile
        .sides
        .iter()
        .enumerate()
        .find(|(_i, &s)| s.1.unwrap_or(0).abs() == previous_id)
        .unwrap()
        .0;
    // Reorient tile
    if direction == 0 {
        match side {
            0 => next_tile.flip_y(),
            1 => next_tile.rotate_direct(),
            2 => (),
            3 => next_tile.rotate_indirect(),
            _ => unreachable!(),
        }
        // Flip if needed
        if next_tile.sides[2].1.unwrap() as isize * (previous_link as isize) < 0 {
            next_tile.flip_x();
        }
    }
    if direction == 3 {
        match side {
            1 => (),
            0 => next_tile.rotate_direct(),
            3 => next_tile.flip_x(),
            2 => next_tile.rotate_indirect(),
            _ => unreachable!(),
        }
        // Flip if needed
        if next_tile.sides[1].1.unwrap() as isize * (previous_link as isize) < 0 {
            next_tile.flip_y();
        }
    }
}

const BASE_MONSTER: &str = "\
..................#.
#....##....##....###
.#..#..#..#..#..#...";

const FLIPPED_MONSTER: &str = "\
.#..#..#..#..#..#...
#....##....##....###
..................#.";

const ROTATED_MONSTER: &str = "\
.#.
#..
...
...
#..
.#.
.#.
#..
...
...
#..
.#.
.#.
#..
...
...
#..
.#.
.##
.#.";

#[derive(Clone)]
struct Monster {
    width: usize,
    inner_width: usize,
    length: usize,
    value: Vec<u8>,
}

impl Monster {
    fn from_str(base: &[u8]) -> Self {
        let mut width = 0;
        let mut length = 0;
        let mut value = Vec::new();
        let mut pos = 0;
        let mut byte = 0;
        let mut byte_pos = 7;
        let mut inner_width = 0;
        while pos < base.len() {
            let c = base[pos];
            if c == b'\n' {
                length += 1;
                if byte_pos != 7 {
                    value.push(byte);
                    if length == 1 {
                        inner_width += 1;
                    }
                    byte = 0;
                }
                byte_pos = 7;
            } else {
                if length == 0 {
                    width += 1;
                }
                if c == b'#' {
                    byte |= 1 << byte_pos;
                }
                if byte_pos == 0 {
                    value.push(byte);
                    if length == 0 {
                        inner_width += 1;
                    }
                    byte = 0;
                    byte_pos = 7;
                } else {
                    byte_pos -= 1;
                }
            }
            pos += 1;
        }
        length += 1;
        if byte_pos != 7 {
            value.push(byte);
        }
        Self {
            width,
            inner_width,
            length,
            value,
        }
    }

    fn flip(&self) -> Self {
        let width = self.width;
        let length = self.length;
        let inner_width = self.inner_width;
        let mut value = self.value.clone();
        for l in 0..length / 2 {
            for i in 0..inner_width {
                value.swap(i + l * inner_width, i + (length - 1 - l) * inner_width);
            }
        }
        Self {
            width,
            inner_width,
            length,
            value,
        }
    }

    fn rotate_indirect(&self) -> Self {
        let width = self.length;
        let length = self.width;
        let inner_width = self.length / 8 + 1;
        let mut value = vec![0; inner_width * length];

        for pos in 0..length * width {
            let new_line = pos / width;
            let old_line = self.length - 1 - pos % self.length;
            let new_col = pos % width;
            let new_offset = 7 - (new_col % 8);
            let old_col = pos / self.length;
            let old_offset = 7 - (old_col % 8);
            value[new_col / 8 + new_line * inner_width] |=
                ((self.value[old_col / 8 + old_line * self.inner_width] & (1 << old_offset))
                    >> old_offset)
                    << new_offset;
        }
        Self {
            width,
            inner_width,
            length,
            value,
        }
    }

    fn generate() -> [Self; 8] {
        let base = Monster::from_str(BASE_MONSTER.as_bytes());
        let r1 = base.rotate_indirect();
        let r2 = r1.rotate_indirect();
        let r3 = r2.rotate_indirect();
        [
            base.flip(),
            base,
            r1.flip(),
            r1,
            r2.flip(),
            r2,
            r3.flip(),
            r3,
        ]
    }

    fn size(&self) -> usize {
        self.value.iter().fold(0, |acc, b| acc + b.count_ones()) as usize
    }
}

impl std::fmt::Debug for Monster {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt.write_str("\n")?;
        fmt.write_fmt(format_args!(
            "width: {}\ninner width: {}\nlength: {}\n",
            self.width, self.inner_width, self.length
        ))?;
        for line in 0..self.length {
            for w in 0..self.inner_width - 1 {
                fmt.write_str(
                    &format!("{:08b}", self.value[w + line * self.inner_width])
                        .replace('0', ".")
                        .replace('1', "#"),
                )?;
            }
            for i in 0..self.width % 8 {
                if self.value[(line + 1) * self.inner_width - 1] & (1 << (7 - i)) != 0 {
                    fmt.write_str("#")?;
                } else {
                    fmt.write_str(".")?;
                }
            }
            fmt.write_str("\n")?;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn monster_test() {
        let mons = Monster::from_str(BASE_MONSTER.as_bytes());
        assert_eq!(
            format!("{:?}", mons),
            "\nwidth: 20\ninner width: 3\nlength: 3\n".to_string() + BASE_MONSTER + "\n"
        );
        let flipped = mons.flip();
        assert_eq!(
            format!("{:?}", flipped),
            "\nwidth: 20\ninner width: 3\nlength: 3\n".to_string() + FLIPPED_MONSTER + "\n"
        );
        let rotated = mons.rotate_indirect();
        assert_eq!(
            format!("{:?}", rotated),
            "\nwidth: 3\ninner width: 1\nlength: 20\n".to_string() + ROTATED_MONSTER + "\n"
        );
    }

    #[test]
    fn photo_test() {
        let mut photo = Photo([1, 2, 4, 126, 16, 32, 64, 128]);
        photo.flip_x();
        assert_eq!(photo, Photo([128, 64, 32, 16, 126, 4, 2, 1]));
        photo.flip_y();
        assert_eq!(photo, Photo([1, 2, 4, 8, 126, 32, 64, 128]));
        photo.rotate_direct();
        assert_eq!(
            photo,
            Photo([
                0b10000000, 0b01001000, 0b00101000, 0b00011000, 0b00001000, 0b00001100, 0b00001010,
                0b00000001
            ])
        );
        photo.rotate_indirect();
        assert_eq!(photo, Photo([1, 2, 4, 8, 126, 32, 64, 128]));
    }

    #[test]
    fn reverse_test() {
        assert_eq!(reverse_u16(0b1011010000), 0b0000101101000000)
    }

    #[test]
    fn parse_test() {
        let tile = r#"Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
#.###..###
"#;
        assert_eq!(
            Tile::from_str(tile.as_bytes(), &mut 5),
            Tile {
                number: 2311,
                sides: [
                    (0b1001101000000, None),
                    (0b100101100000, None),
                    (0b111110011000, None),
                    (0b1011100111000, None),
                ],
                photo: Photo([
                    0b10010000, 0b00011001, 0b11101000, 0b10110111, 0b10001011, 0b10101001,
                    0b01000010, 0b11000101
                ]),
            }
        )
    }

    #[test]
    fn run_test() {
        let tiles = r#"Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."#;
        assert_eq!(run(tiles), 273)
    }
}
