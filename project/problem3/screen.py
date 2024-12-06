import curses
import time

def setup_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0) 
    stdscr.nodelay(1)
    stdscr.timeout(100)

def process_command(command, stdscr):
    stdscr.clear()
    stdscr.addstr(1, 0, f"Processing command: {command}")
    if command == "draw_char":
        draw_char(stdscr)
    elif command == "draw_line":
        draw_line(stdscr)
    else:
        stdscr.addstr(2, 0, "Unknown Command", curses.A_BOLD)

def draw_char(stdscr):
    stdscr.addstr(5, 5, "X", curses.A_BOLD)
    stdscr.refresh()

def draw_line(stdscr):
    max_y, max_x = stdscr.getmaxyx()  
    stdscr.addstr(4, 0, f"Terminal Size: {max_y}x{max_x}")
    
    if max_y < 20 or max_x < 10:
        stdscr.addstr(6, 0, "Terminal is too small to draw line!")
        stdscr.refresh()
        return

    for i in range(10):
        if 6 + i < max_y: 
            stdscr.addstr(6 + i, 5, "-", curses.A_BOLD)
        else:
            break
    stdscr.refresh()

def main(stdscr):
    setup_screen(stdscr)

    # List of commands
    commands = ["draw_char", "draw_line"]

    # Execute commands and display on the screen
    for command in commands:
        process_command(command, stdscr)
        time.sleep(1) 

    # Check if there's enough space to display the exit message
    max_y, max_x = stdscr.getmaxyx()
    if max_y > 12:
        stdscr.addstr(12, 0, "Press any key to exit...")
    else:
        stdscr.addstr(max_y - 1, 0, "Press any key to exit...")

    stdscr.refresh()
    time.sleep(2) 
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
