import turtle
import time
import random

WIDTH, HEIGHT = 500, 500
COLORS = ['red', 'blue', 'orange', 'yellow', 'pink', 'purple', 'black', 'green', 'gray', 'cyan']

def get_number_of_racers():
    while True:
        racers=input("Enter the number of racers (2-10): ")
        if racers.isdigit():
            racers = int(racers)
            if 2 <= racers <= 10:
                return racers
            else:
                print("Number of racers must be in range 2-10")
        else:
            print("Input is not a number")

def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("TURTLE RACE")

def start_race(racers):
    while True:
        racer = random.choice(racers)
        racer.forward(random.randrange(1,20))

        y = racer.pos()[1]
        if y >= HEIGHT // 2 - 10:
            print(f"{racer.fillcolor().capitalize()} turtle won!")
            break


def init_racer(i):
    racer = turtle.Turtle()
    racer.shape('turtle')
    racer.color(COLORS[i])
    racer.left(90)
    racer.penup()

    return racer

def add_racers(num_of_racers):
    random.shuffle(COLORS)
    racers = []
    spacing = WIDTH // (num_of_racers+1)
    for i in range(num_of_racers):
        racers.append(init_racer(i))
        racers[i].setpos(-WIDTH // 2 + (i + 1) * spacing, -HEIGHT // 2 + 20)

    return racers

num_of_racers = get_number_of_racers()

init_turtle()
racers = add_racers(num_of_racers)
start_race(racers)