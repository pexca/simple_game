import tkinter
import random

# constants:
WIDTH = 640
HEIGHT = 480
BG_COLOUR = 'white'
BAD_COLOUR = 'red'
COLOURS = ['aqua', BAD_COLOUR, 'fuchsia', 'pink', BAD_COLOUR, 'yellow', 'gold', BAD_COLOUR, 'chartreuse']
ZERO = 0
CIRCLE_RADIUS = 30
CIRCLE_COLOUR = 'blue'
INIT_DX = 1
INIT_DY = 1
DELAY = 5
NUM_OF_CIRCLES = 10


class Circles:
    def __init__(self, x, y, radius, colour, dx=0, dy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.dx = dx  # смещение по осям
        self.dy = dy

    def draw(self):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius,
                           fill=self.colour, outline=self.colour if self.colour != BAD_COLOUR else 'black')

    def hide(self):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius,
                           fill=BG_COLOUR, outline=BG_COLOUR)  # outline is contour

    def is_collision(self, circle):
        a = abs(self.x + self.dx - circle.x)
        b = abs(self.y + self.dy - circle.y)
        return (a*a + b*b)**0.5 <= self.radius + circle.radius

    def move(self):  # перемещение шарика
        # столкновение с границами окна
        if (self.x + self.radius + self.dx >= WIDTH) or (self.x - self.radius + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.radius + self.dy >= HEIGHT) or (self.y - self.radius + self.dy <= ZERO):
            self.dy = -self.dy

        # action on collision
        for circle in circles:
            if self.is_collision(circle):
                # остановить шарик при столкновении с красным
                if circle.colour != BAD_COLOUR:
                    circle.hide()
                    circles.remove(circle)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


# создание объекта по клику мыши
def mouse_click(event):
    global circle
    if event.num == 1:
        if 'circle' not in globals():
            circle = Circles(event.x, event.y, CIRCLE_RADIUS, CIRCLE_COLOUR, INIT_DX, INIT_DY)
            circle.draw()
        else:
            if circle.dx * circle.dy > 0:  # turn left
                circle.dy = -circle.dy
            else:
                circle.dx = -circle.dx
    elif event.num == 3:
        if circle.dx * circle.dy > 0:  # turn right
            circle.dx = -circle.dx
        else:
            circle.dy = -circle.dy
    print(event.num, event.x, event.y)


# create list of circles
def create_some_circles(number):
    lst = []
    while len(lst) < number:
        next_circle = Circles(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(15, 35),
                                random.choice(COLOURS))
        is_collision = False
        for circle in lst:
            if next_circle.is_collision(circle):
                is_collision = True
                break
        if not is_collision:
            lst.append(next_circle)
            next_circle.draw()
    return lst


# count red balls
def count_red_circles(list_of_circles):
    result = 0
    for circle in list_of_circles:
        if circle.colour == BAD_COLOUR:
            result += 1
    return result


# main game loop
def main():
    if 'circle' in globals():
        circle.move()
        if len(circles) - number_of_red_circles == 0:  # выбиты все шары, кроме красных
            canvas.create_text(WIDTH/2, HEIGHT/2, text='YOU WON!', font='Arial 20', fill=CIRCLE_COLOUR)
            circle.dx = circle.dy = 0  # stops the circle
        elif circle.dx == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text='YOU LOST!', font='Arial 20', fill=BAD_COLOUR)
    window.after(DELAY, main)


window = tkinter.Tk()  # основное окно
window.title('Сталкивающиеся шарики')
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, bg=BG_COLOUR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)  # перехват событий мыши
canvas.bind('<Button-3>', mouse_click, '+')
if 'circle' in globals():  # освободить память при аварийном прерывании программы
    del circle
circles = create_some_circles(NUM_OF_CIRCLES)
number_of_red_circles = count_red_circles(circles)
main()
window.mainloop()
