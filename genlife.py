#!/usr/bin/python
""" Graphical interface for input file generator """
from Tkinter import Tk, Canvas, Button, Frame, BOTH, NORMAL, HIDDEN
from gameoflife import advance

def gen_draw(gen_e):
    """ Draw the Game """
    gen_ii = (gen_e.y-3) / gen_cell_size
    gen_jj = (gen_e.x-3) / gen_cell_size
    gen_canvas.itemconfig(gen_cell_matrix[gen_addr(gen_ii, gen_jj)], state=NORMAL, tags='vis')

def gen_addr(gen_ii, gen_jj):
    """ Setup a cell position  by coordinate """
    if gen_ii < 0 or gen_jj < 0 or gen_ii >= gen_field_height or gen_jj >= gen_field_width:
        return len(gen_cell_matrix)-1
    else:
        return gen_ii * (gen_width / gen_cell_size) + gen_jj

#def gen_mark_fields():
    """ Mark hidden fields """
"""
    for i in xrange(gen_field_height):
        for j in xrange(gen_field_width):
            if gen_canvas.gettags(gen_cell_matrix[gen_addr(i, j)])[0] == 'vis':
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=NORMAL, tags=('vis', 'to_vis'))
            else:
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=HIDDEN, tags=('hid', 'to_hid'))
"""

def gen_mark_fields_advance(board):
    """ Mark hidden fields """
    for i in xrange(gen_field_height):
        for j in xrange(gen_field_width):
            if (i, j) in board:
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=NORMAL, tags=('vis', 'to_vis'))
            else:
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=HIDDEN, tags=('hid', 'to_hid'))


def gen_repaint():
    """ Paint game field """
    for i in xrange(gen_field_height):
        for j in xrange(gen_field_width):
            if gen_canvas.gettags(gen_cell_matrix[gen_addr(i, j)])[1] == 'to_hid':
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=HIDDEN, tags=('hid', '0'))
            if gen_canvas.gettags(gen_cell_matrix[gen_addr(i, j)])[1] == 'to_vis':
                gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=NORMAL, tags=('vis', '0'))


def gen_life_file():
    """ Generate file toad.live """
    newstate = set()
# Open file
    gen_f = open(gen_file, 'w')
# Write comments
    gen_f.write(gen_ignored + '\n')

    for i in xrange(gen_field_height):
# Start new line
        gen_str = ''
        for j in xrange(gen_field_width):
            if gen_canvas.gettags(gen_cell_matrix[gen_addr(i, j)])[0] == 'vis':
                gen_str = gen_str + 'O'
                newstate.add((i, j))
            else:
                gen_str = gen_str + '.'
# Write string of file
        gen_f.write(gen_str + '\n')

#Close file
    gen_f.close()
    return newstate


def gen_generate():
    """ Generate toad.life file """
    board = gen_life_file()
    board = advance(board, [3], [2,3])
#    gen_mark_fields()
    gen_mark_fields_advance(board)
    gen_repaint()

def gen_clear():
    """ Clear all game field """
    for i in xrange(gen_field_height):
        for j in xrange(gen_field_width):
            gen_canvas.itemconfig(gen_cell_matrix[gen_addr(i, j)], state=HIDDEN, tags=('hid', '0'))


gen_file = 'toad.life'
gen_ignored = '!Name: Toad\n!'

gen_root = Tk()
gen_root.title('Generator Game of Life')
gen_width = 350
gen_height = 370
config_string = "{0}x{1}".format(gen_width, gen_height + 32)
gen_color = "green"
# possible write just '350x370'
gen_root.geometry(config_string)
gen_cell_size = 20
gen_canvas = Canvas(gen_root, height=gen_height)
gen_canvas.pack(fill=BOTH)

gen_field_height = gen_height / gen_cell_size
gen_field_width = gen_width / gen_cell_size

# Make a 2D array of cell
gen_cell_matrix = []
for i in xrange(gen_field_height):
    for j in xrange(gen_field_width):
        # Create a cell
        gen_square = gen_canvas.create_rectangle(2 + gen_cell_size*j, 2 + gen_cell_size*i, gen_cell_size + gen_cell_size*j - 2, gen_cell_size + gen_cell_size*i - 2, fill=gen_color)
        # Make this cell hidden
        gen_canvas.itemconfig(gen_square, state=HIDDEN, tags=('hid', '0'))
        gen_cell_matrix.append(gen_square)
# It is a dummy element, it's kind of out of the box everywhere
gen_fict_square = gen_canvas.create_rectangle(0, 0, 0, 0, state=HIDDEN, tags=('hid', '0'))
gen_cell_matrix.append(gen_fict_square)


# Add glider
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(3, 3)], state=NORMAL, tags='vis')
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(3, 4)], state=NORMAL, tags='vis')
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(3, 5)], state=NORMAL, tags='vis')
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(4, 2)], state=NORMAL, tags='vis')
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(4, 3)], state=NORMAL, tags='vis')
gen_canvas.itemconfig(gen_cell_matrix[gen_addr(4, 4)], state=NORMAL, tags='vis')
# Add board. It is diferent representation the game fild
board = set()


# Setup frame of window and buttons
gen_frame = Frame(gen_root)
gen_button1 = Button(gen_frame, text='Generate', command=gen_generate)
gen_button2 = Button(gen_frame, text='Clear', command=gen_clear)
gen_button1.pack(side='left')
gen_button2.pack(side='right')
gen_frame.pack(side='bottom')

# Event binding
gen_canvas.bind('<B1-Motion>', gen_draw)
gen_canvas.bind('<ButtonPress>', gen_draw)

# Infiniteloop
gen_root.mainloop()
