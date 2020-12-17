cimport cython

DEF INPUT_WIDTH = 8
DEF NB_CYCLES = 6
DEF GRID_SIZE = 22

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
cpdef int run(str s):
    cdef bint grid_raw[GRID_SIZE][GRID_SIZE][GRID_SIZE]
    cdef bint [:, :, :] grid = grid_raw

    cdef bint grid_raw_old[GRID_SIZE][GRID_SIZE][GRID_SIZE]
    cdef bint [:, :, :] grid_old = grid_raw_old

    cdef int i, j, k, di, dj, dk, step, count
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            for k in range(GRID_SIZE):
                grid[i][j][k] = 0
                grid_old[i][j][k] = 0

    cdef int x_start = NB_CYCLES + 1
    cdef int y_start = NB_CYCLES + 1
    cdef int z_start = NB_CYCLES + INPUT_WIDTH // 2 + 1

    cdef str line
    cdef str c
    for dy, line in enumerate(s.strip().splitlines()):
        for dx, c in enumerate(line):
            grid[x_start + dx][y_start + dy][z_start] = c == '#'

    # print("======== step 0 ========")
    # print_grid(grid, GRID_SIZE)

    for step in range(NB_CYCLES):
        for i in range(1, GRID_SIZE - 1):
            for j in range(1, GRID_SIZE - 1):
                for k in range(1, GRID_SIZE - 1):
                    grid_old[i][j][k] = grid[i][j][k]

        for i in range(1, GRID_SIZE - 1):
            for j in range(1, GRID_SIZE - 1):
                for k in range(1, GRID_SIZE - 1):
                    count = -grid_old[i][j][k]
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            for dk in range(-1, 2):
                                count += grid_old[i + di][j + dj][k + dk]

                    if grid_old[i][j][k]:
                        if count != 2 and count != 3:
                            grid[i][j][k] = 0

                    if not grid_old[i][j][k] and  count == 3:
                        grid[i][j][k] = 1

        # print(f"======== step {step + 1} ========")
        # print_grid(grid, GRID_SIZE)

    count = 0
    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):
            for k in range(1, GRID_SIZE - 1):
                count += grid[i][j][k]

    return count


# cdef void print_grid(bint[:, :, :] grid, int grid_size):
#     cdef str s
#     for k in range(grid_size):
#         print('\n--- k', k)
#         for i in range(grid_size):
#             s = ''
#             for j in range(grid_size):
#                 s += '.#'[grid[j][i][k]]
#             print(s)
#     print('\n')
