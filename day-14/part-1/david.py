from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):
    def parse_mask(self, s):
        assert(len(s) == 36)
        self.mask_x = sum(1<<(35-i) for i in range(36) if s[i] == "X")
        self.mask_1  = sum(1<<(35-i) for i in range(36) if s[i] == "1")

    def parse_set(self, s):
        left, right = s.split(" = ")
        val = int(right)
        key = int(left[4:-1])
        return key, val

    def apply_mask(self, val):
        return (val & self.mask_x) | self.mask_1
            
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
        
            key, val = self.parse_set(line)
            register[key] = self.apply_mask(val)
        
        return sum(register.values())
