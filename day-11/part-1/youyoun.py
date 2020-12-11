from tool.runners.python import SubmissionPy
import numpy as np
from scipy.signal import convolve2d

dirs = {(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)}
char_int_map = {
    'L': 1,
    '#': -1,
    '.': 0
}


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        m = np.array([[char_int_map[x] for x in list(l)] for l in s.splitlines()])
        ker = np.ones((3, 3))
        ker[1, 1] = 0
        adj_seats = convolve2d(np.abs(m), ker, mode='same') * np.abs(m)
        adj_seats[adj_seats == 0] = -1000
        while True:
            free = m == 1
            occ = m == -1
            m2 = convolve2d(free, ker, mode='same') * free - convolve2d(occ, ker, mode='same') * occ
            if (m2 <= -4).sum() == 0 and (m2 == adj_seats).sum() == 0:
                break
            m[m2 <= -4] = 1
            m[m2 == adj_seats] = -1
            m = m * free + m * occ
        return np.sum(m == -1)


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
