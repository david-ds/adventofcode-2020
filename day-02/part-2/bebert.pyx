cpdef int run(s):
    data = []
    for line in s.splitlines():
        if not line.strip():
            continue
        split1 = line.strip().split(": ")
        password = split1[1]
        split2 = split1[0].split(" ")
        letter = split2[1]
        split3 = split2[0].split("-")
        constraint_min = int(split3[0])
        constraint_max = int(split3[1])
        data.append((constraint_min, constraint_max, letter, password))

    valid = 0
    for (constraint_min, constraint_max, letter, password) in data:
        letter_count = 0
        if password[constraint_min - 1] == letter:
            letter_count += 1
        if password[constraint_max - 1] == letter:
            letter_count += 1
        if letter_count == 1:
            valid += 1
    return valid
