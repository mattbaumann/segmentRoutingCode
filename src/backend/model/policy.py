from typing import List

from .candidatePath import CandidatePath


class Policy(object):
    name: str
    color: int
    paths: List[CandidatePath]

    def __init__(self,
                 name: str,
                 color: int,
                 paths: List[CandidatePath]):
        self.name = name
        self.color = color
        self.paths = paths

    def __str__(self):
        return "Policy %s with color %d leads to {%s}" % (self.name,
                                                          self.color,
                                                          ",".join(path.__str__() for path in self.paths))

    def json(self):
        return "{name: %s, color: %d, paths: %s" % (self.name, self.color,
                                                    "[" + ",".join(path.json() for path in self.paths) + "]}")
