############################ CONSTANTS ############################

STARTX = -14430
STARTY = -9150
ADVANCEX = 3450
ADVANCEY = 7050
CELL_SIZE_X = 675
CELL_SIZE_Y = 2100
CELL_DIR = "Right"
CELL_COLOR = 15
CELL_ICON = "None"

MODEL_HEADER = """Coupled
    {
    Type = Root
    Name = life
    Ports = 0; 0
    Description = 
    Graphic
        {
        Position = 0; 0
        Dimension = 600; 600
        Direction = Right
        Color = 15
        Icon = 
        Window = 5000; 5000; 5000; 5000
        }
    Parameters
        {
        }
    System
        {
"""

MODEL_FOOTER = """        }
    }
"""


############################ SCRIPT ############################


# Function that captures the name of the input file with the parameters (Board size and cells alive).
def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file with the parameters for the model", required=True)
    parser.add_argument("-o", "--output", help="Name of the pdm file with the model written", required=True)

    return parser.parse_args()


# Function that reads and validates the data from the input file.
def read_input_file(input_file):
    with open(input_file, "r") as f:
        board_size = int(f.readline())
        a, b = f.readline().split()
        birth = int(f.readline())
        t = int(f.readline())
        alive_cells = []
        for line in f.readlines():
            #append it as tuple of integers
            alive_cells.append(tuple(map(int, line.split())))

    for cell in alive_cells:
        if cell[0] >= board_size or cell[1] >= board_size:
            raise Exception(f"Invalid cell coordinates. They must be lower than the Board Size: {board_size}. Coord x: {cell[0]}, Coord y: {cell[1]}")
    
    return board_size, alive_cells, int(a), int(b), birth, t
        
         

# Function that writes in a .pdm file all the cell components, with their respective parameters.
def generate_cells(board_size, alive_cells, f):
    cell_number = 0
    
    for i in range(0,board_size):
        for j in range(0, board_size):
            f.write("        Atomic\n")
            f.write("            {\n")
            f.write(f"            Name = Cell{cell_number}\n")
            f.write("            Ports = 8 ; 1\n")
            f.write("            Path = life/cell.h\n")
            f.write("            Description = Cell representation for Game of Life\n")
            f.write("            Graphic\n")
            f.write("                {\n")
            f.write(f"                Position = {STARTX + (ADVANCEX * j)} ; {STARTY + (ADVANCEY * i)}\n")
            f.write(f"                Dimension = {CELL_SIZE_X} ; {CELL_SIZE_Y}\n")
            f.write(f"                Direction = {CELL_DIR}\n")
            f.write(f"                Color = {CELL_COLOR}\n")
            f.write(f"                Icon = {CELL_ICON}\n")
            f.write("                }\n")
            f.write("            Parameters\n")
            f.write("                {\n")
            if (j,i) in alive_cells:
                f.write("                isAlive = Str; 1 ;\n")
            else:
                f.write("                isAlive = Str; 0 ;\n")
            
            # If cell_number it's a corner cell
            if (cell_number == 0 or cell_number == (board_size - 1) or cell_number == (board_size * board_size - board_size) or cell_number == ((board_size * board_size) - 1)):
                f.write(f"                maxNeighbors = Str; 3 ;\n")
            # If cell_number it's a border cell
            elif (cell_number < board_size or cell_number % board_size == 0 or cell_number % board_size == (board_size - 1) or cell_number > (board_size * board_size - board_size)):
               f.write(f"                maxNeighbors = Str; 5 ;\n")
            # If cell_number it's a center cell
            else:
                f.write(f"                maxNeighbors = Str; 8 ;\n")
            f.write(f"                name = Str; Cell{cell_number} ;\n")
            f.write("                }\n")            
            f.write("            }\n")

            cell_number += 1


# Function that calculates the coordinates to draw the conections between the cells.
def get_corresponding_row_and_col(cell_number, board_size):
    corresponding_row = ADVANCEY * ((cell_number-1) // board_size)
    corresponding_col = ADVANCEX * ((cell_number-1) % board_size)
    return corresponding_row, corresponding_col


# Function that writes in a .pdm file the lines that connects a current cell with its left-hand cell.
def generate_line_to_left_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number-1} ;  1 ; -1\n")
    write_points_for_line_to_left_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its left-hand cell.
def write_points_for_line_to_left_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13650 + corresponding_col} ; {-18075 + corresponding_col} ; {-18075 + corresponding_col} ; {-18015 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-9450 + corresponding_row} ; {-9450 + corresponding_row} ; {-9000 + corresponding_row} ; {-9000 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-9300 + corresponding_row} ; {-9300 + corresponding_row} ; {-9000 + corresponding_row} ; {-9000 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-9375 + corresponding_row} ; {-9375 + corresponding_row} ; {-9000 + corresponding_row} ; {-9000 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its lower left-hand cell.
def generate_line_to_lower_left_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number+board_size-1} ;  2 ; -1\n")
    write_points_for_line_to_lower_left_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its lower left-hand cell.
