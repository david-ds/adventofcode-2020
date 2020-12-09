from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        contains_sg = set()
        bags = {}
        for l in lines:
            container, contains = [x.strip() for x in
                                   l.replace('.', '').replace('bags', '').replace('bag', '').split(" contain ")]
            contains = [x.strip()[2:] for x in contains.split(',')]
            bags[container] = contains
            if 'shiny gold' in contains:
                contains_sg.add(container)
        counter = 0
        stack = contains_sg.copy()
        processed = set()
        while len(stack) > 0:
            curr_b = stack.pop()
            if curr_b in processed:
                continue
            processed.add(curr_b)
            counter += 1
            # Search for parent bag of current bag
            for k, v in bags.items():
                if curr_b in v:
                    stack.add(k)
        return counter
