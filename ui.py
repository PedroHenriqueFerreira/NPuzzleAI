from tkinter import Tk, Canvas

from game import NPuzzleState
from search import BidirectionalAStarSearch

bidirectional_astar = BidirectionalAStarSearch(NPuzzleState.manhattan_distance)

size = 600

movement_time = 120
movement_frames = 10

interval_time = 100

def draw(steps: list[NPuzzleState]):
    root = Tk()
    root.title("N Puzzle")

    canvas = Canvas(root, width=size, height=size, background='#ddd')
    canvas.pack()

    rectangles: list[int | None] = []
    texts: list[int | None] = []

    rectangles_pos: list[list[list[int]]] = []
    texts_pos: list[list[list[int]]] = []

    for i in range(steps[0].size):
        rectangles_row = []
        texts_row = []
        
        rectangles_row_pos = []
        texts_row_pos = []
        
        for j in range(steps[0].size):
            block_size = size / steps[0].size
            
            x = j * block_size
            y = i * block_size
            
            x_center = x + block_size / 2
            y_center = y + block_size / 2
            
            if steps[0].i != i or steps[0].j != j:
                rectangle = canvas.create_rectangle(x, y, x + block_size, y + block_size, fill='white', outline='#ddd', width=2)
                text = canvas.create_text(x_center, y_center, text=steps[0].matrix[i][j], font=('Arial', 24))

                rectangles_row.append(rectangle)
                texts_row.append(text)
            else:
                rectangles_row.append(None)
                texts_row.append(None)

            rectangles_row_pos.append([x, y])
            texts_row_pos.append([x_center, y_center])

        rectangles.append(rectangles_row)
        texts.append(texts_row)

        rectangles_pos.append(rectangles_row_pos)
        texts_pos.append(texts_row_pos)

    def update(step = 0):
        if step == len(steps) - 1:
            return
        
        i0 = steps[step + 1].i
        j0 = steps[step + 1].j

        i1 = steps[step].i
        j1 = steps[step].j

        rectangle_delta = [
            (rectangles_pos[i1][j1][0] - rectangles_pos[i0][j0][0]) / movement_frames,
            (rectangles_pos[i1][j1][1] - rectangles_pos[i0][j0][1]) / movement_frames
        ]
        
        text_delta = [
            (texts_pos[i1][j1][0] - texts_pos[i0][j0][0]) / movement_frames,
            (texts_pos[i1][j1][1] - texts_pos[i0][j0][1]) / movement_frames
        ]
        
        prev_rectangles_pos = rectangles_pos[i0][j0].copy()
        prev_texts_pos = texts_pos[i0][j0].copy()
        
        def move(counter = 0):
            if counter == movement_frames:
                rectangles[i0][j0], rectangles[i1][j1] = rectangles[i1][j1], rectangles[i0][j0]
                texts[i0][j0], texts[i1][j1] = texts[i1][j1], texts[i0][j0]
                
                rectangles_pos[i1][j1] = prev_rectangles_pos
                texts_pos[i1][j1] = prev_texts_pos
                
                rectangles_pos[i0][j0], rectangles_pos[i1][j1] = rectangles_pos[i1][j1], rectangles_pos[i0][j0]
                texts_pos[i0][j0], texts_pos[i1][j1] = texts_pos[i1][j1], texts_pos[i0][j0]
                
                return
            
            rectangles_pos[i0][j0][0] += rectangle_delta[0]
            rectangles_pos[i0][j0][1] += rectangle_delta[1]
            
            texts_pos[i0][j0][0] += text_delta[0]
            texts_pos[i0][j0][1] += text_delta[1]
            
            if counter == movement_frames - 1:
                rectangles_pos[i0][j0] = rectangles_pos[i1][j1].copy()
                texts_pos[i0][j0] = texts_pos[i1][j1].copy()
            
            canvas.moveto(rectangles[i0][j0], *rectangles_pos[i0][j0])
            canvas.moveto(texts[i0][j0], *texts_pos[i0][j0])
            
            canvas.after(movement_time // movement_frames, move, counter + 1)

        move()
        
        canvas.after(movement_time + interval_time, update, step + 1)

    root.after(1000, update)

    root.mainloop()

start = NPuzzleState([
 [7, 15, 2, 13],
 [6, 10, 12, 9],
 [11, 3, 14, 8],
 [4, 0, 1, 5]
])

goal = NPuzzleState.goal(15)

print('-' * 10 + f' START ' + '-' * 10)
print(start)

print('-' * 10 + f' GOAL ' + '-' * 10)
print(goal)

bidirectional_astar.search(start, goal)

print('-' * 10 + f' {len(bidirectional_astar.path)} STEPS ' + '-' * 10)

draw(bidirectional_astar.path)