from tool.runners.python import SubmissionPy
from collections import Counter

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        numbers = [int(n) for n in s.split("\n")]
        numbers.append(max(numbers) + 3)
        numbers.append(0)
        numbers = sorted(numbers)
        
        number_ways_to_reach = [0] * (max(numbers) + 1)
        number_ways_to_reach[0] = 1

        for n in numbers[1:]:

            number_ways_to_reach[n] += number_ways_to_reach[n-1] 
            if n >= 2:
                number_ways_to_reach[n] += number_ways_to_reach[n-2]
            if n >= 3:
                number_ways_to_reach[n] += number_ways_to_reach[n-3]

        return number_ways_to_reach[-1]