def write_points_for_line_to_lower_left_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13350 + corresponding_col} ; {-13350 + corresponding_col} ; {-18150 + corresponding_col} ; {-18150 + corresponding_col} ; {-18015 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-4800 + corresponding_row} ; {-4800 + corresponding_row} ; {-1650 + corresponding_row} ; {-1650 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-6000 + corresponding_row} ; {-6000 + corresponding_row} ; {-1650 + corresponding_row} ; {-1650 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-5400 + corresponding_row} ; {-5400 + corresponding_row} ; {-1650 + corresponding_row} ; {-1650 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its lower cell.
def generate_line_to_lower_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number+board_size} ;  3 ; -1\n")
    write_points_for_line_to_lower_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its lower cell.
def write_points_for_line_to_lower_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13275 + corresponding_col} ; {-13275 + corresponding_col} ; {-14775 + corresponding_col} ; {-14775 + corresponding_col} ; {-14565 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-6525 + corresponding_row} ; {-6525 + corresponding_row} ; {-1425 + corresponding_row} ; {-1425 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-5925 + corresponding_row} ; {-5925 + corresponding_row} ; {-1425 + corresponding_row} ; {-1425 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-5325 + corresponding_row} ; {-5325 + corresponding_row} ; {-1425 + corresponding_row} ; {-1425 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its lower right-hand cell.
def generate_line_to_lower_right_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number+board_size+1} ;  4 ; -1\n")
    write_points_for_line_to_lower_right_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its lower right-hand cell.
def write_points_for_line_to_lower_right_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13200 + corresponding_col} ; {-13200 + corresponding_col} ; {-11400 + corresponding_col} ; {-11400 + corresponding_col} ; {-11115 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-6450 + corresponding_row} ; {-6450 + corresponding_row} ; {-1200 + corresponding_row} ; {-1200 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-5850 + corresponding_row} ; {-5850 + corresponding_row} ; {-1200 + corresponding_row} ; {-1200 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-5250 + corresponding_row} ; {-5250 + corresponding_row} ; {-1200 + corresponding_row} ; {-1200 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its right-hand cell.
def generate_line_to_right_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number+1} ;  5 ; -1\n")
    write_points_for_line_to_right_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its right-hand cell.
def write_points_for_line_to_right_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13125 + corresponding_col} ; {-13125 + corresponding_col} ; {-11115 + corresponding_col}\n")
    f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-8025 + corresponding_row} ; {-8025 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its upper right-hand cell.
def generate_line_to_upper_right_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number-board_size+1} ;  6 ; -1\n")
    write_points_for_line_to_upper_right_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its upper right-hand cell.
def write_points_for_line_to_upper_right_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13425 + corresponding_col} ; {-13425 + corresponding_col} ; {-12150 + corresponding_col} ; {-12150 + corresponding_col} ; {-11115 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-11100 + corresponding_row} ; {-11100 + corresponding_row} ; {-14850 + corresponding_row} ; {-14850 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-9900 + corresponding_row} ; {-9900 + corresponding_row} ; {-14850 + corresponding_row} ; {-14850 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-10500 + corresponding_row} ; {-10500 + corresponding_row} ; {-14850 + corresponding_row} ; {-14850 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its upper cell.
def generate_line_to_upper_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number-board_size} ;  7 ; -1\n")
    write_points_for_line_to_upper_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its upper cell.
def write_points_for_line_to_upper_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13500 + corresponding_col} ; {-13500 + corresponding_col} ; {-15375 + corresponding_col} ; {-15375 + corresponding_col} ; {-14565 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-11025 + corresponding_row} ; {-11025 + corresponding_row} ; {-14550 + corresponding_row} ; {-14550 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-9825 + corresponding_row} ; {-9825 + corresponding_row} ; {-14550 + corresponding_row} ; {-14550 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-10425 + corresponding_row} ; {-10425 + corresponding_row} ; {-14550 + corresponding_row} ; {-14550 + corresponding_row}\n")


# Function that writes in a .pdm file the lines that connects a current cell with its upper left-hand cell.
def generate_line_to_upper_left_cell(cell_number, board_size, f):
    f.write("        Line\n")
    f.write("            {\n")
    f.write(f"            Source = Cmp ;  {cell_number} ;  1 ; 0\n")
    f.write(f"            Sink = Cmp ;  {cell_number-board_size-1} ;  8 ; -1\n")
    write_points_for_line_to_upper_left_cell(cell_number, board_size, f)
    f.write("            }\n")

