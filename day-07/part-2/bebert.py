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

        return self.add_bags(colors, 'shiny gold') - 1

    def add_bags(self, colors, color):
        sub_bags_color = colors[color][0]
        count = 1
        for sub_bags in sub_bags_color:
            count += sub_bags[0] * self.add_bags(colors, sub_bags[1])
        return count
