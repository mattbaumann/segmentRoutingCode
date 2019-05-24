from typing import List

from src.backend.model.label import Label


class SegmentList(object):
    name: str
    labels: List[Label]

    def __init__(self, name: str, labels: List[Label]):
        self.name = name
        self.labels = labels

    def __str__(self):
        return "Segment List '%s' with labels {%s}" % (self.name, ",".join(label.__str__() for label in self.labels))

    def json(self):
        return '{"name": "%s", "labels": %s' % (self.name, "[" + ",".join(path.json() for path in self.labels) + "]}")

    @classmethod
    def parse_json(cls, value: dict):
        return SegmentList(value["name"],
                           list(map(lambda item: Label.parse_json(item), value["labels"])))
