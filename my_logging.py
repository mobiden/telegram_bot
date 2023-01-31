from datetime import datetime


def create_logs(string: str):
    with open("logs.txt", "a") as l:
        string = str(datetime.now()) + ": " + string
        l.write(str(string) + "\n")
