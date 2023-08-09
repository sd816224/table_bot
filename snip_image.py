import cv2
import numpy as np
import os


def snip(file_path,image_name):


    def click_event(event, x, y, flags, param):
        global img
        global img_backup
        global start_point
        global end_point
        global crop_img
        global crop_status

        # def resize(img,window):
        #     cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        #     img = cv2.resize(img, (960, 540))

        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, ',', y)
            start_point = (x, y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # strXY=str(x)+','+str(y)
            strXY = '1'
            cv2.putText(img, strXY, (x, y), font, 1, (255, 255, 0), 2)
            cv2.imshow('image', img)

        if event == cv2.EVENT_LBUTTONUP:
            print(x, ',', y)
            end_point = (x, y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # strXY=str(x)+','+str(y)
            strXY = '2'
            cv2.putText(img, strXY, (x, y), font, 1, (255, 255, 0), 2)
            crop_img =img[start_point[1]:end_point[1],start_point[0]:end_point[0]]
            cv2.rectangle(img, start_point, end_point, (255, 255, 0), 2)
            crop_status = True
            cv2.imshow('cropped', crop_img)

        if event == cv2.EVENT_RBUTTONDOWN:
            img = img_backup.copy()
            cv2.imshow('image', img)
            cv2.destroyWindow('cropped')
            crop_status = False

    global img
    global img_backup
    global crop_img
    global crop_status

    image_abs_path=os.path.join(file_path,image_name)
    img=cv2.imread(image_abs_path)
    img_backup=img.copy()
    crop_status=False

    while True:
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow('image',img)
        cv2.setMouseCallback('image',click_event)
        k=cv2.waitKey(0)
        if k == ord('k') & 0xFF:
            snipped_image_name='cropped_'+image_name
            if crop_status:
                cv2.imwrite(os.path.join(file_path,snipped_image_name),crop_img)
                crop_status=False
            cv2.destroyAllWindows()
            break

# debug
# file_path=r'C:\Users\ufocz\myland\accounting2\files'
# image_name=r'table.jpg'
# snip(file_path,image_name)