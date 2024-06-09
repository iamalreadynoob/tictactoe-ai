class tictactoe:
    def __init__(self, width):
        self.width = width
        self.matrix = self._init_matrix()
        self.finalizers = self._get_finalizers()

    def _init_matrix(self):
        size = self.width * self.width
        matrix = []
        for i in range(size):
            matrix.append(-1)

        return matrix

    def _get_finalizers(self):
        finalizers = []

        for i in range(self.width):
            for j in range(self.width):
                # horizontal
                if j + 2 < self.width:
                    start = i * self.width + j
                    finalizers.append([start, start + 1, start + 2])
                # vertical
                if i + 2 < self.width:
                    start = i * self.width + j
                    finalizers.append([start, start + self.width, start + self.width * 2])
                # cross
                if j + 2 < self.width and i + 2 < self.width:
                    start = i * self.width + j
                    finalizers.append([start, start + self.width + 1, start + self.width * 2 + 2])
                if j - 2 >= 0 and i + 2 < self.width:
                    start = i * self.width + j
                    finalizers.append([start, start + self.width - 1, start + self.width * 2 - 2])
        return finalizers

    def _move(self, matrix, turn):
        print('Player {} return'.format(str(turn + 1)))
        pos = -1

        while pos < 0 or pos > len(matrix) or matrix[pos] != -1:
            row = int(input('Row: '))
            column = int(input('Column: '))
            pos = row * self.width + column

            if pos > len(matrix) or pos < 0 or matrix[pos] != -1:
                print('Illegal move attempt!')

        matrix[pos] = turn

        return matrix

    def _game_on(self, matrix, finalizers):
        temp = []

        for pos in finalizers:
            if matrix[pos[0]] == matrix[pos[1]] == matrix[pos[2]] and matrix[pos[0]] + matrix[pos[1]] + matrix[pos[2]] != -3:
                return False, finalizers
            elif matrix[pos[0]] == -1 or matrix[pos[1]] == -1 or matrix[pos[2]] == -1:
                temp.append(pos)

        return True, temp

    def _print_table(self, matrix):
        loc = 0

        while loc < len(matrix):
            line = '|'

            for i in range(self.width):
                if matrix[loc] == -1:
                    line += '   |'
                elif matrix[loc] == 0:
                    line += ' X |'
                else:
                    line += ' O |'

                loc += 1

            print(line)

    def _is_filled(self, matrix):
        filled = True

        for i in range(len(matrix)):
            if matrix[i] == -1:
                filled = False
                break

        return filled

    def play(self):
        game_on = True
        turn = 0
        while game_on is True:
            self.matrix = self._move(self.matrix, turn)
            game_on, self.finalizers = self._game_on(self.matrix, self.finalizers)

            self._print_table(self.matrix)

            if game_on is True:
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            else:
                print('Player {} won!'.format(str(turn + 1)))
                turn = -1

            if self._is_filled(self.matrix) is True:
                break

        if turn != -1:
            print('The game has tied!')

    def train(self, model1, model2):
        game_on = True
        turn = 0
        while game_on is True:
            if turn == 0:
                index = model1.predict(self.matrix, self.finalizers)
                self.matrix[index] = 0
            else:
                index = model2.predict(self.matrix, self.finalizers)
                self.matrix[index] = 1

            game_on, self.finalizers = self._game_on(self.matrix, self.finalizers)

            if game_on is True:
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            else:
                if turn == 0:
                    model1.save(1)
                    model2.save(-1)
                else:
                    model1.save(-1)
                    model2.save(1)
                print('Player {} won!'.format(str(turn + 1)))
                turn = -1

            if self._is_filled(self.matrix) is True:
                break

        if turn != -1:
            model1.save(0)
            model2.save(0)
            print('The game has tied!')

        return model1, model2

    def vs(self, model):
        game_on = True
        turn = 0
        while game_on is True:
            if turn == 0:
                self.matrix = self._move(self.matrix, turn)
            else:
                index = model.predict(self.matrix, self.finalizers)
                self.matrix[index] = 1

            game_on, self.finalizers = self._game_on(self.matrix, self.finalizers)

            self._print_table(self.matrix)
            print('***')

            if game_on is True:
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            else:
                if turn == 0:
                    model.save(-1)
                else:
                    model.save(1)
                print('Player {} won!'.format(str(turn + 1)))
                turn = -1

            if self._is_filled(self.matrix) is True:
                break

        if turn != -1:
            model.save(0)
            print('The game has tied!')