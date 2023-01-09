def create_logs(string: str):
    with open('logs.txt', 'a') as l:
        l.write(str(string) + '\n')