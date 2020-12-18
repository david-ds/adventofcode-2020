DEF MODE_ADD = 0
DEF MODE_MULT = 1

cpdef long run(s):
    # s = "1 + (2 * 3) + (4 * (5 + 6))"
    cdef long memory[10]
    cdef long cur_number

    cdef char modes[10]
    cdef int cur = 0
    cdef long res = 0
    cdef int i
    cdef str line
    cdef str c
    for i, line in enumerate(s.strip().replace(' ', '').splitlines()):
        cur = 0
        memory[cur] = 0
        modes[cur] = MODE_ADD
        for c in line:
            if c == '+':
                modes[cur] = MODE_ADD
            if c == '*':
                modes[cur] = MODE_MULT
            elif c == '(':
                cur += 1
                memory[cur] = 0
                modes[cur] = MODE_ADD
            elif c == ')':
                cur -= 1
                # print(') Adding' if modes[cur] == MODE_ADD else ') Multiplying', memory[cur + 1], 'to', memory[cur])
                memory[cur] = memory[cur] + memory[cur + 1] if modes[cur] == MODE_ADD else memory[cur] * memory[cur + 1]
            elif c in '0123456789':
                cur_number = int(c)
                # print('  Adding' if modes[cur] == MODE_ADD else '  Multiplying', cur_number, 'to', memory[cur])
                memory[cur] = memory[cur] + cur_number if modes[cur] == MODE_ADD else memory[cur] * cur_number
        res += memory[cur]
    return res
