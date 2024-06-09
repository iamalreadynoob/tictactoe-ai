from random import randint
import json


class ticmodel:
    def __init__(self, success=10, fname=None):
        self.history = []
        self.id = -1
        self.success = success

        self.memory = {}
        if fname is not None:
            with open(fname, "r") as infile:
                self.memory = json.load(infile)

    def _flat(self, matrix):
        result = ''

        for val in matrix:
            result += str(val)

        return result

    def _is_one(self, matrix, pos):
        amount = 0
        index = -1
        for i in range(len(pos)):
            if matrix[pos[i]] == -1:
                amount += 1
                index = i
                if amount > 1:
                    break

        if amount == 1:
            return True, index
        else:
            return False, index

    def _get_possible(self, matrix):
        empty = []

        for i in range(len(matrix)):
            if matrix[i] == -1:
                empty.append(i)

        return empty

    def assign(self, id):
        self.id = id

    def predict(self, matrix, finalizers):
        save = None
        finish = None

        for pos in finalizers:
            situ, index = self._is_one(matrix, pos)
            if situ is True:
                matrix[pos[index]] = self.id

                if matrix[pos[0]] == matrix[pos[1]] == matrix[pos[2]]:
                    finish = pos[index]
                else:
                    save = pos[index]

            if (save is not None) and (finish is not None):
                break

        if finish is not None:
            return finish

        if save is not None:
            return save

        flat = self._flat(matrix)
        if flat in self.memory:
            value = None
            move = -1

            for pos in self.memory[flat]:
                if self.memory[flat][pos] >= self.success:
                    if value is None or self.memory[flat][pos] > value:
                        value = self.memory[flat][pos]
                        move = pos

            if move != -1:
                destiny = randint(1, 10)
                if destiny < 8:
                    self.history.append([flat, move])
                    return int(move)

        empty = self._get_possible(matrix)
        destiny = randint(0, len(empty) - 1)
        self.history.append([flat, empty[destiny]])

        return empty[destiny]

    def save(self, endgame):
        increase = 0

        if endgame == -1:
            increase = -1
        elif endgame == 0:
            increase = 1
        elif endgame == 1:
            increase = 2

        for hist in self.history:
            if hist[0] in self.memory and str(hist[1]) in self.memory[hist[0]]:
                self.memory[hist[0]][str(hist[1])] += increase
            else:
                self.memory[hist[0]] = {}
                self.memory[hist[0]][str(hist[1])] = increase

        self.history.clear()


    def json(self, fname):
        with open(fname, "w") as outfile:
            json.dump(self.memory, outfile)


def combine(model1, model2, fname=None):
    combined = model1.memory

    for position in model2.memory:
        if position in combined:
            for move in model2.memory[position]:
                if move in combined[position]:
                    combined[position][move] += model2.memory[position][move]
                else:
                    combined[position][move] = model2.memory[position][move]
        else:
            combined[position] = model2.memory[position]

    if fname is not None:
        with open(fname, "w") as outfile:
            json.dump(combined, outfile)

    return combined
