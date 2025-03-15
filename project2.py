import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3
VAL=40

bet_symbols = {
    "A": 2, "B": 4, "C": 6, "D": 8
}

def check_winnings(columns, lines, bet):
    winnings=0
    for line in range(lines):
        symbol=columns[0][line]
        for column in columns[1:]:
            symbol_to_check=column[line]
            if symbol!=symbol_to_check:
                break
        else:
            winnings += VAL/bet_symbols[symbol] * bet

    return winnings

def get_slot_spin(rows,cols,symbols):
    all_symbols=[]
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns=[]
    for _ in range(cols):
        column=[]
        current_symbols=all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot(columns):
    print("\nSlot machine:")
    for row in zip(*columns):
        print(*row, sep=" | ")

def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Enter number greater than zero")
    else:
        print("Please enter a number")

    return amount

def number_of_lines():
    while True:
        lines=input("Enter number of lines to bet on 1-3: ")
        if lines.isdigit():
            lines = int(lines)
            if 1<= lines <=MAX_LINES:
                break
            else:
                print("Enter a valid number of lines")

    return lines

def get_bet():
    while True:
        amount = input("How much would you like to bet? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Bet must be between {MIN_BET} and {MAX_BET}$")
        else:
            print("Please enter a number")

    return amount

def valid_bet(bet, balance, lines):
    while True:
        total_bet = bet * lines
        if total_bet > balance:
            print(f"Bet cant be higher than your current balance: {balance}")
            bet = get_bet()
        else:
            return bet, total_bet

def check_balance(balance):
    if balance < 1:
        deposit_more = input("No more resources, do you want to deposit more? [y/n] ").lower()
        if deposit_more == 'y':
            return deposit()
        else:
            quit()
    else:
        return 0

def spin(balance):
    lines = number_of_lines()
    bet, total_bet = valid_bet(get_bet(), balance, lines)

    print(f"\nYou are betting ${bet} on each of {lines} lines. Total bet is: ${total_bet}")
    balance -= total_bet
    print(f"Your balance is now: ${balance}$")

    slots = get_slot_spin(ROWS, COLS, bet_symbols)
    print_slot(slots)

    winnings = round(check_winnings(slots, lines, bet), 2)
    if winnings > 0:
        balance += winnings
        balance = round(balance, 2)
        print(f"You won: ${winnings}, Current balance: ${balance}")
    else:
        print(f"You lost, Current balance: ${balance}")

    return balance

def main():
    balance = deposit()

    while True:
        balance = spin(balance)

        if input("\nWant to bet more(press enter)? To quit type 'q' ").lower() == 'q':
            quit()

        balance += check_balance(balance)


main()
