from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    # declaring empty cost 3d list
    cost = [[(0, 0) for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    # getting through "one of empty cells scenario"
    for i in range(1, len(b) + 1):
        cost[0][i] = (i, Operation.INSERTED)
    for i in range(1, len(a) + 1):
        cost[i][0] = (i, Operation.DELETED)
    # Figuring amount of possible operations
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            deletion_cost, _ = cost[i - 1][j]
            deletion_cost += 1
            insertion_cost, _ = cost[i][j - 1]
            insertion_cost += 1
            substraction_cost, _ = cost[i - 1][j - 1]
            if not a[i - 1] == b[j - 1]:
                substraction_cost += 1
            # Creating list of cost operations to get best scenario out of it
            cost_values = [(deletion_cost, Operation.DELETED), (insertion_cost,
                                                                Operation.INSERTED), (substraction_cost, Operation.SUBSTITUTED)]
            cost[i][j] = cost_values[cost_values.index(min(cost_values, key=lambda x: x[0]))]
            # key = lambda x: x[0] will take first(0) value to compare
    return(cost)