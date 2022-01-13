from pathlib import Path
import os.path
import pygame
import math

pygame.init()

# Okno
WIDTH = 300
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Kółko i krzyżyk")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Czcinaka
END_FONT = pygame.font.SysFont('arial', 40)
font = pygame.font.SysFont("monospace", 60)

# Obrazki
file_X_IMAGE = Path("x.png")
file_O_IMAGE = Path("o.png")



class Game:
    #Sprawdzenie czy istnieją obrazy X i O, jesli nie, wpisanie wlasnych
    def downloading_X_IMAGE(self):
        if os.path.exists("x.png"):
            X_IMAGE = pygame.transform.scale(pygame.image.load("x.png"), (80, 80))
        else:
            X_IMAGE = font.render("X", 1, BLACK)
        return X_IMAGE

    def downloading_O_IMAGE(self):
        if os.path.exists("o.png"):
            O_IMAGE = pygame.transform.scale(pygame.image.load("o.png"), (80, 80))
        else:
            O_IMAGE = font.render("O", 1, BLACK)
        return O_IMAGE

    def draw_grid(self):
        gap = WIDTH // ROWS

        # punkty początkowe
        x = 0
        y = 0

        for i in range(ROWS):
            x = i * gap

            pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
            pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


    #tworzenie tablicy gry
    def initialize_grid(self):
        dis_to_cen = WIDTH // ROWS // 2

        # Tablica gry
        game_array = [[None, None, None], [None, None, None], [None, None, None]]

        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x = dis_to_cen * (2 * j + 1)
                y = dis_to_cen * (2 * i + 1)

                # współrzędne centrum
                game_array[i][j] = (x, y, "", True)

        return game_array

    def render(self):
        win.fill(WHITE)
        Game.draw_grid(Game)

        # Rysowanie X i O
        for image in images:
            x, y, IMAGE = image
            win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

        pygame.display.update()

    def display_message(content):
        pygame.time.delay(500)
        win.fill(WHITE)
        end_text = END_FONT.render(content, 1, BLACK)
        win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
        pygame.display.update()
        pygame.time.delay(3000)


class Player:

    # wybór pozycji X i O
    def click(game_array):
        global x_turn, o_turn, images

        # pozycja myszy
        m_x, m_y = pygame.mouse.get_pos()

        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x, y, char, can_play = game_array[i][j]

                # Odległość między myszą a środkiem kwadratu
                dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

                # Jeśli jest w środku kwadratu
                if dis < WIDTH // ROWS // 2 and can_play:
                    if x_turn:  # Czas na X
                        images.append((x, y, Game.downloading_X_IMAGE(Game)))
                        x_turn = False
                        o_turn = True
                        game_array[i][j] = (x, y, 'x', False)

                    elif o_turn:  # Czas na O
                        images.append((x, y, Game.downloading_O_IMAGE(Game)))
                        x_turn = True
                        o_turn = False
                        game_array[i][j] = (x, y, 'o', False)

    # sprawdznie kto wygrał
    def has_won(game_array):
        # Sprawdzanie wierszy
        for row in range(len(game_array)):
            if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
                Game.display_message(game_array[row][0][2].upper() + " wygrał!")
                return True

        # Sprawdzanie kolumn
        for col in range(len(game_array)):
            if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
                Game.display_message(game_array[0][col][2].upper() + " wygrał!")
                return True

        # Sprawdzanie głównej przekątnej
        if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
            Game.display_message(game_array[0][0][2].upper() + " wygrał!")
            return True

        # Sprawdzanie przeciwnej przekątnej
        if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
            Game.display_message(game_array[0][2][2].upper() + " wygrał!")
            return True

        return False

    # sprawdzanie czy remis
    def has_drawn(game_array):
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                if game_array[i][j][2] == "":
                    return False

        Game.display_message("Remis!")
        return True


def main():
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = Game.initialize_grid(Game)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Player.click(game_array)

        Game.render(Game)

        if Player.has_won(game_array) or Player.has_drawn(game_array):
            run = False


while True:
    main()
