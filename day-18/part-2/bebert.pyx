DEF MAX_DEPTH = 20

DEF MODE_ADD = 0
DEF MODE_MULT = 1

cpdef long run(s):
    # s = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    # s = "5 *[ 9 *[ (7 *[ 3 *[ 3 + 9 *[ 3 + (8 + 6 *[ 4 ]) ]]]) ] ]"
    # s = "0 *[ 1 *[ (3 *[ 4 *[ 5 + 5 *[ 6 + (7 + 7 *[ 8 ]) ]]]) ] ]"
    # s = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    # s = "6 * 4"
    cdef long memory[MAX_DEPTH]
    cdef long cur_number

    cdef char modes[MAX_DEPTH]

    cdef int fake_close[MAX_DEPTH]
    cdef int fake_cur = 0

    cdef int k
    for k in range(MAX_DEPTH):
        fake_close[k] = 0

    cdef int fake_pos = 0
    cdef int cur = 0
    cdef long res = 0
    cdef int i
    cdef int j
    cdef str line
    cdef str c
    for i, line in enumerate(s.strip().splitlines()):
        cur = 0
        memory[cur] = 0
        modes[cur] = MODE_ADD
        fake_close[cur] = 0
        fake_cur = 0
        for c in line:
            if c == ' ':
                continue
            # print(c)
            if c == '+':
                modes[cur] = MODE_ADD
            if c == '*':
                modes[cur] = MODE_MULT
                cur += 1
                memory[cur] = 0
                modes[cur] = MODE_ADD
                fake_close[fake_cur] += 1
            elif c == '(':
                cur += 1
                memory[cur] = 0
                modes[cur] = MODE_ADD
                fake_cur += 1
            elif c == ')':
                # print('fake_curs:', pretty_fake_curs(fake_close), ', cur:', cur, '->', cur - 1)
                # print('] *', fake_close[fake_cur])
                for j in range(fake_close[fake_cur]):
                    fake_close[fake_cur] -= 1
                    cur -= 1
                    # print('Adding' if modes[cur] == MODE_ADD else 'Multiplying', memory[cur + 1], 'to', memory[cur])
                    memory[cur] = memory[cur] + memory[cur + 1] if modes[cur] == MODE_ADD else memory[cur] * memory[cur + 1]
                fake_cur -= 1
                cur -= 1
                # print('Adding' if modes[cur] == MODE_ADD else 'Multiplying', memory[cur + 1], 'to', memory[cur])
                memory[cur] = memory[cur] + memory[cur + 1] if modes[cur] == MODE_ADD else memory[cur] * memory[cur + 1]
                # print(f'{cur}--->', memory[cur])
            elif c in '0123456789':
                cur_number = int(c)
                # print('Adding' if modes[cur] == MODE_ADD else 'Multiplying', cur_number, 'to', memory[cur])
                memory[cur] = memory[cur] + cur_number if modes[cur] == MODE_ADD else memory[cur] * cur_number
                # print('--->', memory[cur], 'at', cur)

        # print(f'----------- end of {i}, cur at {cur}, res {memory[cur]}, {fake_close[fake_cur]} to close')
        for j in range(fake_close[fake_cur]):
            fake_close[fake_cur] -= 1
            cur -= 1
            # print('Adding' if modes[cur] == MODE_ADD else 'Multiplying', memory[cur + 1], 'to', memory[cur])
            memory[cur] = memory[cur] + memory[cur + 1] if modes[cur] == MODE_ADD else memory[cur] * memory[cur + 1]
            # print('--->', memory[cur], 'at', cur)

        res += memory[cur]

    # print('==>', res)
    return res


# cdef str pretty_fake_curs(int* fc):
#     cdef int i
#     s = '['
#     for i in range(MAX_DEPTH - 1):
#         s += str(fc[i]) + ','
#     s += str(fc[MAX_DEPTH - 1])
#     return s + ']'
