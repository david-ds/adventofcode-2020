from tool.runners.python import SubmissionPy

from collections import deque

class DavidSubmission(SubmissionPy):

    def parse_mask(self, s):
        # assert(len(s) == 36)
        self.mask_1 = sum(1<<(35-i) for i in range(36) if s[i] == "1")
        self.floating_bits = [35-i for i in range(36) if s[i] == "X"]

    def parse_set(self, s):
        left, right = s.split(" = ")
        val = int(right)
        key = int(left[4:-1])
        return key, val
            
    def apply_mask(self, key):
        q = deque()
        results = []
        key = key | self.mask_1
        q.append((0,key))
        while q:
            i, x = q.pop()
            if i == len(self.floating_bits):
                results.append(x)
                continue

            # set self.floating_bits[i] bit to 0 and 1
            x1 = x|(1<<self.floating_bits[i])
            x0 = x& ~(1<<self.floating_bits[i])
            q.append((i+1, x0))
            q.append((i+1, x1))
        return results

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        register = dict()
        for line in s.split("\n"):
            if line.startswith("mask"):
                self.parse_mask(line[7:])
                continue
        
            original_key, val = self.parse_set(line)
            for derived_key in self.apply_mask(original_key):
                register[derived_key] = val
        
        return sum(register.values())
