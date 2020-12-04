from tool.runners.python import SubmissionPy

import re


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n\n"):
            keyvalues = line.split()
            keys = set()

            for keyvalue in keyvalues:
                key, value = keyvalue.split(":")
                keys.add(key)

                if key == "byr" and (int(value) < 1920 or int(value) > 2002):
                    break

                if key == "iyr" and (int(value) < 2010 or int(value) > 2020):
                    break

                if key == "eyr" and (int(value) < 2020 or int(value) > 2030):
                    break

                if key == "hgt":
                    if value.endswith("cm"):
                        if int(value[:-2]) < 150 or int(value[:-2]) > 193:
                            break
                    elif value.endswith("in"):
                        if int(value[:-2]) < 59 or int(value[:-2]) > 76:
                            break
                    else:
                        break

                if key == "hcl" and re.match(r"^#[0-9a-f]{6}$", value) is None:
                    break

                if key == "ecl" and value not in {
                    "amb",
                    "blu",
                    "brn",
                    "gry",
                    "grn",
                    "hzl",
                    "oth",
                }:
                    break

                if key == "pid" and re.match(r"^\d{9}$", value) is None:
                    break
            else:
                if {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} <= keys:
                    result += 1

        return result
