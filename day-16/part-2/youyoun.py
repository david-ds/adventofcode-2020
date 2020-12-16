from tool.runners.python import SubmissionPy
from collections import Counter


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        class_range_map = {}
        i = 0
        while True:
            if s[i] != '':
                class_, range_ = s[i].split(':')
                ranges = [tuple(map(int, x.split('-'))) for x in range_.split(' or ')]
                class_range_map[class_] = ranges
                i += 1
            else:
                break

        my_ticket = list(map(int, s[i + 2].split(',')))
        nearby_tickets = [list(map(int, x.split(','))) for x in s[i + 5:]]

        possible_vals = set()
        for ranges in class_range_map.values():
            for range_ in ranges:
                for i in range(range_[0], range_[1] + 1):
                    possible_vals.add(i)

        to_discard = set()
        for i, ticket in enumerate(nearby_tickets):
            for e in ticket:
                if e not in possible_vals:
                    to_discard.add(i)
                    break
        nearby_tickets = [t for i, t in enumerate(nearby_tickets) if i not in to_discard]

        ind_poss_class_map = {}
        for i in range(len(my_ticket)):
            possible_classes = set(class_range_map.keys())
            for t in nearby_tickets:
                invalid = set()
                for cls in possible_classes:
                    if not (class_range_map[cls][0][0] <= t[i] <= class_range_map[cls][0][1] or class_range_map[cls][1][0] <= t[i] <= class_range_map[cls][1][1]):
                        invalid.add(cls)
                for e in invalid:
                    possible_classes.remove(e)
            ind_poss_class_map[i] = possible_classes

        class_ind_map = {}
        while len(class_ind_map) < len(my_ticket):
            cls_counter = Counter()
            for p_classes in ind_poss_class_map.values():
                cls_counter.update(Counter(p_classes))
            cls = sorted(cls_counter.most_common(), key=lambda x: x[1])[0][0]
            for i in ind_poss_class_map:
                if cls in ind_poss_class_map[i]:
                    class_ind_map[cls] = i
                    ind_poss_class_map.pop(i)
                    break
        keys_of_interest = {'departure location',
                            'departure station',
                            'departure platform',
                            'departure track',
                            'departure date',
                            'departure time'}
        score = 1
        for k in keys_of_interest:
            score *= my_ticket[class_ind_map[k]]
        return score
