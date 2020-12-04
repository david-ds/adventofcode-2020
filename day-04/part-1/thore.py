from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        optional_fields = {"cid"}

        valid_passports_count = 0
        for passport in s.split("\n\n"):
            rows = passport.replace("\n", " ").split(" ")
            fields = {tag.split(":")[0] for tag in rows}
            if (fields ^ required_fields).issubset(optional_fields):
                valid_passports_count += 1

        return valid_passports_count
