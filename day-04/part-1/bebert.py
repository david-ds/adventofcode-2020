from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        chunks1 = s.strip().replace('\r', '').split('\n\n')
        chunks2 = [c.replace('\n', ' ').split(' ') for c in chunks1]
        keys = [{k.split(':')[0] for k in c} for c in chunks2]
        required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']  # , 'cid']

        count = 0
        for k in keys:
            for r in required:
                if r not in k:
                    break
            else:
                count += 1
        return count
