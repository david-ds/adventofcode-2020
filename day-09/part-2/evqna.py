from tool.runners.python import SubmissionPy

PREAMBLE_LENGTH = 25

class EvqnaSubmission(SubmissionPy):

    def is_valid(self, n, preamble):
        for x in preamble:
            if n - x != x and n - x in preamble:
                return True
        return False
    
    def first_invalid_num(self, nums):
        preamble = set(nums[:PREAMBLE_LENGTH])

        for i in range(PREAMBLE_LENGTH, len(nums)):
            n = nums[i]
            if not self.is_valid(n, preamble):
                return n
            preamble.remove(nums[i - PREAMBLE_LENGTH])
            preamble.add(n)
    
    def find_range_with_sum(self, nums, target):
        i, j = 0, 2
        s = sum(nums[i:j])
        while s != target:
            if s < target:
                s += nums[j]
                j += 1
            else:
                s -= nums[i]
                i += 1
        return nums[i:j]

    def run(self, s):
        nums = [int(n) for n in s.splitlines()]
        x = self.first_invalid_num(nums)
        L = self.find_range_with_sum(nums, x)
        return min(L) + max(L)

