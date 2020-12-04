from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        chunks1 = s.strip().replace('\r', '').split('\n\n')
        chunks2 = [c.replace('\n', ' ').split(' ') for c in chunks1]
        keys = [{k.split(':')[0]: k.split(':')[1] for k in c} for c in chunks2]
        required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']  # , 'cid']

        numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        hex_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
        eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

        count = 0
        for k in keys:
            if any(r not in k for r in required):
                continue

            byr = int(k['byr'])
            if byr < 1920 or byr > 2002:
                continue

            iyr = int(k['iyr'])
            if iyr < 2010 or iyr > 2020:
                continue

            eyr = int(k['eyr'])
            if eyr < 2020 or eyr > 2030:
                continue

            if k['hgt'][-2:] == 'in':
                hgt = int(k['hgt'][:-2])
                if hgt < 59 or hgt > 76:
                    continue
            elif k['hgt'][-2:] == 'cm':
                hgt = int(k['hgt'][:-2])
                if hgt < 150 or hgt > 193:
                    continue
            else:
                continue

            if k['hcl'][0] != '#' or len(k['hcl']) != 7 or any(c not in hex_chars for c in k['hcl'][1:]):
                continue

            if k['ecl'] not in eye_colors:
                continue

            if len(k['pid']) != 9 or any(c for c in k['pid'] if c not in numbers):
                continue

            count += 1

        return count
