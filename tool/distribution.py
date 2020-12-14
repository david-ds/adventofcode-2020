
HISTOGRAM_CHARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
HISTOGRAM_WIDTH = 6


def get_time_distribution(durations):
    if not durations:
        return ''
    _max, _min = max(durations), min(durations)
    n = HISTOGRAM_WIDTH
    step = (_max - _min) / float(n)
    r = [0] * (n + 1)
    for i in range(n + 1):
        c = 0
        for d in durations:
            if _min + i * step <= d < _min + (i + 1) * step:
                c += 1
        r[i] = c / len(durations)
    s = []
    for x in r:
        found = False
        for i, c in enumerate(HISTOGRAM_CHARS[1:]):
            if i / n < x <= (i + 1) / n:
                s.append(c)
                found = True
                break
        if not found:
            s.append(HISTOGRAM_CHARS[0])
    return "{} [{:.03f}-{:.03f}]ms".format(
        "".join(s),
        _min,
        _max,
    )
