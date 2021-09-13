# Snake "Worm" Game
# Evelyn C

import pygame
import random

pygame.init()

# game variables

# colours
brown = (90, 75, 65)
pink = (192, 144, 152)
black = (0, 0, 0)
red = (210, 71, 71)
white = (255, 255, 255)
green = (102, 158, 75)
light_blue = (148, 190, 203)

dis_width = 800
dis_height = 600

best_length = 1

clock = pygame.time.Clock()

# fonts
font1 = pygame.font.SysFont("Open Sans", 36, True)
font2 = pygame.font.SysFont("Open Sans", 20, True, True)

# create display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Worm")
pygame.display.update()


# logic for spawning food pieces
class FOOD:
    food_size = 10
    need_respawn = False

    def __init__(self):
        self.pos_x = round((random.random() *
                            (dis_width - self.food_size)) / self.food_size) * self.food_size
        self.pos_y = round((random.random() *
                            (dis_height - self.food_size)) / self.food_size) * self.food_size
        self.rect = [self.pos_x, self.pos_y, self.food_size, self.food_size]

    def spawn_food(self):
        if self.need_respawn:
            food.__init__()
            self.need_respawn = False
        pygame.draw.rect(dis, green, self.rect)


food = FOOD()


class WORM:
    worm_size = 10
    worm_speed = 10

    # initiate worm values
    def __init__(self):
        self.head = [dis_width / 2, dis_height / 2]
        self.body = [[self.head[0], self.head[1]]]
        self.x_change = 0
        self.y_change = 0
        self.length = 1
        self.attempt_turn = ""
        self.move = ""

    # draw worm
    def draw_worm(self):
        for x in self.body:
            pygame.draw.rect(dis, pink, pygame.Rect(x[0], x[1], self.worm_size, self.worm_size))

    # logic for worm movement + behaviour
    def movement(self, events, game_over):
        for event in events:
            # enable WASD and arrow keys to move worm
            if event.type == pygame.KEYDOWN:
                if event.key == ord('w') or event.key == pygame.K_UP:
                    self.attempt_turn = "UP"
                elif event.key == ord('a') or event.key == pygame.K_LEFT:
                    self.attempt_turn = "LEFT"
                elif event.key == ord('d') or event.key == pygame.K_RIGHT:
                    self.attempt_turn = "RIGHT"
                elif event.key == ord('s') or event.key == pygame.K_DOWN:
                    self.attempt_turn = "DOWN"

        # prevent worm from reversing and colliding with itself
        if self.attempt_turn == "UP" and self.move != "DOWN":
            self.move = "UP"
        elif self.attempt_turn == "LEFT" and self.move != "RIGHT":
            self.move = "LEFT"
        elif self.attempt_turn == "RIGHT" and self.move != "LEFT":
            self.move = "RIGHT"
        elif self.attempt_turn == "DOWN" and self.move != "UP":
            self.move = "DOWN"

        # create movement
        if self.move == "UP":
            self.x_change = 0
            self.y_change = -self.worm_speed
        elif self.move == "LEFT":
            self.x_change = -self.worm_speed
            self.y_change = 0
        elif self.move == "RIGHT":
            self.x_change = self.worm_speed
            self.y_change = 0
        elif self.move == "DOWN":
            self.x_change = 0
            self.y_change = self.worm_speed

        # apply change in pos
        self.head[0] += self.x_change
        self.head[1] += self.y_change
        self.body.append([self.head[0], self.head[1]])
        if len(self.body) > self.length:
            del self.body[0]

        # if crash into barrier
        if self.head[0] >= dis_width or self.head[0] < 0 or self.head[1] >= dis_height or self.head[1] < 0:
            game_over = True
            return game_over

        # if crash into itself
        for x in self.body[:-1]:
            if self.head[0] == x[0] and self.head[1] == x[1]:
                game_over = True
                return game_over

        # food interaction
        if self.head[0] == food.pos_x and self.head[1] == food.pos_y:
            self.length += 1
            food.need_respawn = True

        return game_over


worm = WORM()


# function to create messages
def message(text, colour, font_type, height):
    msg = font_type.render(text, True, colour)
    dis.blit(msg, ((dis_width / 2) - (msg.get_rect().width / 2), height))


# function to draw title screen
def title_screen():
    dis.fill(light_blue)
    pygame.draw.rect(dis, green, pygame.Rect(0, 300, 800, 20))
    pygame.draw.rect(dis, brown, pygame.Rect(0, 310, 800, 290))
    pygame.draw.rect(dis, pink, pygame.Rect(380, 425, 40, 10))
    message("WORM", black, font1, 200)
    message("a snake game", black, font2, 240)
    message("WASD or Arrow Keys to Move - press any key to continue", black, font2, 550)
    pygame.display.update()


# function to draw end screen
def end_screen():
    dis.fill(black)
    message("GAME OVER", white, font1, 250)
    message("esc to close", white, font2, 400)
    message("space to play again", white, font2, 450)
    message("Final Length: " + str(worm.length), white, font2, 300)
    pygame.display.update()


# main logic to run game
def game_loop():
    game_end = False
    game_over = False
    dis_title = True

    while not game_end:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_end = True
                return game_end

        # display title screen
        while dis_title:
            title_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    dis_title = False

        # display game over screen
        while game_over:
            end_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = True
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_end = True
                        game_over = False
                    elif event.key == pygame.K_SPACE:
                        worm.__init__()
                        food.__init__()
                        game_loop()

        # main logic
        dis.fill(brown)
        food.spawn_food()
        worm.draw_worm()
        game_over = worm.movement(events, game_over)

        clock.tick(17)
        pygame.display.update()

    # quit game
    pygame.quit()
    quit()


if __name__ == "__main__":
    game_loop()
