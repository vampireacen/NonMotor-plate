import cv2
import numpy as np

def nonmotor_plate(number: str, plate_type='Green'):
    bg_img = ''
    wei_img = ''
    fang_img = ''
    code_img = ''
    number_suffix = ''
    if plate_type in ['White', 'white']:
        bg_img = '_w_.png'
        wei_img = '_wei_.png'
        fang_img = '_fang_.png'
        code_img = 'code_.png'
        number_suffix = '_.jpg'
    elif plate_type in ['Green', 'green']:
        bg_img = '_g_.png'
        wei_img = 'wei_.png'
        fang_img = 'fang_.png'
        code_img = 'code.png'
        number_suffix = '__.png'
    if bg_img != '':
        plate = np.random.randint(0, 10, 7)
        if number is not None:
            plate = list(number)
    bg = cv2.imread('model_plate/' + bg_img)
    wei = cv2.imread('model_plate/' + wei_img)
    fang = cv2.imread('model_plate/' + fang_img)
    code = cv2.imread('model_plate/' + code_img)
    number_0 = cv2.imread('model_plate/_' + str(plate[0]) + number_suffix)
    number_1 = cv2.imread('model_plate/_' + str(plate[1]) + number_suffix)
    number_2 = cv2.imread('model_plate/_' + str(plate[2]) + number_suffix)
    number_3 = cv2.imread('model_plate/_' + str(plate[3]) + number_suffix)
    number_4 = cv2.imread('model_plate/_' + str(plate[4]) + number_suffix)
    number_5 = cv2.imread('model_plate/_' + str(plate[5]) + number_suffix)
    number_6 = cv2.imread('model_plate/_' + str(plate[6]) + number_suffix)

    wei = cv2.resize(wei, (175, 175))
    fang = cv2.resize(fang, (175, 175))
    code = cv2.resize(code, (110, 110))
    number_0 = cv2.resize(number_0, (100, 200))
    number_1 = cv2.resize(number_1, (100, 200))
    number_2 = cv2.resize(number_2, (100, 200))
    number_3 = cv2.resize(number_3, (100, 200))
    number_4 = cv2.resize(number_4, (100, 200))
    number_5 = cv2.resize(number_5, (100, 200))
    number_6 = cv2.resize(number_6, (100, 200))

    # I want to put logo on top-left corner, So I create a ROI
    rows_wei, cols_wei, channels_wei = wei.shape
    rows_fang, cols_fang, channels_fang = fang.shape
    rows_code, cols_code, channels_code = code.shape
    rows_0, cols_0, channels_0 = number_0.shape
    rows_1, cols_1, channels_1 = number_1.shape
    rows_2, cols_2, channels_2 = number_2.shape
    rows_3, cols_3, channels_3 = number_3.shape
    rows_4, cols_4, channels_4 = number_4.shape
    rows_5, cols_5, channels_5 = number_5.shape
    rows_6, cols_6, channels_6 = number_6.shape

    roi_wei = bg[100:rows_wei + 100, 100:cols_wei + 100]
    roi_fang = bg[100:rows_fang + 100, 100:cols_fang + 100]
    roi_code = bg[100:rows_code + 100, 100:cols_code + 100]
    roi_0 = bg[300:rows_0 + 300, 100:cols_0 + 100]
    roi_1 = bg[300:rows_1 + 300, 250:cols_1 + 250]
    roi_2 = bg[300:rows_2 + 300, 400:cols_2 + 400]
    roi_3 = bg[300:rows_3 + 300, 550:cols_3 + 550]
    roi_4 = bg[300:rows_4 + 300, 700:cols_4 + 700]
    roi_5 = bg[300:rows_5 + 300, 850:cols_5 + 850]
    roi_6 = bg[300:rows_6 + 300, 950:cols_6 + 950]

    # Now create a mask of logo and create its inverse mask also
    img2gray_wei = cv2.cvtColor(wei, cv2.COLOR_BGR2GRAY)
    ret_wei, mask_wei = cv2.threshold(img2gray_wei, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_wei = cv2.bitwise_not(mask_wei)

    img2gray_fang = cv2.cvtColor(fang, cv2.COLOR_BGR2GRAY)
    ret_fang, mask_fang = cv2.threshold(img2gray_fang, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_fang = cv2.bitwise_not(mask_fang)

    img2gray_code = cv2.cvtColor(code, cv2.COLOR_BGR2GRAY)
    ret_code, mask_code = cv2.threshold(img2gray_code, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_code = cv2.bitwise_not(mask_code)

    img2gray_0 = cv2.cvtColor(number_0, cv2.COLOR_BGR2GRAY)
    ret_0, mask_0 = cv2.threshold(img2gray_0, 200, 0, cv2.THRESH_BINARY)  # 200 255
    mask_inv_0 = cv2.bitwise_not(mask_0)

    img2gray_1 = cv2.cvtColor(number_1, cv2.COLOR_BGR2GRAY)
    ret_1, mask_1 = cv2.threshold(img2gray_1, 200, 0, cv2.THRESH_BINARY)
    mask_inv_1 = cv2.bitwise_not(mask_1)

    img2gray_2 = cv2.cvtColor(number_2, cv2.COLOR_BGR2GRAY)
    ret_2, mask_2 = cv2.threshold(img2gray_2, 200, 0, cv2.THRESH_BINARY)
    mask_inv_2 = cv2.bitwise_not(mask_2)

    img2gray_3 = cv2.cvtColor(number_3, cv2.COLOR_BGR2GRAY)
    ret_3, mask_3 = cv2.threshold(img2gray_3, 200, 0, cv2.THRESH_BINARY)
    mask_inv_3 = cv2.bitwise_not(mask_3)

    img2gray_4 = cv2.cvtColor(number_4, cv2.COLOR_BGR2GRAY)
    ret_4, mask_4 = cv2.threshold(img2gray_4, 200, 0, cv2.THRESH_BINARY)
    mask_inv_4 = cv2.bitwise_not(mask_4)

    img2gray_5 = cv2.cvtColor(number_5, cv2.COLOR_BGR2GRAY)
    ret_5, mask_5 = cv2.threshold(img2gray_5, 200, 0, cv2.THRESH_BINARY)
    mask_inv_5 = cv2.bitwise_not(mask_5)

    img2gray_6 = cv2.cvtColor(number_6, cv2.COLOR_BGR2GRAY)
    ret_6, mask_6 = cv2.threshold(img2gray_6, 200, 0, cv2.THRESH_BINARY)
    mask_inv_6 = cv2.bitwise_not(mask_6)
    # Now black-out the area of logo in ROI
    img_bg_wei = cv2.bitwise_and(roi_wei, roi_wei, mask=mask_wei)
    img_bg_fang = cv2.bitwise_and(roi_fang, roi_fang, mask=mask_fang)
    img_bg_code = cv2.bitwise_and(roi_code, roi_code, mask=mask_code)
    img_bg_0 = cv2.bitwise_and(roi_0, roi_0, mask=mask_0)
    img_bg_1 = cv2.bitwise_and(roi_1, roi_1, mask=mask_1)
    img_bg_2 = cv2.bitwise_and(roi_2, roi_2, mask=mask_2)
    img_bg_3 = cv2.bitwise_and(roi_3, roi_3, mask=mask_3)
    img_bg_4 = cv2.bitwise_and(roi_4, roi_4, mask=mask_4)
    img_bg_5 = cv2.bitwise_and(roi_5, roi_5, mask=mask_5)
    img_bg_6 = cv2.bitwise_and(roi_6, roi_6, mask=mask_6)

    # Take only region of logo from logo image.
    img2_fg_wei = cv2.bitwise_and(wei, wei, mask=mask_inv_wei)
    img2_fg_fang = cv2.bitwise_and(fang, fang, mask=mask_inv_fang)
    img2_fg_code = cv2.bitwise_and(code, code, mask=mask_inv_code)
    img2_fg_0 = cv2.bitwise_and(number_0, number_0, mask=mask_inv_0)
    img2_fg_1 = cv2.bitwise_and(number_1, number_1, mask=mask_inv_1)
    img2_fg_2 = cv2.bitwise_and(number_2, number_2, mask=mask_inv_2)
    img2_fg_3 = cv2.bitwise_and(number_3, number_3, mask=mask_inv_3)
    img2_fg_4 = cv2.bitwise_and(number_4, number_4, mask=mask_inv_4)
    img2_fg_5 = cv2.bitwise_and(number_5, number_5, mask=mask_inv_5)
    img2_fg_6 = cv2.bitwise_and(number_6, number_6, mask=mask_inv_6)

    # Put logo in ROI and modify the main image
    dst_wei = cv2.add(img_bg_wei, img2_fg_wei)
    dst_fang = cv2.add(img_bg_fang, img2_fg_fang)
    dst_code = cv2.add(img_bg_code, img2_fg_code)
    dst_0 = cv2.add(img_bg_0, img2_fg_0)
    dst_1 = cv2.add(img_bg_1, img2_fg_1)
    dst_2 = cv2.add(img_bg_2, img2_fg_2)
    dst_3 = cv2.add(img_bg_3, img2_fg_3)
    dst_4 = cv2.add(img_bg_4, img2_fg_4)
    dst_5 = cv2.add(img_bg_5, img2_fg_5)
    dst_6 = cv2.add(img_bg_6, img2_fg_6)

    bg[110:rows_wei + 110, 340:cols_wei + 340] = dst_wei
    bg[110:rows_fang + 110, 697:cols_fang + 697] = dst_fang
    bg[150:rows_code + 150, 547:cols_code + 547] = dst_code
    bg[310:rows_0 + 310, 102:cols_0 + 102] = dst_0
    bg[310:rows_1 + 310, 252:cols_1 + 252] = dst_1
    bg[310:rows_2 + 310, 402:cols_2 + 402] = dst_2
    bg[310:rows_3 + 310, 552:cols_3 + 552] = dst_3
    bg[310:rows_4 + 310, 702:cols_4 + 702] = dst_4
    bg[310:rows_5 + 310, 852:cols_5 + 852] = dst_5
    bg[310:rows_6 + 310, 1002:cols_6 + 1002] = dst_6

    plate_ = [str(i) for i in plate]
    return bg, ''.join(plate_)


if __name__ == '__main__':
    img, plate_number = nonmotor_plate(None)
    print(plate_number)
    cv2.imshow("result", img)
    cv2.waitKey()
