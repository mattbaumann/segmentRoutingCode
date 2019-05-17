class Label:
    label: int
    type: str

    def __init__(self, label: int, type: str):
        self.label = label
        self.type = type

    def __str__(self):
        return "%s label with id: %s" % (self.type, self.label)
