import pygame
from server import server_boy
from client import socky_boy
import sys
from pygame.locals import *

pygame.init()

WIDTH = 500
HEIGHT = 500
OFFSET_LEFT = WIDTH / 3
OFFSET_LEFT = HEIGHT / 3
SQUARE_WIDTH = 70
screen = pygame.display.set_mode((WIDTH, HEIGHT))
squares = []


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

    def update_board(self, num):
        self.board[num[0]][num[1]] = 1 if self.isPlayerOne else 2
        self.isPlayerOne = not self.isPlayerOne
        if self.is_over():
            print("Game Over")
            self.reset()
        return 0, num

    def checkBoard(self, x, y, player_type):
        if player_type == 1:
            if self.isPlayerOne == False:
                return -1, (-1, -1)
        elif player_type == 2:
            if self.isPlayerOne == True:
                return -1, (-1, -1)
        for square in squares:
            update, num = square.isClicked(x, y, self.isPlayerOne)
            if update:
                return self.update_board(num)


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


if len(sys.argv) < 2:
    print("You need to specify server or client")
    exit()

player_type = sys.argv[1]
game = Game()
running = True

if player_type == "server":
    server = server_boy()
    player_type = 1
elif player_type == "client":
    client = socky_boy()
    player_type = 2
else:
    print("Invalid player type")
    exit()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if player_type == 1:
                x, y = pygame.mouse.get_pos()
                return_value, num = game.checkBoard(x, y, player_type)
                if return_value != -1:
                    pygame.display.update()
                    print("num is " + str(num))
                    server.sendMove(num)
                    responce = server.awaitMove()
                    game.update_board(responce)
                    game.isPlayerOne = not game.isPlayerOne
                    print("responce " + str(responce))
            else:
                x, y = pygame.mouse.get_pos()
                return_value, num = game.checkBoard(x, y, player_type)
                if return_value != -1:
                    print("num is " + str(num))
                    pygame.display.update()
                    client.sendMove(num)
                    responce = client.awaitMove()
                    game.update_board(responce)
                    game.isPlayerOne = not game.isPlayerOne
                    print(responce)

        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                server.getConnection()
                server.sendHi()
            if event.key == pygame.K_a and player_type == 2:
                responce = client.awaitMove()
                game.isPlayerOne = not game.isPlayerOne
                print(responce)

        pygame.display.update()
