from tool.runners.python import SubmissionPy

def euclid(a, b):
    '''Returns r, u, v such that r = a*u + b*v and r = gcd(a, b)
    '''
    r, u, v, r2, u2, v2 = a, 1, 0, b, 0, 1
    while r2 != 0:
        q = r // r2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q*r2, u - q*u2, v - q*v2
    return r, u, v

class EvqnaSubmission(SubmissionPy):

    def modular_inverse(self, x, n):
        r, u, _ = euclid(x, n)
        assert r == 1
        return u

    def solve_CRT(self, equations):
        N = 1
        for _, mod in equations:
            N *= mod

        result = 0
        for residue, mod in equations:
            x = N // mod
            y = self.modular_inverse(x, mod)
            result += residue * x * y
        return result % N

    def run(self, s):
        _, ids = s.splitlines()
        constraints = []
        for i, bus in enumerate(ids.split(',')):
            if bus != 'x':
                constraints.append((-i, int(bus)))
        
        return self.solve_CRT(constraints)
