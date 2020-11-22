from hough.hough import getDiceValue
from cnn.cnn import train_cnn
from cnn.cnn import predict_cnn


def main():
    print(getDiceValue("images/d_02/20201025_170644.jpg"))

    # train_cnn()
    predict_cnn('images/d_02/im_93.jpg')

if __name__ == '__main__':
    main()

