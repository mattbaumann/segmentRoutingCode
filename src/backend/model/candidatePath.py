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
