cimport cython

DEF FLOOR = 0
DEF EMPTY = 1
DEF TAKEN = 2
DEF INPUT_SIZE = 100000

# cdef void print_grid(char*grid, int w, int h):
#     print('w', w, 'h', h)
#     cdef i = 0
#     cdef str s
#     for i in range(h):
#         s = ''
#         for j in range(w):
#             s += '.L#'[grid[i * w + j]]
#         print(s)
#     print('')

# s1 = """L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# """
#
# s2 = """LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# """

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef int run(s):
    cdef char grid[INPUT_SIZE]
    cdef char grid_old[INPUT_SIZE]
    cdef int w = 0
    cdef int h = 0
    cdef int i = 0
    cdef int j = 0
    cdef int x = 0
    cdef int c = 0
    cdef str a
    for i, line in enumerate(s.strip().splitlines()):
        w = len(line)
        h += 1
        for j, a in enumerate(line):
            if a == '.':
                grid[i * w + j] = FLOOR
            else:
                grid[i * w + j] = EMPTY

    # LOOPY DOOP
    # cdef int step_debug = 0
    cdef bint moving = True
    while moving:
        # step_debug += 1
        # if step_debug > 5000:
        #     print("BREAAAAAAAAAAAK")
        #     break
        # print('--- step', step_debug, '---')
        # print_grid(grid, w, h)

        moving = False

        # copy in old
        for x in range(h * w):
            grid_old[x] = grid[x]

        # one step
        for x in range(h * w):
            j = x % w
            if (
                    grid_old[x] == EMPTY
                    and (x < w or grid_old[x - w] != TAKEN)  # n
                    and (x < w or j == w - 1 or grid_old[x - w + 1] != TAKEN)  # ne
                    and (j == w - 1 or grid_old[x + 1] != TAKEN)  # e
                    and (x >= (h - 1) * w or j == w - 1 or grid_old[x + w + 1] != TAKEN)  # se
                    and (x >= (h - 1) * w or grid_old[x + w] != TAKEN)  # s
                    and (x >= (h - 1) * w or j == 0 or grid_old[x + w - 1] != TAKEN)  # sw
                    and (j == 0 or grid_old[x - 1] != TAKEN)  # w
                    and (x < w or j == 0 or grid_old[x - w - 1] != TAKEN)  # nw
            ):
                grid[x] = TAKEN
                moving = True
            elif grid_old[x] == TAKEN:
                c = 0
                if x >= w and grid_old[x - w] == TAKEN:  # n
                    c += 1
                if x >= w and j < w - 1 and grid_old[x - w + 1] == TAKEN:  # ne
                    c += 1
                if j < w - 1 and grid_old[x + 1] == TAKEN:  # e
                    c += 1
                if x < (h - 1) * w and j < w - 1 and grid_old[x + w + 1] == TAKEN:  # se
                    c += 1
                if x < (h - 1) * w and grid_old[x + w] == TAKEN:  # s
                    c += 1
                if x < (h - 1) * w and j > 0 and grid_old[x + w - 1] == TAKEN:  # sw
                    c += 1
                if j > 0 and grid_old[x - 1] == TAKEN:  # w
                    c += 1
                if x >= w and j > 0 and grid_old[x - w - 1] == TAKEN:  # nw
                    c += 1

                if c >= 4:
                    grid[x] = EMPTY
                    moving = True

    # count taken
    cdef int res = 0
    for x in range(h * w):
        if grid[x] == TAKEN:
            res += 1

    return res
