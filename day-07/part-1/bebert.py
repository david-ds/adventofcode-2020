from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        colors = {}
        for line in s.strip().splitlines():
            color, contains_raw = line.split(' bags contain ')
            contains = []
            for c in contains_raw.split(', '):
                parts = c.split(' ')
                if parts[0] == 'no':
                    continue
                contains.append((int(parts[0]), ' '.join(parts[1:-1])))
            colors[color] = [contains, False]

        self.fill_can_contain(colors, 'shiny gold')

        return sum(1 for k, v in colors.items() if v[1])

    def fill_can_contain(self, colors, color):
        for k, v in colors.items():
            if not v[1] and color in (vu[1] for vu in v[0]):
                v[1] = True
                self.fill_can_contain(colors, k)
