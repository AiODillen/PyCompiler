#create a function class similar to the variable class
import Models.Level
class Function:
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body


    def __repr__(self):
        return f"Function({self.name}, {self.parameters}, {self.return_type}, {self.body})"

    def __str__(self):
        return f"Function({self.name}, {self.parameters}, {self.return_type}, {self.body})"

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.name == other.name
