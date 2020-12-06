from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    validation = {
        "byr": lambda v: cast_to_int(v, 1920, 2002),
        "iyr": lambda v: cast_to_int(v, 2010, 2020),
        "eyr": lambda v: cast_to_int(v, 2020, 2030),
        "hgt": lambda v: validate_height(v),
        "hcl": lambda v: len(v) == 7
        and v[0] == "#"
        and all(c in "0123456789abcdef" for c in v[1:]),
        "ecl": lambda v: v in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda v: cast_to_int(v, digits=9),
    }

    def run(self, input):
        passports = [
            dict(
                field_value.split(":")
                for field_value in serialized.replace("\n", " ").split(" ")
            )
            for serialized in input.split("\n\n")
        ]
        return sum([self._is_valid(passport) for passport in passports])

    def _is_valid(self, passport):
        return all(
            field in passport and validate(passport[field])
            for field, validate in self.validation.items()
        )


def cast_to_int(val, mini=None, maxi=None, digits=4):
    if len(val) != digits:
        return False
    try:
        nb = int(val)
        return mini <= nb <= maxi if mini and maxi else True
    except ValueError:
        return False


def validate_height(val):
    if len(val) < 2:
        return False

    if val[-2:] == "cm":
        return cast_to_int(val[:-2], 150, 193, digits=3)
    elif val[-2:] == "in":
        return cast_to_int(val[:-2], 59, 76, digits=2)

    return False
