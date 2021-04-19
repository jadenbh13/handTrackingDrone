import argparse
import cv2
from gestDet import getGest
from time import sleep
from yolo import YOLO

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--network', default="normal", help='Network Type: normal / tiny / prn / v4-tiny')
ap.add_argument('-d', '--device', default=0, help='Device to use')
ap.add_argument('-s', '--size', default=416, help='Size for yolo')
ap.add_argument('-c', '--confidence', default=0.2, help='Confidence for yolo')
ap.add_argument('-nh', '--hands', default=-1, help='Total number of hands to be detected per frame (-1 for all)')
args = ap.parse_args()

if args.network == "normal":
    print("loading yolo...")
    yolo = YOLO("models/cross-hands.cfg", "models/cross-hands.weights", ["hand"])
elif args.network == "prn":
    print("loading yolo-tiny-prn...")
    yolo = YOLO("models/cross-hands-tiny-prn.cfg", "models/cross-hands-tiny-prn.weights", ["hand"])
elif args.network == "v4-tiny":
    print("loading yolov4-tiny-prn...")
    yolo = YOLO("models/cross-hands-yolov4-tiny.cfg", "models/cross-hands-yolov4-tiny.weights", ["hand"])
else:
    print("loading yolo-tiny...")
    yolo = YOLO("models/cross-hands-tiny.cfg", "models/cross-hands-tiny.weights", ["hand"])

yolo.size = int(args.size)
yolo.confidence = float(args.confidence)

print("starting webcam...")
cv2.namedWindow("preview")
"""vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False"""

file1="yDirection.txt"
file2="xDirection.txt"
file3="faceDetect.txt"
file4="name.txt"
file5="dist.txt"

with open(file3, 'w') as filetowrite:
    filetowrite.write("Not detected")

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
colour = (255, 0, 0)
thickness = 2
frame = cv2.imread("pic.png")
while True:
    try:
        frame = cv2.imread("pic.png")
        width, height, inference_time, results = yolo.inference(frame)

        cv2.putText(frame, f'{round(1/inference_time,2)} FPS', (15,15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,255), 2)

        results.sort(key=lambda x: x[2])
        wm = width / 2
        hm = height / 2
        wUp = int(wm + 45)
        wDown = int(wm - 45)
        hUp = int(hm + 45)
        hDown = int(hm - 45)

        hand_count = len(results)
        if args.hands != -1:
            hand_count = int(args.hands)

        if len(results[:hand_count]) == 0:
            with open(file3, 'w') as filetowrite:
                filetowrite.write("Not detected")
        else:
            with open(file3, 'w') as filetowrite:
                filetowrite.write("Detected")

        for detection in results[:hand_count]:
            id, name, confidence, x, y, w, h = detection
            cx = int(x + (w / 2))
            cy = int(y + (h / 2))
            disUp = 9000
            disDown = 6000
            area = w * h
            print("Area is: " + str(int(area)))
            print(cx)
            print(cy)
            if cx < wDown:
                print("Left")
                with open(file2, 'w') as filetowrite:
                    filetowrite.write("Left")
            elif cx > wUp:
                print("Right")
                with open(file2, 'w') as filetowrite:
                    filetowrite.write("Right")
            else:
                print("X stable")
                with open(file2, 'w') as filetowrite:
                    filetowrite.write("Stop")

            if int(area) < disDown:
                print("Forward")
                with open(file5, 'w') as filetowrite:
                    filetowrite.write("Forward")
            elif int(area) > disUp:
                print("Back")
                with open(file5, 'w') as filetowrite:
                    filetowrite.write("Back")
            else:
                print("Z stable")
                with open(file5, 'w') as filetowrite:
                    filetowrite.write("Stop")

            if cy < hDown:
                print("Up")
                with open(file1, 'w') as filetowrite:
                    filetowrite.write("Up")
            elif cy > hUp:
                print("Down")
                with open(file1, 'w') as filetowrite:
                    filetowrite.write("Down")
            else:
                print("Y stable")
                with open(file1, 'w') as filetowrite:
                    filetowrite.write("Stop")

            try:
                crop_img = frame[y:y+h, x:x+w]
                predic = getGest(crop_img)
                pred = predic[0]
                sc = predic[1]
                print(pred)
                print(sc)
                if 'Fist' not in pred:
                    print("   ")
                    print("   ")
                    print("Take photo")
                    print("   ")
                    print("   ")
                    with open(file3, 'w') as filetowrite:
                        filetowrite.write("Not detected")
                    sleep(3)
                    vb = cv2.imread("pic.png")
                    cv2.imwrite("phot.jpg", vb)
                    sho = cv2.imread("phot.jpg")
                    print("Taken")
                #cv2.imshow("Cropped", crop_img)
            except Exception as e:
                print(e)

            color = (0, 255, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.circle(frame,(cx,cy), 10, (0,0,255), 10)
            cv2.putText(frame, str(int(area)), (cx, cy), font,
                       fontScale, colour, thickness, cv2.LINE_AA)
            text = "%s (%s)" % (name, round(confidence, 2))
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 2)
        cv2.circle(frame,(wUp,hUp), 10, (0,0,0), 10)
        cv2.circle(frame,(wDown,hDown), 10, (255,255,255), 10)
        cv2.imshow("preview", frame)

        frame = cv2.imread("pic.png")

        key = cv2.waitKey(20)
        if key == 27:
            break
    except Exception as e:
        print(e)
        key = cv2.waitKey(20)
        if key == 27:
            with open(file3, 'w') as filetowrite:
                filetowrite.write("Not detected")
            break
with open(file3, 'w') as filetowrite:
    filetowrite.write("Not detected")
cv2.destroyAllWindows()
#vc.release()
