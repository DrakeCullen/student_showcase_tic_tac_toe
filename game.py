import pygame

from pygame.locals import *

pygame.init()

WIDTH = 500
HEIGHT = 500
OFFSET_LEFT = WIDTH / 3
OFFSET_LEFT = HEIGHT / 3
SQUARE_WIDTH = 70


class Square:
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.clicked = False
        self.num = (r, c)

    def __str__(self):
        return f"x: {self.x} y:{self.y}"

    def isClicked(self, clickX, clickY, isPlayerOne):
        if (
            clickX >= self.x
            and clickX <= self.x + SQUARE_WIDTH
            and clickY >= self.y
            and clickY <= self.y + SQUARE_WIDTH
            and self.clicked == False
        ):
            if isPlayerOne == True:
                pygame.draw.circle(
                    screen,
                    (255, 0, 0),
                    (self.x + SQUARE_WIDTH / 2 - 5, self.y + SQUARE_WIDTH / 2 - 5),
                    SQUARE_WIDTH / 2 - 10,
                )
            else:
                pygame.draw.line(
                    screen,
                    (255, 0, 0),
                    (self.x + 5, self.y + 5),
                    (self.x + SQUARE_WIDTH - 15, self.y + SQUARE_WIDTH - 15),
                    5,
                )
                pygame.draw.line(
                    screen,
                    (255, 0, 0),
                    (self.x + SQUARE_WIDTH - 15, self.y + 5),
                    (self.x + 5, self.y + SQUARE_WIDTH - 15),
                    5,
                )
            self.clicked = True
            return True, self.num
        return False, self.num


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        draw_squares()
        self.isRunning = True
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.isPlayerOne = True

    def is_over(self):
        # check if any row is filled or any column is filled or any diagonal is filled
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != 0:
            return True
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] != 0:
            return True
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] != 0:
            return True
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] != 0:
            return True
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] != 0:
            return True
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] != 0:
            return True
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True
        elif self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:
            return True
        return False

    def checkBoard(self, x, y):
        for square in squares:
            update, num = square.isClicked(x, y, self.isPlayerOne)
            if update:
                self.board[num[0]][num[1]] = 1 if self.isPlayerOne else 2
                self.isPlayerOne = not self.isPlayerOne
                if self.is_over():
                    print("Game Over")
                    self.reset()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
squares = []


def draw_squares():
    print("Drawing Squares")
    squares.clear()
    for i in range(3):
        for j in range(3):
            x = i * SQUARE_WIDTH + OFFSET_LEFT
            y = j * SQUARE_WIDTH + OFFSET_LEFT
            square = Square(x, y, i, j)
            squares.append(square)
            pygame.draw.rect(
                screen,
                (203, 234, 233),
                Rect(x, y, SQUARE_WIDTH - 10, SQUARE_WIDTH - 10),
            )


game = Game()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.checkBoard(x, y)
        pygame.display.update()
