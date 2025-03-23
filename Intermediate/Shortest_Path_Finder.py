import curses
from curses import wrapper
import time
import queue

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def init_color_pairs():
    curses.init_pair(1,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)

def print(stdscr, maze, path=[]):
    stdscr.clear()
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i,row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "*", RED)
            else:
                stdscr.addstr(i,j*2,value, GREEN)
    time.sleep(0.5)
    stdscr.refresh()

def find_start(maze, start):
    for i, row in enumerate(maze):
        if start in row:
            return i, row.index('O')

    return None

def find_path(stdscr, maze):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()
    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        print(stdscr, maze, path)

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            i,j = neighbor
            if maze[i][j] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:
        neighbors.append((row-1, col))
    if row+1 < len(maze):
        neighbors.append((row+1, col))
    if col > 0:
        neighbors.append((row, col-1))
    if col+1 < len(maze[0]):
        neighbors.append((row, col+1))

    return neighbors

def main(stdscr):
    init_color_pairs()

    find_path(stdscr, maze)
    stdscr.getch()

wrapper(main)
