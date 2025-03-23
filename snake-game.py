import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile: #used to store the position of the snake and the food
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas= tkinter.Canvas(window, bg="teal", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()   
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
#format +(w)*(h)+(x)+(y)
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) #single tile, food
snake_body = [] #list of tiles, snake body
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

def change_direction(event):
    #print(event.keysym)
    global velocity_x, velocity_y, game_over 
    if(game_over):
        return

    if(event.keysym == "Up" and velocity_y != 1):
        velocity_x = 0
        velocity_y = -1
    elif(event.keysym == "Down" and velocity_y != -1):
        velocity_x = 0
        velocity_y = 1
    elif(event.keysym == "Left" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    elif(event.keysym == "Right" and velocity_x != -1):
        velocity_x = 1
        velocity_y = 0

def move_snake():
    global snake, food, snake_body, game_over, score
    if(game_over):
        return
    
    #if the snake eats itself or hits the wall, the game is over
    if(snake.x<0 or snake.x>=WINDOW_WIDTH or snake.y<0 or snake.y>=WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision with food
    if(snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(snake.x, snake.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
    
    #update the snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            pre_tile = snake_body[i-1]
            tile.x = pre_tile.x
            tile.y = pre_tile.y

    #collision with the wall
    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        snake.x = 5*TILE_SIZE
        snake.y = 5*TILE_SIZE
        snake_body.clear()

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score
    move_snake()

    canvas.delete("all") #clear the canvas

    #draw the food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="gold")

    #draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="violet")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="violet")
    
    if(game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text= f"Game Over: {score}", fill="white", font= "Arial 20")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(100, draw) #100ms = 1/10s, 10 frames per second

draw()


window.bind("<KeyRelease>", change_direction)
window.mainloop()