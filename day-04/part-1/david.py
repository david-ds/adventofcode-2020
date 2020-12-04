from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def is_valid_passport(self, fields):
        if len(fields) == 8:
            return True

        return len(fields) == 7 and "cid" not in fields

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
