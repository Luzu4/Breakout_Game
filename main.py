import turtle
import time
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# Box positions
EASY_POS = [(-330, 250), (-240, 250), (-150, 250), (-60, 250), (30, 250), (120, 250), (210, 250), (300, 250),
            (-330, 220), (-240, 220), (-150, 220), (-60, 220), (30, 220), (120, 220), (210, 220), (300, 220),
            (-330, 190), (-240, 190), (-150, 190), (-60, 190), (30, 190), (120, 190), (210, 190), (300, 190),
            (-330, 160), (-240, 160), (-150, 160), (-60, 160), (30, 160), (120, 160), (210, 160), (300, 160),
            (-330, 130), (-240, 130), (-150, 130), (-60, 130), (30, 130), (120, 130), (210, 130), (300, 130)]
# Box Colours
COLORS = ['red', 'blue', 'white', 'yellow', 'green', 'purple']
HIGH_SCORE = 0
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('white')
        self.shapesize(1)
        self.penup()


class Board(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.color('white')
        self.x = 0
        self.y = -250
        self.penup()
        self.shapesize(0.5, 4)
        self.setposition(self.x, self.y)


class Block(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.color(random.choice(COLORS))
        self.penup()
        self.shapesize(1, 4)


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.color('white')
        self.goto(0, 0)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f'Score: {self.score}, HIGH SCORE: {HIGH_SCORE}', align=ALIGNMENT, font=FONT)

    def increase_score(self):
        global HIGH_SCORE
        self.score += 1
        if HIGH_SCORE < self.score:
            HIGH_SCORE += 1
        self.clear()
        self.update_scoreboard()


class Game:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.bgcolor('black')
        self.window.tracer(0)
        self.window.title('Breakout Game by Luz')
        self.ball = Ball()
        self.board = Board()
        # Canvas to use user mouse
        canvas = self.window.getcanvas()
        canvas.bind('<Motion>', self.set_cords)
        self.dx, self.dy = 1, 1
        self.step = 5
        # Random ball position every game
        self.ball.setx(random.randint(-250, 250))
        self.x_board, self.y_board = 250, -250
        self.scoreboard = Scoreboard()
        self.boxes = []
        self.x_holder = 0
        self.set_blocks()
        self.move()
        self.window.mainloop()

    def new_game(self):
        self.window.clearscreen()
        self.__init__()

    def set_blocks(self):
        for block in EASY_POS:
            box = Block()
            self.boxes.append(box)
            box.setposition(block[0], block[1])

    # Read mouse X position
    def set_cords(self, event):
        self.x_board = event.x

    def move(self):
        # Detect collision with walls right and left
        if self.ball.xcor() >= WINDOW_WIDTH / 2 or self.ball.xcor() <= -(WINDOW_WIDTH / 2):
            self.dx *= -1
        # Detect collision with top face and user board. We need to add height (20) and width (100) of our board
        if self.ball.ycor() >= WINDOW_HEIGHT / 2 or (
                self.board.ycor() + 10 > self.ball.ycor() and
                self.board.xcor() + 50 >= self.ball.xcor() >= self.board.xcor() - 50):
            self.dy *= -1
        # If our ball us under board we want to start new game
        if self.ball.ycor() < self.board.ycor():
            self.new_game()
        # Detect collision with boxes
        for box in self.boxes:
            if box.xcor() + 50 >= self.ball.xcor() >= box.xcor() - 50 and\
                    box.ycor() + 15 >= self.ball.ycor() >= box.ycor() - 15:
                # If collision direction is from the side we want to bounce right or left
                if self.ball.xcor() - box.xcor() < self.ball.ycor() - box.ycor() and\
                        (self.x_holder > box.xcor() + 40 or self.x_holder < box.xcor() - 40):
                    self.dx *= -1
                    self.scoreboard.increase_score()
                # if from bottom or top we want to bounce  down/up
                else:
                    self.dy *= -1
                    self.scoreboard.increase_score()
                # Hide box outside window
                box.goto(-1000, -1000)
        # Need to save last position to detect side of collision
        self.x_holder = self.ball.xcor()
        self.ball.goto(self.ball.xcor() + self.dx * self.step, self.ball.ycor() + self.dy * self.step)
        # Move board by user mouse
        self.board.setposition(self.x_board - 400, self.y_board)
        self.window.update()
        # Sleep a bit to slow ball
        time.sleep(0.01)

        self.window.ontimer(self.move)


game = Game()
