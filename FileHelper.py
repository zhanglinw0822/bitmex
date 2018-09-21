import os

def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            list_name.append(file_path)

def read_one_line(filename):
    file = open(filename, 'r')
    line = file.readline()
    return line

def copy(src, dest):
    os.rename(src, dest)

def create(path):
    if os.path.exists(path):
        return
    os.mkdir(path)

if __name__ == '__main__':
    filenames = []
    listdir("E:/bit", filenames)
    for filename in filenames:
        print(read_one_line(filename))
