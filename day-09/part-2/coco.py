from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        numbers = [int(m) for m in s.strip().split("\n")]
        target = self.part1(numbers)

        pointer1 = 0
        pointer2 = 1

        sum = numbers[pointer1] + numbers[pointer2]

        while True:
            if sum == target:
                candidates = numbers[pointer1 : pointer2 + 1]
                return min(candidates) + max(candidates)
            if sum > target:
                sum -= numbers[pointer1]
                pointer1 += 1
            elif sum < target:
                pointer2 += 1
                sum += numbers[pointer2]


    ##################################
    # PART 1
    def part1(self, numbers):
        candidates = set(numbers[:26])
        for i in range(25, len(numbers)):
            number = numbers[i]
            is_sum = False
            for p in candidates:
                if number - p in candidates and number != 2 * p:
                    is_sum = True
                    break
            candidates.add(number)
            candidates.remove(numbers[i-25])
            if not is_sum:
                return number
