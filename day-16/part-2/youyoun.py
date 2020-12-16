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

        # Parse everything
        for i in range(20):
            if s[i] != '':
                class_, range_ = s[i].split(':')
                ranges = [tuple(map(int, x.split('-'))) for x in range_.split(' or ')]
                class_range_map[class_] = ranges
            else:
                break

        my_ticket = list(map(int, s[22].split(',')))
        nearby_tickets = [list(map(int, x.split(','))) for x in s[25:]]

        # Remove invalid tickets
        to_discard = set()
        for i, ticket in enumerate(nearby_tickets):
            for e in ticket:
                is_valid = False
                for r in class_range_map.values():
                    if r[0][0] <= e <= r[0][1] or r[1][0] <= e <= r[1][1]:
                        is_valid = True
                        break
                if is_valid:
                    continue
                to_discard.add(i)
        nearby_tickets = [t for i, t in enumerate(nearby_tickets) if i not in to_discard]

        # List of possible classes for each index of tickets
        ind_poss_class_map = {}
        for i in range(len(my_ticket)):
            possible_classes = set(class_range_map.keys())
            for t in nearby_tickets:
                invalid = set()
                for cls in possible_classes:
                    if not (class_range_map[cls][0][0] <= t[i] <= class_range_map[cls][0][1] or
                            class_range_map[cls][1][0] <= t[i] <= class_range_map[cls][1][1]):
                        invalid.add(cls)
                possible_classes = possible_classes - invalid
            ind_poss_class_map[i] = possible_classes

        # Count number of occurences of each class in all indexes
        class_ind_map = {}
        cls_counter = Counter()
        for p_classes in ind_poss_class_map.values():
            cls_counter.update(Counter(p_classes))

        # Counting occurences results in one class appearing once, a second one appearing twice
        # (once in an index same as the previous class)
        # Meaning that once you assign to the lowest occurence class an index,
        # the next class will only be available for one index.
        i = 0
        while len(class_ind_map) < len(my_ticket):
            cls = sorted(cls_counter.most_common(), key=lambda x: x[1])[i][0]
            for j in ind_poss_class_map:
                if cls in ind_poss_class_map[j]:
                    class_ind_map[cls] = j
                    ind_poss_class_map.pop(j)
                    break
            i += 1

        # Compute results
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


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
