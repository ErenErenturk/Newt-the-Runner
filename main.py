import time
import pygame
import random
import math
import turtle
# importing levels list from levels.py
from levels import levels

# setting up pygame library
pygame.mixer.init()
# setting windows with turtle library
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Newt The Runner")
wn.setup(1000, 1000)
wn.tracer(0)

# theme music
bg_music = pygame.mixer.Sound("gifs_musics/alttheme.mp3")
pygame.mixer.Sound.play(bg_music)
# defining game action sound effects
death_sound = pygame.mixer.Sound("gifs_musics/player_death.mp3")
ouh_sound = pygame.mixer.Sound("gifs_musics/ouh.mp3")
slash_sound = pygame.mixer.Sound("gifs_musics/slash.mp3")
gold_sound = pygame.mixer.Sound("gifs_musics/gold.mp3")
key_sound = pygame.mixer.Sound("gifs_musics/key.mp3")
door_sound = pygame.mixer.Sound("gifs_musics/door.mp3")

# registering shapes
images = ["start_page.gif",
          "victory.gif",
          "game_over.gif",
          "wall.gif",
          "altwall.gif",
          "hp.gif",
          "blood.gif",
          "key.gif",
          "door.gif",
          "gold.gif",
          "skeletonright.gif",
          "skeletonleft.gif",
          "pl.gif",
          "pr.gif",
          "attl.gif",
          "attr.gif",
          "prf.gif",
          "plf.gif"]
for img in images:
    img = "gifs_musics/" + img
    print(img)
    turtle.register_shape(img)


# pen class
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/altwall.gif")
        self.color("gray")
        self.turtlesize(1.5)
        self.penup()
        self.speed(0)


# door class
class Door(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/door.gif")
        self.color("green")
        self.penup()
        self.speed(0)
        self.turtlesize(1.5)


# key class
class Key(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/key.gif")
        self.color("#957163")
        self.penup()
        self.speed(0)
        self.key = 1
        self.goto(x, y)
        self.turtlesize(1.5)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# player class
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/pr.gif")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.key = 0
        self.health = 5
        self.death = 0
        self.way = 0

    def go_up(self):
        # calculate the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 36
        # check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        # calculate the spot to move to
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 36
        # check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        # calculate the spot to move to
        move_to_x = player.xcor() - 36
        move_to_y = player.ycor()
        # check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.shape("gifs_musics/pl.gif")
            self.way = -1
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        # calculate the spot to move to
        move_to_x = player.xcor() + 36
        move_to_y = player.ycor()
        # check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.shape("gifs_musics/pr.gif")
            self.way = 1
            self.goto(move_to_x, move_to_y)

    def attack(self):
        pygame.mixer.Sound.play(slash_sound)
        attack_count = 0
        for nme in enemies:
            if self.is_close_to_attack(nme):
                attack_count += 1

                if nme.xcor() >= self.xcor():
                    self.shape("gifs_musics/attr.gif")
                else:
                    self.shape("gifs_musics/attl.gif")
                self.gold += nme.gold
                nme.health -= 1
                nme.die()
                nme.destroy()
                wn.update()
                time.sleep(0.3)
                if self.way == 1:
                    self.shape("gifs_musics/pr.gif")
                else:
                    self.shape("gifs_musics/pl.gif")
        if not attack_count:
            if self.way == 1:
                self.shape("gifs_musics/attr.gif")
                wn.update()
                time.sleep(0.2)
                self.shape("gifs_musics/pr.gif")
            else:
                self.shape("gifs_musics/attl.gif")
                wn.update()
                time.sleep(0.2)
                self.shape("gifs_musics/pl.gif")

    def is_close_to_attack(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 70:
            return True
        else:
            return False

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False


# treasure class
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/gold.gif")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# enemy class
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("gifs_musics/skeletonright.gif")
        self.penup()
        self.speed(0)
        self.health = 1
        self.gold = 25
        self.damage = 1
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 36
        elif self.direction == "down":
            dx = 0
            dy = -36
        elif self.direction == "left":
            self.shape("gifs_musics/skeletonleft.gif")
            dx = -36
            dy = 0
        elif self.direction == "right":
            self.shape("gifs_musics/skeletonright.gif")
            dx = 36
            dy = 0
        else:
            dx = 0
            dy = 0

        # check if player is close
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        # calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])
        turtle.ontimer(self.move, t=random.randint(100, 250))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 120:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def die(self):
        statistics["enemy"] += 1
        self.shape("gifs_musics/blood.gif")
        self.stamp()


# treasures list
treasures = []

# keys list
keys = []

# enemies list
enemies = []

# player statistics
statistics = {"gold": 0, "enemy": 0}

# defining game_on for game loop
game_on = False


# starting game loop
def start_game():
    global game_on
    turtle.clear()
    game_on = True


# showing start menu
def show_menu():
    turtle.onkey(start_game, "Return")
    turtle.shape("gifs_musics/start_page.gif")
    turtle.goto(0, 0)
    turtle.stamp()
    wn.update()


# finishing game with using game over or victory options
def finish_game(game_win):
    clear_maze()
    door.goto(2000, 2000)
    key.goto(2000, 2000)
    player.goto(2000, 2000)
    pen.goto(2000, 2000)
    # you win screen
    if game_win:
        turtle.shape("gifs_musics/victory.gif")
        turtle.goto(0, 0)
        turtle.stamp()
        turtle.color("pink")
        turtle.goto(0, 17)
        turtle.write(statistics['gold']*5000 + statistics['enemy']*10000, font=("Impact", 50, "normal"))
        turtle.goto(-300, -100)
        turtle.color("gold")
        turtle.write(f"Total Gold Collected: {statistics['gold']}", font=("Impact", 25, "normal"))
        turtle.goto(-300, -200)
        turtle.color("red")
        turtle.write(f"Total Enemy Killed: {statistics['enemy']}", font=("Impact", 25, "normal"))
    # game over screen
    elif not game_win:
        turtle.shape("gifs_musics/game_over.gif")
        turtle.goto(0, 0)
        turtle.stamp()

    while True:
        wn.update()


# setting up level
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            # calculate the screen x, y coords
            screen_x = -432 + (x * 36)
            screen_y = 450 - (y * 36)
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                # add coordinates to wall list
                walls.append((screen_x, screen_y))
            # check if it is a "P"
            if character == "P":
                player.goto(screen_x, screen_y)
            # check if it is a "T"
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))
            # check if it is a "E"
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))
            # check if it is a "D"
            if character == "D":
                door.goto(screen_x, screen_y)
            # check if it is "K"
            if character == "K":
                keys.append(Key(screen_x, screen_y))


