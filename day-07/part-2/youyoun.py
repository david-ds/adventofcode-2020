from tool.runners.python import SubmissionPy

def count_bags(G, bag):
    c = 0
    if len(G[bag]) == 0:
        return 1
    for b in G[bag]:
        c += b[1] * count_bags(G, b[0])
    return c + 1


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        bags = {}
        for l in lines:
            container, contains = [x.strip() for x in
                                   l.replace('.', '').replace('bags', '').replace('bag', '').split(" contain ")]
            contains_2 = []
            for x in contains.split(','):
                bag, quant = x[2:].replace('other', '').strip(), int(x.strip()[:2].replace('no', '0'))
                if quant > 0:
                    contains_2.append((bag, quant))
            bags[container] = contains_2
        counter = count_bags(bags, 'shiny gold') - 1
        return counter
