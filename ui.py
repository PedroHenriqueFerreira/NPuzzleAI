from tkinter import Tk, Canvas

from game import NPuzzleState
from search import BidirectionalAStarSearch

bidirectional_astar = BidirectionalAStarSearch(NPuzzleState.manhattan_distance)

BOX_SIZE = 600

INITIALIZE_TIME = 1000

MOVEMENT_TIME = 100
MOVEMENT_FRAMES = 10

INTERVAL_TIME = 100

BG_COLOR = '#DDD'

BLOCK_COLOR = '#FFF'

BORDER_SIZE = 2

def draw(steps: list[NPuzzleState]):
    root = Tk()
    root.title("N Puzzle")

    canvas = Canvas(root, width=BOX_SIZE, height=BOX_SIZE, background=BG_COLOR)
    canvas.pack()

    rectangles: list[int | None] = []
    texts: list[int | None] = []

    rectangles_pos: list[list[list[int]]] = []
    texts_pos: list[list[list[int]]] = []

    start = steps[0]

    for i in range(start.grid):
        rectangles_row = []
        texts_row = []
        
        rectangles_row_pos = []
        texts_row_pos = []
        
        for j in range(start.grid):
            block_size = BOX_SIZE / start.grid
            
            x = j * block_size
            y = i * block_size
            
            x_center = x + block_size / 2
            y_center = y + block_size / 2
            
            if steps[0].i == i and steps[0].j == j:
                rectangles_row.append(None)
                texts_row.append(None)
            else:
                rectangle = canvas.create_rectangle(
                    x, 
                    y, 
                    x + block_size, 
                    y + block_size, 
                    fill=BLOCK_COLOR, 
                    outline=BG_COLOR, 
                    width=BORDER_SIZE
                )
                
                text = canvas.create_text(
                    x_center, 
                    y_center, 
                    text=start.matrix[i][j], 
                    font=('Arial', 24)
                )

                rectangles_row.append(rectangle)
                texts_row.append(text)

            rectangles_row_pos.append([x, y])
            texts_row_pos.append([x_center, y_center])

        rectangles.append(rectangles_row)
        texts.append(texts_row)

        rectangles_pos.append(rectangles_row_pos)
        texts_pos.append(texts_row_pos)

    def run(step: int = 0):
        if step == len(steps) - 1:
            return canvas.after(INITIALIZE_TIME, root.destroy)
        
        curr = steps[step]
        next = steps[step + 1]
        
        i0, j0 = next.i, next.j
        i1, j1 = curr.i, curr.j

        rectangle_delta_x = rectangles_pos[i1][j1][0] - rectangles_pos[i0][j0][0]
        rectangle_delta_y = rectangles_pos[i1][j1][1] - rectangles_pos[i0][j0][1]

        text_delta_x = texts_pos[i1][j1][0] - texts_pos[i0][j0][0]
        text_delta_y = texts_pos[i1][j1][1] - texts_pos[i0][j0][1]
        
        def movement(counter = 0):
            if counter == MOVEMENT_FRAMES:
                return
            
            if counter == MOVEMENT_FRAMES - 1:
                canvas.moveto(rectangles[i0][j0], *rectangles_pos[i1][j1])
                canvas.moveto(texts[i0][j0], *texts_pos[i1][j1])
                
                rectangles[i0][j0], rectangles[i1][j1] = rectangles[i1][j1], rectangles[i0][j0]
                texts[i0][j0], texts[i1][j1] = texts[i1][j1], texts[i0][j0]
            else:
                rectangle_x = rectangles_pos[i0][j0][0] + rectangle_delta_x * (counter + 1) / MOVEMENT_FRAMES
                rectangle_y = rectangles_pos[i0][j0][1] + rectangle_delta_y * (counter + 1) / MOVEMENT_FRAMES
                
                text_x = texts_pos[i0][j0][0] + text_delta_x * (counter + 1) / MOVEMENT_FRAMES
                text_y = texts_pos[i0][j0][1] + text_delta_y * (counter + 1) / MOVEMENT_FRAMES
                
                canvas.moveto(rectangles[i0][j0], rectangle_x, rectangle_y)
                canvas.moveto(texts[i0][j0], text_x, text_y)
            
            canvas.after(MOVEMENT_TIME // MOVEMENT_FRAMES, movement, counter + 1)

        movement()
        
        canvas.after(MOVEMENT_TIME + INTERVAL_TIME, run, step + 1)

    root.after(INITIALIZE_TIME, run)
    root.mainloop()