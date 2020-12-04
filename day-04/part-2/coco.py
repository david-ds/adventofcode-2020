from tool.runners.python import SubmissionPy

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        # Your code goes here
        required_fields = ["byr", "iyr", "eyr","hgt","hcl","ecl","pid"]
        hex_characters = set("0123456789abcdef")
        numbers = set("0123456789")
        eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        lines = s.strip().split("\n\n")
        n_valid = 0

        for l in lines:
            # Parsing
            field_value = l.replace("\n", " ").split()
            field_value = [f.split(':') for f in field_value]
            fields = dict(field_value)

            # Validating
            if not all(r in fields for r in required_fields):
                continue
            
            if len(fields["byr"]) != 4 or int(fields["byr"]) < 1920 or int(fields["byr"]) > 2002:
                continue

            if len(fields["iyr"]) != 4 or int(fields["iyr"]) < 2010 or int(fields["iyr"]) > 2020:
                continue

            if len(fields["eyr"]) != 4 or int(fields["eyr"]) < 2020 or int(fields["eyr"]) > 2030:
                continue
            
            if fields["hgt"].endswith("cm"):
                if int(fields["hgt"][:-2]) < 150 or int(fields["hgt"][:-2]) > 193:
                    continue
            elif fields["hgt"].endswith("in"):
                if int(fields["hgt"][:-2]) < 59 or int(fields["hgt"][:-2]) > 76:
                    continue
            else:
                continue

            if (not fields["hcl"].startswith("#")) or len(fields["hcl"]) != 7:
                continue
            if not all(c in hex_characters for c in fields["hcl"][1:]):
                continue

            if fields["ecl"] not in eye_colors:
                continue

            if len(fields["pid"]) != 9:
                continue
            if not all(c in numbers for c in fields["pid"]):
                continue
            
            n_valid += 1

        return n_valid
