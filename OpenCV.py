import cv2

def set_cap():
    cap = cv2.VideoCapture(0)
    #擷取畫面 寬度 設定為512
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    #擷取畫面 高度 設定為512
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

def read_cap(cap):
    ret,image_src =cap.read()
    image=cv2.resize(image_src,(224,224))
    return image

def close_cap(cap):
    cap.release()

