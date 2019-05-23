class Label(object):
    label: int
    type: str

    def __init__(self, label: int, type: str):
        self.label = label
        self.type = type

    def __str__(self):
        return "%s label with id: %s" % (self.type, self.label)

    def json(self):
        return "{label: %d, type: %s}" % (self.label, self.type)

    @classmethod
    def parse_json(cls, value: dict):
        return Label(value["label"], value["type"])
