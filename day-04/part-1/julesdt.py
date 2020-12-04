from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def check(self, found_keys):
        required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        return all([x in found_keys for x in required_keys])

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
                key_value = key.split(':')[0]
                found_keys.add(key_value)
        if self.check(found_keys):
            counter += 1
        return counter
