from argparse import ArgumentParser
import numpy as np
from PIL import Image

def initialize_grid(N: int) -> np.ndarray:
    """Creates the initial state of the board.

    Args:
        N (int): Length of a side of the grid.

    Returns:
        np.ndarray: An NxN grid containing only 0s & 1s.
    """

    print("Creating grid")

    ###########################################################
    # Make a random array of shape (N, N), containing 0s and 1s
    ###########################################################

    grid = np.random.choice([0, 1], size=(N, N), p=[0.9, 0.1])

    return grid



def get_neighbours(i,j,grid):
    """gets the neighbours of current cell of the current grid.

    Args:
        i (int): row number of the cell.
        j (int): column number of the cell.
        grid (np.ndarray) : the current grid.

    Returns:
        int : total number of neighbours.
    """
    
    N = len(grid)
    neighbours = 0

    for p in range(i-1, i+2):
        for q in range(j-1, j+2):

            if p == i and q == j:
                continue

            if p == N:
                p = 0
            if q == N:
                q = 0

            neighbours += grid[p][q]

    return neighbours
            


def update_grid(grid: np.ndarray) -> np.ndarray:
    """Applies the update rule to the current grid and returns the next grid state.

    Args:
        grid (np.ndarray): Current grid.

    Returns:
        np.ndarray: Next grid.
    """
    
    print("Updating grid.")

    # If grid[i, j] == 1, it is a "live" cell; if 0, it is a "dead" cell.
    #
    # Any cell grid[i, j] has exactly 8 neighbours (the surrounding cells).
    #
    # Cells at the borders also have 8 neighbours, because the borders are continuous.
    # That is, the cell above (0, j) is (N-1, j); the cell to the right of (i, N-1) is (i, 0).
    #
    # Under the above conditions, applying the following rules:
    #
    # 1. Underpopulation: Any live cell with less than 2 live neighbours becomes a dead cell.
    # 2. Overpopulation: Any live cell with more than 3 live neighbours becomes a dead cell.
    # 3. Healthy: Any live cell with 2 or 3 live neighbours survives and remains a live cell.
    # 4. Reproduction: At any dead cell with exactly 3 live neighbours, a new live cell is born.

    N = len(grid)
    output_grid = np.zeros((N,N), dtype=int)

    for i in range(N):
        for j in range(N):
            current_cell = grid[i][j]
            neighbours = get_neighbours(i,j,grid)

            if neighbours == 3:
                new_cell = 1
            elif neighbours < 2 or neighbours > 3:
                new_cell = 0
            else:
                new_cell = current_cell

            output_grid[i][j] = new_cell

    return output_grid
            



def game_of_life(N: int, T: int, O: str):
    """Runs the game of life for T seconds on an NxN grid.

    Args:
        N (int): Board size
        T (int): Time
        O (str): Name of output file
    """
    
    print("Starting game.")
   
    # 1. Initializing a start_grid with initialize_grid()
    #
    # 2. Calling update_grid() T times. Storing each output grid in a list.
    #
    # 3. Creating a gif animation called "output.gif" with T + 1 grid images (start grid + T updated grids).
  
    
    grid = initialize_grid(N)
    results = []
    results.append(Image.fromarray(256 * grid.astype(np.uint8)).convert('RGB').resize((256,256)))

    for t in range(T):
        grid = update_grid(grid)
        results.append(Image.fromarray(256 * grid.astype(np.uint8)).convert('RGB').resize((256,256)))

    results[0].save(O,
               save_all=True, append_images=results[1:],duration=150, loop=0)



    

if __name__ == "__main__":
    parser = ArgumentParser("Run: python3 game_of_life.py --N 8 --T 15")
    parser.add_argument("--N", type=int, required=True, help="Size of grid.")
    parser.add_argument("--T", type=int, required=True, help="How many timesteps to observe.")
    parser.add_argument("--O", type=str, default="output.gif", help="Name of output.gif file.")
    args = parser.parse_args()

    game_of_life(args.N, args.T, args.O)