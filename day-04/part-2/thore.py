import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        return sum(self.is_valid_passport(ps) for ps in s.split("\n\n"))

    def is_valid_passport(self, passport_string):
        rows = passport_string.replace("\n", " ").split(" ")
        split_rows = [row.split(":") for row in rows]
        passport = {k: v for k, v in split_rows}

        required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        optional_fields = {"cid"}
        fields = passport.keys()
        if not (fields ^ required_fields).issubset(optional_fields):
            return False

        is_valid_year = lambda s, lower, upper: (
            s.isnumeric() and len(s) == 4 and lower <= int(s) <= upper
        )
        if not is_valid_year(passport["byr"], 1920, 2002):
            return False
        if not is_valid_year(passport["iyr"], 2010, 2020):
            return False
        if not is_valid_year(passport["eyr"], 2020, 2030):
            return False

        hgt = passport["hgt"]
        if hgt.endswith("cm"):
            if not hgt[:-2].isnumeric() or not 150 <= int(hgt[:-2]) <= 193:
                return False
        elif hgt.endswith("in"):
            if not hgt[:-2].isnumeric() or not 59 <= int(hgt[:-2]) <= 76:
                return False
        else:
            return False

        hcl = passport["hcl"]
        if not re.fullmatch("#[0-9a-f]{6}", hcl):
            return False

        ecl = passport["ecl"]
        if not ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        pid = passport["pid"]
        if not pid.isnumeric() or not len(pid) == 9:
            return False

        return True
