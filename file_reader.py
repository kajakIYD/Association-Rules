from pathlib import Path


def read(file_path):
    try:
        my_file = Path(file_path)
        if my_file.is_file():
            print('Good, file exists')
        else:
            print('Bad, thewre is not such a file')
        with open(file_path, "r") as f:
            return f.read()
    except IOError:
        print(IOError)
        return -1




