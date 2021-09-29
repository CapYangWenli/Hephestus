class IncorrectInput(Exception):
    pass

def StringToTuple(txt):
    tp = tuple(map(int, txt.split(', ')))

    return tp

def main():
    print("Please enter three numbers in tuple")
    txt = raw_input()
    print(StringToTuple(txt))

if __name__ == "__main__":
    main()