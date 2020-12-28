from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):
    def next_bus_departure(self, bus_id, ts):
        q = ts // bus_id
        if q * bus_id == ts:
            return ts
        else:
            return (q + 1) * bus_id

    def run(self, s):
        ts, ids = s.splitlines()
        ts = int(ts)
        in_service = set()
        for e in ids.split(','):
            if e != 'x':
                in_service.add(int(e))
        
        departures = [(id, self.next_bus_departure(id, ts)) for id in in_service]
        bus, departure = min(departures, key=lambda x: x[1])
        return bus * (departure - ts)
