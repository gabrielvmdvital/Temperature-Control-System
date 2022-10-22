import json

with open(r"src\config\config.json", encoding='utf-8') as fp:
    data = json.load(fp)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(type(data))
    print(data)


