from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def check(self, found_keys):
        required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        return all([x in found_keys for x in required_keys])

    def key_validity(self, key, value):
        if key == "cid":
            pass
        elif key == "byr":
            try:
                if len(value) == 4 and 1920 <= int(value) <= 2002:
                    return True
            except ValueError:
                pass
        elif key == "iyr":
            try:
                if len(value) == 4 and 2010 <= int(value) <= 2020:
                    return True
            except ValueError:
                pass
        elif key == "eyr":
            try:
                if len(value) == 4 and 2020 <= int(value) <= 2030:
                    return True
            except ValueError:
                pass
        elif key == "hgt":
            try:
                if (value.endswith("in") and 59 <= int(value[:-2]) <= 76) \
                    or (value.endswith("cm") and 150 <= int(value[:-2]) <= 193):
                    return True
            except ValueError:
                pass
        elif key == "hcl":
            if value.startswith('#') and len(value) == 7 and all([x in "1234567890abcdef" for x in value[1:]]):
                return True
        elif key == "ecl":
            if value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                return True
        elif key == "pid":
            try:
                if len(value) == 9 and int(value):
                    return True
            except ValueError:
                pass
        return False

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        
        counter = 0
        found_keys = set()
        for line in s.split('\n'):
            if len(line) == 0:
                if self.check(found_keys):
                    counter += 1
                found_keys = set()
                continue
            keys = line.split(' ')
            for key in keys:
                key_value, value = key.split(':')
                if self.key_validity(key_value, value):
                    found_keys.add(key_value)
                
        if self.check(found_keys):
            counter += 1
        return counter
