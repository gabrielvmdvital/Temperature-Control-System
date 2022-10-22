import json


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

with open(r"src\config\config.json", encoding='utf-8') as fp:
    data = json.load(fp)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(type(data))
    print(data)


