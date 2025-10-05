from contextlib import AbstractContextManager
import sqlite3

class PrintRed:
    def __enter__(self):
        print("\033[31;10m", end="")
        return self # don't forget this!

    def __exit__(self, exc_type, exc_value, traceback):
        print("\033[0m", end="")
        return False


class OpenDB(AbstractContextManager):
    def __init__(self, db_path=".db.sqlite"):
        self.db_path = db_path
        self.db = sqlite3.connect(self.db_path)
        
    def add(self, content="Something to add"):
        print(f"{content}\nwill be added to the DB")
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
        return True
    
class IgnoreZeroDiv(AbstractContextManager):
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type.__name__ == 'ZeroDivisionError':
            line = traceback.tb_lineno
            print(f"We pretend you didn't divide by zero in line {line}")
            return True
        return False



def main():
    print("PrintRed")
    print("--------")
    print("Before context")
    with PrintRed() as c:
        print("Within context...")
        print("...more in context")
    print("After context")
    print()
    print("OpenDB")
    print("------")
    with OpenDB() as db:
        db.add()
    print()
    print("IgnoreZeroDiv")
    print("-------------")
    with IgnoreZeroDiv() as _:
        x = 1/0
        print(f"We won't arrive here: {x}")
        


if __name__ == "__main__":
    main()
