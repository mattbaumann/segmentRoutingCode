from typing import List

from src.backend.model.label import Label


class SegmentList:
    name: str
    labels: List[Label]

    def __init__(self, name: str, labels: List[Label]):
        self.name = name
        self.labels = labels

    def __str__(self):
        return "Segment List '%s' with labels {%s}" % (self.name, ",".join(label.__str__() for label in self.labels))