class Variable:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __eq__(self, other):
        return self.name == other.name
