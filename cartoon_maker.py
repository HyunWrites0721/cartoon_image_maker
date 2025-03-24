import cv2 as cv
import numpy as np

def drawText(img, text, org=(10, 25), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=0.6, color=(0, 0, 0), colorBoundary=(255, 255, 255)):
    cv.putText(img, text, org, fontFace, fontScale, colorBoundary, thickness=2)
    cv.putText(img, text, org, fontFace, fontScale, color)


def cartoonify_adaptive(img):
    # simplify color
    for _ in range(3):
        img = cv.bilateralFilter(img, 9, 15, 75)

    # edging
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.adaptiveThreshold(cv.medianBlur(gray, 3), 255, 
                                  cv.ADAPTIVE_THRESH_MEAN_C, 
                                  cv.THRESH_BINARY, 9, 9)

    #cartoon make
    cartoon = cv.bitwise_and(img, img, mask=edges)
    return cartoon

def cartoonify_canny(img):
    # simplify color
    for _ in range(2):
        img = cv.bilateralFilter(img, 9, 15, 75)

    # edging
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 100, 200)
    edges = cv.bitwise_not(edges)

    #cartoon make
    cartoon = cv.bitwise_and(img, img, mask=edges)
    return cartoon

img_list = ['ace.jpg', 'luffy.jpg', 'whitebeard.jpg', 'calmdownman.jpg', 'chimpearl.jpg', 'beautifulgirl.jpg']
img_index = 0

while True:
    img = cv.imread(img_list[img_index])
    cartoon_img_adaptive = cartoonify_adaptive(img)
    cartoon_img_canny = cartoonify_canny(img)
    drawText(img, "img original")
    drawText(cartoon_img_adaptive, "cartoon_adaptive")
    drawText(cartoon_img_canny, "cartoon_Canny")
    
    merge = np.hstack([img, cartoon_img_adaptive, cartoon_img_canny])

    cv.imshow("IMG | Cartoon - adaptive thresholding | Cartoon - Canny edging", merge)
    key = cv.waitKey()
    if key == 27:
        break
    elif key == ord('+') or ord('='):
        img_index = (img_index + 1) % len(img_list)
    elif key == ord('-') or ord('_'):
        img_index = (img_index -1) % len(img_list)
    
cv.destroyAllWindows()