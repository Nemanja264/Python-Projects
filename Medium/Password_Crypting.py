from cryptography.fernet import Fernet

def write_key():
    key=Fernet.generate_key()
    with open("key.key", "wb") as kf:
        kf.write(key)

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

def acc_name_input():
    while True:
        acc_name = input("Account name: ")
        with open('password.txt', 'r') as file:
            acc_names = [line.split(" ")[0] for line in file]
        if acc_name in acc_names:
            print("This account name is already taken!")
            continue
        else:
            return acc_name

def view():
    with open('password.txt', 'r') as f:
        for line in f:
            data=line.strip()
            user,passw=data.split(" ")
            print(f"User: {user} Password: {fer.decrypt(passw.encode()).decode()}")

def add():
    acc_name=acc_name_input()
    pwd=input("Password: ")

    with open('password.txt', 'a') as f:
        f.write(f'{acc_name} {fer.encrypt(pwd.encode()).decode()}\n')

#master_pwd = input("Input master password: ")
key = load_key()
fer = Fernet(key)

while True:
    mode=input("Would you like to view or add a new password? To quit press q! ").lower()
    if mode=='q':
        break

    if mode=="view":
        view()
    elif mode=="add":
        add()
    else:
        print("Invalid mode!")
        continue
