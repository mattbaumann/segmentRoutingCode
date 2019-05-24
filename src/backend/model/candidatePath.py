from typing import List

from .segmentList import SegmentList


class CandidatePath:
    preference: int
    hops: List[SegmentList]

    def __init__(self, preference: int, hops: List[SegmentList]):
        self.preference = preference
        self.hops = hops

    def __str__(self):
        return "Preference %d and paths {%s}" % (self.preference, ",".join(hop.__str__() for hop in self.hops))

    def json(self):
        return '{"preference": %d, "hops": %s' % (
        self.preference, "[" + ",".join(path.json() for path in self.hops) + "]}")

    @classmethod
    def parse_json(cls, value: dict):
        path = CandidatePath(value["preference"],
                             list(map(lambda item: SegmentList.parse_json(item), value["hops"])))
