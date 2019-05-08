class Board:
    def __init__(self, num_stones, name_1, name_2):
        self.num_stones = num_stones
        self.hole_counts = [self.num_stones] * 6 + [-1] + [self.num_stones] * 6 + [-1]
        self.hole_division = {
            0: [0, 1, 2, 3, 4, 5],
            1: [7, 8, 9, 10, 11, 12]
        }
        self.players = [Player(name, num, self.hole_division[num])
                        for num, name in enumerate([name_1, name_2])]

    def __repr__(self):
        return f'''
        Board:
        {self.hole_counts[7:13][::-1]}
        {self.hole_counts[0:6]}
        '''


class Player:
    def __init__(self, name, num, holes):
        self.name = name
        self.number = num
        self.holes = holes
        self.point_hole = 6 if num == 0 else 13
        self.skip_hole = 13 if num == 0 else 6
        self.points = 0

    def add_points(self, points):
        self.points += points

    def __repr__(self):
        return f'Player {self.name} has {self.points}'