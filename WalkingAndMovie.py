#!/usr/bin/env python
#-*- cording: utf-8 -*-
import time
import cv2
import sys

g_width = 320;
g_height = 240;

#カメラのサイズを適宜変更して処理速度を調整
g_width2 = 100;
g_height2 = 100;

out_img = cv2.imread("white.jpg");
out_img = cv2.resize(out_img, (g_width2, g_height2))


timeStart = 0
timeEnd = 0
spanTime = 0

args = sys.argv

print(len(sys.argv))

if len(args) < 3:
 exit()

#diffFolder = args[1];
#動きに合わせて再生する動画のファイルパス
MovieFilePath = args[1];
#差分判定率
DiffJudgePercent = float(args[2])

# VideoCapture オブジェクトを取得します
g_capture = cv2.VideoCapture(0)

print(g_capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width2))
print(g_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height2)) 

out_img = cv2.imread("white.jpg")

global firstPoseFlg
firstPoseFlg = True;

MoviePlayFlg = True

def Play():

    global g_capture
    global g_width
    global g_height

    global diffFolder
    global diffEdgeFolder
    global poseFlowFilePath
    global MusicFilePath
    global out_img
    global MoviePlayFlg
    global DiffJudgePercent
    
    global MatchCount
    
    timeStart = 0.0
    timeEnd = 0.0
    spanTime = 0.0
    timeSpan = 0.1;


    cap2 = cv2.VideoCapture(MovieFilePath)        
    while(cap2.isOpened()):
        ret, frame = g_capture.read()
        img1 = frame;
        
        
        str1 = cv2.waitKey(1)
        
        cv2.imshow('frame', frame)

        if MoviePlayFlg == True:
            ret2, frame2 = cap2.read()
            frame3 = cv2.resize(frame2,(g_width, g_height))
            
            cv2.imshow('frame3', frame3)
        
        if str1 == ord("q"):
            break
            
        currentTime = time.time()
        if timeStart == 0:
            timeStart = time.time()
            timeEnd = time.time()
            
            ret2, frame2 = cap2.read()

            frame3 = cv2.resize(frame2,(g_width, g_height))
            
            cv2.imshow('frame3', frame3)
            
        else:
            timeEnd = time.time()
            
        timeDiff = timeEnd - timeStart
        
        if(timeDiff >= timeSpan):
            img3 = Diff(img1, img2)
            WRate = calcWhiteRate(img3)
            #print(WRate)
            if WRate >= DiffJudgePercent:
                MoviePlayFlg = True
            else:
                MoviePlayFlg = False


            
            timeStart = currentTime
       
        img2 = img1

    
    cap2.release()
    g_capture.release()

    cv2.destroyAllWindows()

def calcWhiteRate(img1):

    global g_width2
    global g_height2
    
    WCount = 0
    
    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
             
             if ( img1[y, x, 0] == 255 and
                  img1[y, x, 1] == 255 and
                  img1[y, x, 2] == 255 ) :
                    WCount = WCount+1
    
    WRate = WCount / (g_width2 * g_height2)
    WRate = WRate * 100.0
    
    return WRate
    
def Saiten(poseName):
    global diffFolder
    global g_capture
    global haikei_img
    global MatchCount
    
    poseFileName = diffFolder + "\\" + poseName + ".jpg"
    pose_img = cv2.imread(poseFileName);
    
    ret, frame = g_capture.read()
    ret_img = Diff(haikei_img, frame)
    #cv2.imshow('ret1', ret_img)
    cv2.waitKey(1)
    
    sameRate1 = calcOverlapRate(ret_img, pose_img)
    
    str2 = "一致率:" + str(sameRate1) + "%";
    print(str2)
    
    if sameRate1 >= 45.0:
        MatchCount = MatchCount + 1

    return 0

def Diff(img1, img2):
    
    global g_width
    global g_height
    global out_img

    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
            if img1[y, x, 0] >= img2[y, x, 0]:
                out_img[y, x, 0] = abs(img1[y, x, 0] - img2[y, x, 0]);
            else:
                out_img[y, x, 0] = abs(img2[y, x, 0] - img1[y, x, 0]);

            if img1[y, x, 1] >= img2[y, x, 1]:
                out_img[y, x, 1] = abs(img1[y, x, 1] - img2[y, x, 1]);
            else:
                out_img[y, x, 1] = abs(img2[y, x, 1] - img1[y, x, 1]);

            if img1[y, x, 2] >= img2[y, x, 2]:
                out_img[y, x, 2] = abs(img1[y, x, 2] - img2[y, x, 2]);
            else:
                out_img[y, x, 2] = abs(img2[y, x, 2] - img1[y, x, 2]);

            absSum = int(out_img[y, x, 0]) + int(out_img[y, x, 1]) + int(out_img[y, x, 2])
            if absSum >= 120:
                    out_img[y, x, 0] = 255
                    out_img[y, x, 1] = 255
                    out_img[y, x, 2] = 255
            else:
                    out_img[y, x, 0] = 0
                    out_img[y, x, 1] = 0
                    out_img[y, x, 2] = 0
                    
    return out_img


def main(): 

    Play()


    return 0
   

    
        
main()
