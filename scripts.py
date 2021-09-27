class IncorrectInput(Exception):
    pass

def StringToTuple(txt):
    tp = tuple(map(int, txt.split(', ')))

    if tp[0] > 100 or tp[0] < 0:
        raise IncorrectInput("The value for motor speed must be from 0 to 100")

    if tp[1] > 90 or tp[1] < -90:
        raise IncorrectInput("The value of servo angle can only be in -90 to 90 range")

    return tuple(map(int, txt.split(', ')))

def main():
    print("Please enter three numbers in tuple")
    txt = input()
    print(StringToTuple(txt))

if __name__ == "__main__":
    main()