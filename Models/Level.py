import Models.Variable as Var


class Level:
    def __init__(self, name):
        # Initialize the nested dictionary
        self.levels = {}
        self.level = 0
        self.name = name

    def add_data(self, level: int, data):
        # Add data to the specified level
        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(data)

    def check_data_below_current_level(self, target_data):
        # Check if the target_data is present in any level below the current_level
        for level in range(self.level + 1):
            if level in self.levels and target_data in self.levels[level]:
                return True
        return False

    def __str__(self):
        return f"Level({self.name}, {self.level}, {self.levels})"