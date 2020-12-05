from tool.runners.python import SubmissionPy

import re


class JonSubmission(SubmissionPy):

    def run(self, s):
        l = s.strip().split("\n\n")
        count = 0

        for p in l:
            d = {k: v for k, v in (f.split(":") for f in p.split())}
            if is_valid(d):
                count += 1

        return count


is_4digits = re.compile(r"\d{4}").fullmatch
is_height_cm = re.compile(r"\d{3}cm").fullmatch
is_height_in = re.compile(r"\d{2}in").fullmatch
is_hex_color = re.compile(r"#[0-9a-f]{6}").fullmatch
eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
is_9digits = re.compile(r"\d{9}").fullmatch


def is_valid(d):
    if len(d) < 7 or (len(d) == 7 and "cid" in d):
        return False

    byr = d.get("byr", "")
    iyr = d.get("iyr", "")
    eyr = d.get("eyr", "")
    hgt = d.get("hgt", "")
    hcl = d.get("hcl", "")
    ecl = d.get("ecl", "")
    pid = d.get("pid", "")

    return (
        is_4digits(byr) and 1920 <= int(byr) <= 2002
        and is_4digits(iyr) and 2010 <= int(iyr) <= 2020
        and is_4digits(eyr) and 2020 <= int(eyr) <= 2030
        and (
            (is_height_cm(hgt) and 150 <= int(hgt[:-2]) <= 193)
            or (is_height_in(hgt) and 59 <= int(hgt[:-2]) <= 76)
        )
        and is_hex_color(hcl)
        and ecl in eye_colors
        and is_9digits(pid)
    )
