import curses
import random
from curses import wrapper
import time
import threading

TEXT_ROW=0
TIMER_ROW=1

def load_text():
    with open("wpm_text.txt", "r") as f:
        return random.choice(f.readlines()).strip()

def timer_starter(stdscr):
    start_time = time.time()
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=update_timer, args=(stdscr, start_time, stop_event), daemon=True)
    timer_thread.start()

    return start_time, stop_event, timer_thread

def time_stopper(stop_event, timer_thread):
    stop_event.set()
    timer_thread.join()

def display_test_sentence(stdscr, sentence):
    stdscr.clear()
    stdscr.addstr(sentence, curses.color_pair(1))
    stdscr.refresh()

def update_timer(stdscr, start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        stdscr.move(TIMER_ROW,0)
        stdscr.clrtoeol()  # Clear the line before updating
        stdscr.addstr(TIMER_ROW, 0, f"Time: {elapsed_time:.2f} seconds")
        stdscr.refresh()
        time.sleep(0.1)  # Update the timer every 0.1 seconds

def welcome_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing test!")
    stdscr.addstr(2,0,"Press any key to begin:")
    stdscr.refresh()

    stdscr.getkey()
    while True:
        start_test(stdscr)

        stdscr.addstr(3, 0, "Press 'q' to quit or any other key to do more tests")
        if stdscr.getkey() == 'q':
            break

def start_test(stdscr):
    sentence = load_text()
    display_test_sentence(stdscr, sentence)

    start_time, stop_event, timer_thread = timer_starter(stdscr)
    elapsed_time = typing(stdscr, start_time, sentence)
    time_stopper(stop_event, timer_thread)

    print(f"\nYou needed {elapsed_time:.2f} seconds to finish the test")

def typing(stdscr, start_time, sentence):
    current_text=""
    cursor_pos = 0

    while current_text != sentence:
        key = stdscr.getch()

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor_pos > 0:
                current_text = current_text[:-1]
                cursor_pos -= 1
                if cursor_pos < len(sentence):
                    stdscr.addch(TEXT_ROW, cursor_pos, sentence[cursor_pos], curses.color_pair(1))
                else:
                    stdscr.addch(TEXT_ROW, cursor_pos, " ")
                stdscr.move(TEXT_ROW, cursor_pos)
                stdscr.refresh()
            continue

        if cursor_pos < len(sentence) and chr(key) == sentence[cursor_pos]:
            stdscr.addch(TEXT_ROW, cursor_pos, key, curses.color_pair(3))
        else:
            stdscr.addch(TEXT_ROW, cursor_pos, key, curses.color_pair(2))

        current_text += chr(key)
        cursor_pos += 1

        stdscr.refresh()

    return time.time() - start_time


def init_pairs():
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)

def main(stdscr):
    init_pairs()
    welcome_screen(stdscr)


wrapper(main)