# clearing maze elements to change level
def clear_maze():
    for nme in enemies:
        nme.clear()
        nme.destroy()
        player.key = 0
        statistics["gold"] += player.gold
        player.gold = 0
    for tre in treasures:
        tre.destroy()
    walls.clear()
    pen.clear()
    door.clear()


# next level and player animation
def next_maze(level_num):
    clear_maze()
    setup_maze(levels[level_num])
    # enemy movement
    for nme in enemies:
        turtle.ontimer(nme.move, t=250)
    # player animation
    player.shape("gifs_musics/prf.gif")
    wn.update()
    time.sleep(0.5)
    player.shape("gifs_musics/pr.gif")


# writing player statistic on the screen
def write_objects():
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-445, 470)
    turtle.color("yellow")
    turtle.write(f"Newt's Gold= {player.gold}", font=("Impact", 15, "normal"))
    turtle.goto(-245, 470)
    turtle.color("white")
    turtle.write(f"Keys= {player.key}", font=("Impact", 15, "normal"))
    turtle.goto(-145, 470)
    turtle.color("red")
    turtle.write(f"Damage Count= {player.death}", font=("Impact", 15, "normal"))
    turtle.goto(250, 470)
    turtle.color("lightgreen")
    turtle.write(f"HP=", font=("Impact", 15, "normal"))
    # player health point onjects
    turtle.shape("gifs_musics/hp.gif")
    for num in range(player.health):
        turtle.goto(300 + (num * 24), 485)
        turtle.stamp()
    # zero health
    if not player.health:
        turtle.hideturtle()

    wn.update()
    turtle.clear()


# creating class instances
pen = Pen()
player = Player()
door = Door()

# creating wall coordinate list
walls = []

# setting up the level using setup_maze
current_level = 1
setup_maze(levels[current_level])

# keyboard binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.attack, "space")

# turning off screen updates
wn.tracer(0)

# showing start_menu when game does not start
while not game_on:
    show_menu()

# moving enemies at first
for enemy in enemies:
    # start moving enemies
    turtle.ontimer(enemy.move, t=250)

# Main game loop
while game_on:
    # player statistics on game screen
    write_objects()

    # player reaching gold
    # iterate through treasure list
    for treasure in treasures:
        if player.is_collision(treasure):
            # adding the treasure gold to the player gold
            player.gold += treasure.gold
            pygame.mixer.Sound.play(gold_sound)
            # destroying the treasure
            treasure.destroy()
            # removing the treasure from the treasures list
            treasures.remove(treasure)
    # player collecting key
    for key in keys:
        if player.is_collision(key):
            pygame.mixer.Sound.play(key_sound)
            player.key += key.key
            key.destroy()
            keys.remove(key)
    # player reaching door with total keys
    if player.is_collision(door) and not keys:
        # last level end
        if current_level == len(levels) - 1:
            finish_game(True)
            game_on = False
            # next level
        else:
            pygame.mixer.Sound.play(door_sound)
            current_level += 1
            next_maze(current_level)

    # iterate through enemy list to see if player collide
    for enemy in enemies:
        if player.is_collision(enemy):
            player.death -= 1
            player.health -= enemy.damage
            # player death
            if not player.health:
                pygame.mixer.Sound.play(death_sound)
                write_objects()
                finish_game(False)
            # player damage
            else:
                pygame.mixer.Sound.play(ouh_sound)
            time.sleep(0.2)
