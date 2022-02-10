import argparse
import os
import time
from tqdm import tqdm
import cv2
import numpy as np
from motorPlate import motor_plate
from nonMotorPlate import nonmotor_plate
import random


def parse_args():
    parser = argparse.ArgumentParser(description='NonMotor license plate generator')
    parser.add_argument('--amount', default=10, type=int, help='amount of license plates')
    parser.add_argument('--save_dir', default='./plate', help='plate save path')
    parser.add_argument('--show_img', action='store_true', help='show the plate')
    parser.add_argument('--number', type=str, help='designated 7-digit license plate number')
    parser.add_argument('--plate_type', type=str, help='designated plate type, option[White/white/Green/green]')
    parser.add_argument('--label_txt_path', default='./plate/label.txt', type=str,
                        help='save img_name & plate_number to path_to_txt')
    parser.add_argument('--rotate_angle', default=30, type=int,
                        help='rotation angle, numpy.random.uniform(-rotate_angle,rotate_angle)')
    args = parser.parse_args()
    return args


def random_index(rate):
    """随机变量的概率函数"""
    #
    # 参数rate为list<int>
    # 返回概率事件的下标索引
    start = 0
    index = 0
    randnum = random.randint(1, sum(rate))

    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index


def plate(number: str, plate_type='Green'):
    if plate_type in ['Yellow', 'Blue', 'yellow', 'blue']:
        bg, plate = motor_plate(number, plate_type)
    else:
        bg, plate = nonmotor_plate(number, plate_type)
    return bg, plate


def rad(x):
    return x * np.pi / 180


def pespective_transform(img, angle_vari=30):
    w, h = img.shape[0:2]
    fov = 42
    anglex = np.random.uniform(-angle_vari, angle_vari)
    angley = np.random.uniform(-angle_vari, angle_vari)
    anglez = np.random.uniform(-angle_vari + 10, angle_vari - 10)

    # 镜头与图像间的距离，21为半可视角，算z的距离是为了保证在此可视角度下恰好显示整幅图像
    z = np.sqrt(w ** 2 + h ** 2) / 2 / np.tan(rad(fov / 2))
    # 齐次变换矩阵
    rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(rad(anglex)), -np.sin(rad(anglex)), 0],
                   [0, -np.sin(rad(anglex)), np.cos(rad(anglex)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    ry = np.array([[np.cos(rad(angley)), 0, np.sin(rad(angley)), 0],
                   [0, 1, 0, 0],
                   [-np.sin(rad(angley)), 0, np.cos(rad(angley)), 0, ],
                   [0, 0, 0, 1]], np.float32)

    rz = np.array([[np.cos(rad(anglez)), np.sin(rad(anglez)), 0, 0],
                   [-np.sin(rad(anglez)), np.cos(rad(anglez)), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]], np.float32)

    r = rx.dot(ry).dot(rz)

    # 四对点的生成
    pcenter = np.array([h / 2, w / 2, 0, 0], np.float32)

    p1 = np.array([0, 0, 0, 0], np.float32) - pcenter
    p2 = np.array([w, 0, 0, 0], np.float32) - pcenter
    p3 = np.array([0, h, 0, 0], np.float32) - pcenter
    p4 = np.array([w, h, 0, 0], np.float32) - pcenter

    dst1 = r.dot(p1)
    dst2 = r.dot(p2)
    dst3 = r.dot(p3)
    dst4 = r.dot(p4)

    list_dst = [dst1, dst2, dst3, dst4]

    org = np.array([[0, 0],
                    [w, 0],
                    [0, h],
                    [w, h]], np.float32)

    dst = np.zeros((4, 2), np.float32)

    # 投影至成像平面
    for i in range(4):
        dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]
        dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]

    warpR = cv2.getPerspectiveTransform(org, dst)

    result = cv2.warpPerspective(img, warpR, (h, w))

    return result


def rotate(image, angle_vari=30):
    angle = np.random.uniform(-angle_vari, angle_vari)
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 10)
    dst = cv2.warpAffine(image, M, (cols, rows))
    return dst


def imgBrightness(img1, c, b):
    rows, cols, channels = img1.shape
    blank = np.zeros([rows, cols, channels], img1.dtype)
    rst = cv2.addWeighted(img1, c, blank, 1 - c, b)
    return rst


if __name__ == '__main__':
    args = parse_args()
    label_list = []
    w = 0
    g = 0
    y = 0
    b = 0
    for i in tqdm(range(args.amount)):
        # assign type
        plate_type_list = ['White', 'Green', 'Yellow', 'Blue']
        rate = [30, 30, 30, 10]
        index = np.random.randint(4)
        if args.plate_type is not None:
            assert args.plate_type in ['White', 'white', 'Green',
                                       'green', 'Yellow', 'yellow', 'Blue',
                                       'blue'], 'plate_type must be White/white/Green/green'
            if args.plate_type in ['White', 'white']:
                index = 0
            else:
                index = 1

        # assign number
        if args.number is not None:
            assert len(args.number) == 7, 'plate number of digits must be 7'
        # generate plate
        cor = plate_type_list[random_index(rate)]
        if cor == 'White':
            w += 1
        elif cor == 'Green':
            g += 1
        elif cor == 'Yellow':
            y += 1
        elif cor == 'Blue':
            b += 1
        plate_img, plate_number = plate(args.number, cor)

        # pespective transform & rotate
        angle_vari = 30
        if args.rotate_angle is not None:
            angle_vari = args.rotate_angle
        plate_img = pespective_transform(plate_img, angle_vari=angle_vari)
        # plate_img = rotate(plate_img, angle_vari=angle_vari)

        # blur
        rd = np.random.randint(20, 40)
        plate_img = cv2.blur(plate_img, (rd, rd))

        # brightness
        c = np.random.randint(5, 15) / 10
        plate_img = imgBrightness(plate_img, c, 50)

        # resize
        weight = np.random.randint(40, 120)
        high = np.random.randint(80, 240)
        plate_img = cv2.resize(plate_img, (high, weight))

        # show
        if args.show_img:
            cv2.imshow("result", plate_img)
            c = cv2.waitKey()

        # save
        img_name = None
        if args.save_dir is not None:
            if not os.path.exists(args.save_dir):
                os.mkdir(args.save_dir)
            img_name = str(time.time()).replace('.', '') + '.jpg'
            path = os.path.join(args.save_dir, img_name)
            cv2.imwrite(path, plate_img)
        if img_name is not None:
            label_list.append('{}{}{}'.format(img_name, '\t', plate_number))
    if args.save_dir is not None:

        print('saved {} white plate images to {}.'.format(w, args.save_dir))
        print('saved {} green plate images to {}.'.format(g, args.save_dir))
        print('saved {} yellow plate images to {}.'.format(y, args.save_dir))
        print('saved {} blue plate images to {}.'.format(b, args.save_dir))
        print('saved total {} images to {}.'.format(args.amount, args.save_dir))
    if args.label_txt_path is not None:
        with open(args.label_txt_path, 'w', encoding='utf8') as f:
            for label in label_list:
                f.writelines(label + '\n')
        print('saved label txt to {}.'.format(args.label_txt_path))
    print('finished!')