# Function that writes the x and y coords for the line that connects a current cell with its upper left-hand cell.
def write_points_for_line_to_upper_left_cell(cell_number, board_size, f):
    corresponding_row, corresponding_col = get_corresponding_row_and_col(cell_number, board_size)
    f.write(f"            PointX = {-13650 + corresponding_col} ; {-13575 + corresponding_col} ; {-13575 + corresponding_col} ; {-18750 + corresponding_col} ; {-18750 + corresponding_col} ; {-18015 + corresponding_col}\n")
    if (cell_number % 3 == 1):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-10950 + corresponding_row} ; {-10950 + corresponding_row} ; {-14325 + corresponding_row} ; {-14325 + corresponding_row}\n")
    elif (cell_number % 3 == 2):
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-11550 + corresponding_row} ; {-11550 + corresponding_row} ; {-14325 + corresponding_row} ; {-14325 + corresponding_row}\n")
    else:
        f.write(f"            PointY = {-8100 + corresponding_row} ; {-8100 + corresponding_row} ; {-10350 + corresponding_row} ; {-10350 + corresponding_row} ; {-14325 + corresponding_row} ; {-14325 + corresponding_row}\n")


# Function that distinguishes between the different types of cells and calls the appropriate function to generate the lines that connect the current cell with its neighbors.
def generate_lines(board_size, f):
    cell_number = 1
    for i in range(board_size*board_size):
        if cell_number == 1:                                            # Upper left corner cell
            generate_line_to_lower_cell(cell_number, board_size, f)
            generate_line_to_lower_right_cell(cell_number, board_size, f)
            generate_line_to_right_cell(cell_number, board_size, f)
        
        elif cell_number == board_size:                                 # Upper right corner cell
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_lower_left_cell(cell_number, board_size, f)
            generate_line_to_lower_cell(cell_number, board_size, f)

        elif cell_number == (board_size * board_size - board_size) + 1: # Bottom left corner cell
            generate_line_to_right_cell(cell_number, board_size, f)
            generate_line_to_upper_right_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)

        elif cell_number == (board_size * board_size):                  # Bottom right corner cell
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)
            generate_line_to_upper_left_cell(cell_number, board_size, f)
        
        elif cell_number < board_size:                                  # Upper Edge cells
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_lower_left_cell(cell_number, board_size, f)
            generate_line_to_lower_cell(cell_number, board_size, f)
            generate_line_to_lower_right_cell(cell_number, board_size, f)
            generate_line_to_right_cell(cell_number, board_size, f)

        elif cell_number % board_size == 0:                             # Right Edge cells
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_lower_left_cell(cell_number, board_size, f)
            generate_line_to_lower_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)
            generate_line_to_upper_left_cell(cell_number, board_size, f)

        elif cell_number % board_size == 1:                             # Left Edge cells
            generate_line_to_lower_cell(cell_number, board_size, f)
            generate_line_to_lower_right_cell(cell_number, board_size, f)
            generate_line_to_right_cell(cell_number, board_size, f)
            generate_line_to_upper_right_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)
        
        elif cell_number > (board_size * board_size - board_size):      # Bottom Edge cells
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_right_cell(cell_number, board_size, f)
            generate_line_to_upper_right_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)
            generate_line_to_upper_left_cell(cell_number, board_size, f)

        else:                                                           # Center cells
            generate_line_to_left_cell(cell_number, board_size, f)
            generate_line_to_lower_left_cell(cell_number, board_size, f)
            generate_line_to_lower_cell(cell_number, board_size, f)
            generate_line_to_lower_right_cell(cell_number, board_size, f)
            generate_line_to_right_cell(cell_number, board_size, f)
            generate_line_to_upper_right_cell(cell_number, board_size, f)
            generate_line_to_upper_cell(cell_number, board_size, f)
            generate_line_to_upper_left_cell(cell_number, board_size, f)

        cell_number += 1


# Function that generates the constants.h file with the parameters for the model.
def write_constants(a, b, birth, transition_time, file_name):
    f = open(file_name, "w")
    f.write("#if !defined constants_h\n")
    f.write("#define constants_h\n")
    f.write(f"\n")
    f.write(f"const int A = {a};\n")
    f.write(f"const int B = {b};\n")
    f.write(f"const int BIRTH = {birth};\n")
    f.write(f"const int TRANSITION_TIME = {transition_time};\n")
    f.write(f"const int NEIGHBORS_AMOUNT = 8;\n")
    f.write(f"\n")
    f.write(f"#endif\n")
    f.close()


# Function that generates the model with the corresponding amount of cells and all its connections.
def generate_model(board_size, alive_cells, a, b, birth, transition_time, file_name):
    write_constants(a, b, birth, transition_time, "atomics/life/constants.h")
    f = open(file_name, "w")
    f.write(MODEL_HEADER)
    generate_cells(board_size, alive_cells, f)
    generate_lines(board_size, f)
    f.write(MODEL_FOOTER)
    f.close()

# Main function.
if __name__ == "__main__":
    args = parse_args()
    board_size, alive_cells, a, b, birth, transition_time = read_input_file(f"game_of_life/input/{args.input}")
    generate_model(board_size, alive_cells, a, b, birth, transition_time, f"examples/{args.output}")

