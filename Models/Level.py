import Models.Variable as Var


class Level:
    def __init__(self):
        # Initialize the nested dictionary
        self.levels = {}

    def add_data(self, level: int, data: Var.Variable):
        # Add data to the specified level
        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(data)

    def check_data_below_current_level(self, current_level: int, target_data: Var.Variable):
        # Check if the target_data is present in any level below the current_level
        for level in range(current_level + 1):
            if level in self.levels and target_data in self.levels[level]:
                return True
        return False
