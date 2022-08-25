import os

def set_size_file(fileName, w_size):
    filePaht = '/Users/huanglele/Desktop/' + fileName
    print(filePaht)
    while True:
        img_size = (os.path.getsize(filePaht)) / (1024 * 1024)
        print(img_size)
        if img_size > w_size:
            break
        else:
            with open(filePaht, "a+") as f:
                f.write("1234567890009876543211234567890987654323456789098765432123456789000987654321123456789098765432345678909876543212345678900098765432")
    print(img_size)

if __name__ == '__main__':
    set_size_file("1.jpeg", 5)
