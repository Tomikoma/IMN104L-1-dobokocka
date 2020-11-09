from hough.hough import getDiceValue
from cnn.cnn import train_cnn


def main():
    print(getDiceValue("images/d_02/20201025_170644.jpg"))

    train_cnn()


if __name__ == '__main__':
    main()

