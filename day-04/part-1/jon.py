from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        l = s.strip().split("\n\n")
        count = 0

        for p in l:
            keys = {f.split(":")[0] for f in p.split()}
            if len(keys) == 8 or (len(keys) == 7 and "cid" not in keys):
                count += 1

        return count
