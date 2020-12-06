from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    mandatory = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    def run(self, input):
        passports = [
            {
                field_value.split(":")[0]
                for field_value in serialized.replace("\n", " ").split(" ")
            }
            for serialized in input.split("\n\n")
        ]
        return sum([passport.issuperset(self.mandatory) for passport in passports])
