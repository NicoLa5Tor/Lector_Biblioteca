import cv2

cap = cv2.VideoCapture(0)
print("pasa al while")
while True:
    ret,frame = cap.read()
    if ret is False:
        break
    cv2.imshow('cam',frame)

    if cv2.waitKey(1) == 27:
        break