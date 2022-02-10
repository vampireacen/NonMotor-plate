import cv2
import numpy as np


def motor_plate(plate_number: str, plate_type='Yellow'):
    bg_img = ''
    Lu_img = ''
    G_img = ''
    number_suffix = ''
    if plate_type in ['Yellow', 'yellow']:
        bg_img = 'Yellow.png'
        Lu_img = '140_Lu_.png'
        G_img = 'G.png'
        number_suffix = '.png'
    elif plate_type in ['Blue', 'blue']:
        bg_img = 'Blue.png'
        Lu_img = '140_Lu__.png'
        G_img = 'G_.png'
        number_suffix = '_.png'
    if bg_img != '':
        letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U',
                       'V', 'W', 'X', 'Y', 'Z']
        first_part = letter_list[np.random.randint(24)] if np.random.randint(2) == 1 else np.random.randint(10)
        last_part = letter_list[np.random.randint(24)]
        number_ = ''.join(str(i) for i in np.random.randint(0, 10, 3))
        plate = str(first_part) + number_ + last_part
        if plate_number is not None:
            plate = list(plate_number)
    bg = cv2.imread('model_plate/' + bg_img)

    w, h = bg.shape[0:2]
    bg = cv2.circle(bg, (int(h / 2), 200), 20, (0, 0, 0) if plate_type in ['Yellow', 'yellow'] else (255, 255, 255), -1)

    # read img
    Lu = cv2.imread('model_plate/' + Lu_img)
    G_ = cv2.imread('model_plate/' + G_img)
    part1_prefix = '220_down_' if plate[0].isalpha() else '140_'
    part1 = cv2.imread('model_plate/' + part1_prefix + plate[0] + number_suffix)
    part2 = cv2.imread('model_plate/140_' + plate[1] + number_suffix)
    part3 = cv2.imread('model_plate/140_' + plate[2] + number_suffix)
    part4 = cv2.imread('model_plate/140_' + plate[3] + number_suffix)
    part5 = cv2.imread('model_plate/220_down_' + plate[4] + number_suffix)
    # resize
    Lu = cv2.resize(Lu, (250, 250))
    G_ = cv2.resize(G_, (280, 280))
    part1 = cv2.resize(part1, (150, 340))
    part2 = cv2.resize(part2, (150, 340))
    part3 = cv2.resize(part3, (150, 340))
    part4 = cv2.resize(part4, (150, 340))
    part5 = cv2.resize(part5, (150, 340))
    # row,col,channel
    rows_Lu, cols_Lu, channels_Lu = Lu.shape
    rows_G_, cols_G_, channels_G_ = G_.shape
    rows_part1, cols_part1, channels_part1 = part1.shape
    rows_part2, cols_part2, channels_part2 = part2.shape
    rows_part3, cols_part3, channels_part3 = part3.shape
    rows_part4, cols_part4, channels_part4 = part4.shape
    rows_part5, cols_part5, channels_part5 = part5.shape
    # create ROI
    roi_Lu = bg[100:rows_Lu + 100, 100:cols_Lu + 100]
    roi_G_ = bg[100:rows_G_ + 100, 100:cols_G_ + 100]
    roi_part1 = bg[100:rows_part1 + 100, 100:cols_part1 + 100]
    roi_part2 = bg[100:rows_part2 + 100, 100:cols_part2 + 100]
    roi_part3 = bg[100:rows_part3 + 100, 100:cols_part3 + 100]
    roi_part4 = bg[100:rows_part4 + 100, 100:cols_part4 + 100]
    roi_part5 = bg[100:rows_part5 + 100, 100:cols_part5 + 100]
    # create a mask of insert_img and create its inverse mask also
    img2gray_Lu = cv2.cvtColor(Lu, cv2.COLOR_BGR2GRAY)
    ret_Lu, mask_Lu = cv2.threshold(img2gray_Lu, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_Lu = cv2.bitwise_not(mask_Lu)

    img2gray_G_ = cv2.cvtColor(G_, cv2.COLOR_BGR2GRAY)
    ret_G_, mask_G_ = cv2.threshold(img2gray_G_, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_G_ = cv2.bitwise_not(mask_G_)

    img2gray_part1 = cv2.cvtColor(part1, cv2.COLOR_BGR2GRAY)
    ret_part1, mask_part1 = cv2.threshold(img2gray_part1, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_part1 = cv2.bitwise_not(mask_part1)

    img2gray_part2 = cv2.cvtColor(part2, cv2.COLOR_BGR2GRAY)
    ret_part2, mask_part2 = cv2.threshold(img2gray_part2, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_part2 = cv2.bitwise_not(mask_part2)

    img2gray_part3 = cv2.cvtColor(part3, cv2.COLOR_BGR2GRAY)
    ret_part3, mask_part3 = cv2.threshold(img2gray_part3, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_part3 = cv2.bitwise_not(mask_part3)

    img2gray_part4 = cv2.cvtColor(part4, cv2.COLOR_BGR2GRAY)
    ret_part4, mask_part4 = cv2.threshold(img2gray_part4, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_part4 = cv2.bitwise_not(mask_part4)

    img2gray_part5 = cv2.cvtColor(part5, cv2.COLOR_BGR2GRAY)
    ret_part5, mask_part5 = cv2.threshold(img2gray_part5, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_part5 = cv2.bitwise_not(mask_part5)
    # black-out the area of logo in ROI
    img_bg_Lu = cv2.bitwise_and(roi_Lu, roi_Lu, mask=mask_Lu)
    img_bg_G_ = cv2.bitwise_and(roi_G_, roi_G_, mask=mask_G_)
    img_bg_part1 = cv2.bitwise_and(roi_part1, roi_part1, mask=mask_part1)
    img_bg_part2 = cv2.bitwise_and(roi_part2, roi_part2, mask=mask_part2)
    img_bg_part3 = cv2.bitwise_and(roi_part3, roi_part3, mask=mask_part3)
    img_bg_part4 = cv2.bitwise_and(roi_part4, roi_part4, mask=mask_part4)
    img_bg_part5 = cv2.bitwise_and(roi_part5, roi_part5, mask=mask_part5)
    # take only region of logo from insert_img image
    img2_fg_Lu = cv2.bitwise_and(Lu, Lu, mask=mask_inv_Lu)
    img2_fg_G_ = cv2.bitwise_and(G_, G_, mask=mask_inv_G_)
    img2_fg_part1 = cv2.bitwise_and(part1, part1, mask=mask_inv_part1)
    img2_fg_part2 = cv2.bitwise_and(part2, part2, mask=mask_inv_part2)
    img2_fg_part3 = cv2.bitwise_and(part3, part3, mask=mask_inv_part3)
    img2_fg_part4 = cv2.bitwise_and(part4, part4, mask=mask_inv_part4)
    img2_fg_part5 = cv2.bitwise_and(part5, part5, mask=mask_inv_part5)
    # put insert_img in ROI and modify the main image
    dst_Lu = cv2.add(img_bg_Lu, img2_fg_Lu)
    dst_G_ = cv2.add(img_bg_G_, img2_fg_G_)
    dst_part1 = cv2.add(img_bg_part1, img2_fg_part1)
    dst_part2 = cv2.add(img_bg_part2, img2_fg_part2)
    dst_part3 = cv2.add(img_bg_part3, img2_fg_part3)
    dst_part4 = cv2.add(img_bg_part4, img2_fg_part4)
    dst_part5 = cv2.add(img_bg_part5, img2_fg_part5)

    bg[70:rows_Lu + 70, 250:cols_Lu + 250] = dst_Lu
    bg[60:rows_G_ + 60, 700:cols_G_ + 700] = dst_G_
    bg[350:rows_part1 + 350, 70:cols_part1 + 70] = dst_part1
    bg[350:rows_part2 + 350, 300:cols_part2 + 300] = dst_part2
    bg[350:rows_part3 + 350, 525:cols_part3 + 525] = dst_part3
    bg[350:rows_part4 + 350, 750:cols_part4 + 750] = dst_part4
    bg[350:rows_part5 + 350, 975:cols_part5 + 975] = dst_part5

    # cv2.imshow("result", bg)
    # c = cv2.waitKey()
    return bg, 'G' + plate


if __name__ == '__main__':

    img, plate_number = motor_plate(None)
    print(plate_number)
    cv2.imshow("result", img)
    cv2.waitKey()
