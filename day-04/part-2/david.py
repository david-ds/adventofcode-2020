from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):
    
    @classmethod
    def is_integer_in_range(cls, val, low, high):
        n = int(val)
        return low <= n <= high

    @classmethod
    def is_valid_height(cls, height):
        if height.endswith("cm"):
            return cls.is_integer_in_range(height[:-2], 150, 193)
        elif height.endswith("in"):
            return cls.is_integer_in_range(height[:-2], 59, 76)
        else:
            return False
    
    @classmethod
    def keys_with_constraints(cls):
        return {
        "byr": lambda x: cls.is_integer_in_range(x, 1920, 2002),
        "iyr": lambda x: cls.is_integer_in_range(x, 2010, 2020),
        "eyr": lambda x: cls.is_integer_in_range(x, 2020, 2030),
        "hgt": lambda x: cls.is_valid_height(x),
        "hcl": lambda x: len(x) == 7 and x[0] == "#" and all(c in list("0123456789abcdef") for c in x[1:]),
        "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
        "pid": lambda x: len(x) == 9 and all(c in list("0123456789") for c in x),
    }

    @classmethod
    def is_valid_passport(cls, d):
        return all(key in d and is_valid_field(d[key]) for key, is_valid_field in cls.keys_with_constraints().items())

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        count = 0
        passports = s.split("\n\n")
        for passport_str in passports:
            tags = passport_str.replace("\n", " ").strip().split()
            fields = dict()
            for tag in tags:
                k,v = tag.split(":")
                fields[k] = v
            
            if self.is_valid_passport(fields):
                count += 1
        
        return count
