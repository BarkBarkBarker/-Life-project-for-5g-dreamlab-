from tkinter import *  # library for drawing
import random


def check_neighbours(x, y):
    """
    Checking neighbour cells for condition of born or death
    :param x: x of cell
    :param y: y of cell
    :return: True if cell should change status, False if nothing to change
    """
    num_of_living = 0  # number of living neighbours

    for i in range(-1, 2):  # run through all neighbours in 3x3 area without center(current cell) and count living
        for j in range(-1, 2):
            if blocks_n_x - 1 >= (x + i) >= 0 and blocks_n_y - 1 >= (y + j) >= 0 and not (i == 0 and j == 0):
                if cells[x + i][y + j]:
                    num_of_living += 1

    # check what have to do with a cell
    if 2 <= num_of_living <= 3 and cells[x][y]:  # no need to change
        return False
    elif (num_of_living == 3 and not cells[x][y]) or (
            (3 < num_of_living or num_of_living< 2) and cells[x][y]):  # need to change (born or kill)
        return True


def start_random():
    """
    Place starting cells in random position, numbers of cells gets from entry window
    :return: nothing
    """
    global game_flag  # stop the game
    if game_flag:  #
        start_stop_game()  #

    for i in range(blocks_n_x):  # clear previous data
        for j in range(blocks_n_y):  #
            cells[i][j] = False  #
            canvas.itemconfig(blocks_of_cells[i][j], fill="white")

    try:  # gets number from entry, if it out of limits, set as this limit;
        N_entry = int(entry_rand.get())
        if N_entry < 0:
            N_entry = 0
        elif N_entry > blocks_n_x*blocks_n_y:
            N_entry = blocks_n_x*blocks_n_y
    except ValueError:  # if not int or not entered set as 150
        N_entry = 150

    for i in range(N_entry):  # filling N-pcs of random cells
        x_rand = random.randint(0, blocks_n_x - 1)
        y_rand = random.randint(0, blocks_n_y - 1)
        cells[x_rand][y_rand] = True  # change status
        canvas.itemconfig(blocks_of_cells[x_rand][y_rand], fill="green")  # change color of block


def start_stop_game():
    """
    Starting or stopping the game, called from button
    :return: nothing
    """
    global game_flag
    if game_flag:
        game_flag = False
        but_start_stop['text'] = 'Start'
        but_start_stop['bg'] = 'Green'
    else:
        game_flag = True
        but_start_stop['text'] = 'Stop'
        but_start_stop['bg'] = 'Red'
        iteration()


def iteration():
    global game_flag
    """
    One iteration of game: running through all cells, checking for conditions and changing status if need
    :return: nothing
    """
    changing = False  # flag for the case if no changes during iteration to stop run
    for i in range(blocks_n_x):
        for j in range(blocks_n_y):
            if check_neighbours(i, j):
                if game_flag:  # check for the case if game was stopped during run in iteration
                    changing = True
                    if cells[i][j]:  # killing a living cell (True -> False)
                        canvas.itemconfig(blocks_of_cells[i][j], fill="white")
                    else:  # born from dead cell (False -> True)
                        canvas.itemconfig(blocks_of_cells[i][j], fill="green")
                    cells[i][j] = not cells[i][j]  # swap status
    if not changing and game_flag:
        start_stop_game()
    if game_flag:  # doing loop with timing of fps
        root.after(int(1000 / fps), iteration)


# constants declaration
WIDTH = 800  # width of canvas
HEIGHT = 600  # height of canvas
block_size = 20  # length of block(one cell) in px
fps = 10  # number of iterations (frames) per second
blocks_n_x = int(WIDTH / block_size)  # number of blocks in horizontal axis
blocks_n_y = int(HEIGHT / block_size)  # number of blocks in vertical axis

game_flag = False  # main flag for game running

# initialise Tkinter windows and buttons
root = Tk()
root.title("Life")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
buttons = Frame(root)  # frame with buttons and entry
but_rand = Button(buttons, text="Randomly place cells", command=start_random, width=20, height=1)
but_start_stop = Button(buttons, text="Start", command=start_stop_game, width=20, height=1, bg='green', fg='white')
entry_rand = Entry(buttons, width=75)
entry_rand.insert(0, 'Enter the integer number of starting random points, default = 150')
entry_rand.pack(side=LEFT)
but_rand.pack(side=LEFT)
but_start_stop.pack(side=LEFT)
buttons.pack()
canvas.pack()

for i in range(0, WIDTH, block_size):  # draw vertical and horizontal lines of field
    canvas.create_line(i, 0, i, HEIGHT, tag='lines')  #
for i in range(0, HEIGHT, block_size):  #
    canvas.create_line(0, i, WIDTH, i, tag='lines')  #

# declaration of arrays - statuses and blocks (rectangles of Tkinter) for every cell;
# in default all cells are dead, blocks are white; size of field= 40x30
cells = []
blocks_of_cells = []
for i in range(blocks_n_x):
    cells.append([])
    blocks_of_cells.append([])
    for j in range(blocks_n_y):
        cells[i].append(False)
        blocks_of_cells[i].append(canvas.create_rectangle(i * block_size, j * block_size, (i + 1) * block_size, (j + 1) * block_size, fill="white", tag='blocks'))

root.mainloop()  # mainloop of Tkinter
