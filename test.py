import sys

def test(i: int) -> None:
    if i < 9000:
        test(i + 1)
    print(i)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    test(0)