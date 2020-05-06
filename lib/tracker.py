#!/usr/bin/python
#coding:utf-8

import cv2
import numpy as np
import matplotlib.pyplot as plt

class Tracker:
    def __init__(self,j):
        print("init")
        self.jnlf = j
        self.cap = cv2.VideoCapture(0)
        #wi = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #hi = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #fp = self.cap.get(cv2.CAP_PROP_FPS)
        #print('width,hight,fps: ',wi,hi,fp) #640.0 480.0 30.0
        self.cap.set(3,640) #幅
        self.cap.set(4,480) #高さ
        self.cap.set(5,5) #fps

        #最初の物体検知用枠(正方形)を配置
        # 座標原点は左上
        # x = (640-width)/2 枠が左右中心に位置
        # 480-y-hight = bottom やや上側に配置
        x,y,w,h = 245,200,150,150
        self.window = (x,y,w,h) #タプルリテラル/数値配列そのものに意味

        #画像取得+回転
        rtn,frame = self.cap.read()
        frame = cv2.rotate(frame,cv2.ROTATE_180)
        #2次元配列の切り取り/numpyにおけるスライス/roi: Region of Interest
        roi = frame[y:y+h,x:x+w] 
        cv2.imwrite(self.jnl('01_frame'),frame)
        cv2.imwrite(self.jnl('02_roi'),roi)

        #HSVに変換/Hue(色相) Saturation(彩度) Value(明度)
        hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        cv2.imwrite(self.jnl('03_hsv_roi'),hsv_roi)
        #フィルタの作成/彩度59以下明度31以下を無視
        # inRangeで下限・上限で指定して2値化
        img_mask = cv2.inRange(hsv_roi,np.array((0.,60.,32.)),np.array((180.,255.,255.)))
        cv2.imwrite(self.jnl('04_img_mask'),img_mask)

        #色相のヒストグラムを作成
        # 作成したマスクにより色味がない・暗い領域を計算除外
        self.roi_hist = cv2.calcHist([hsv_roi],[0],img_mask,[180],[0,180])
        plt.plot(self.roi_hist)
        plt.savefig(self.jnl('05_roi_hist'))
        #255段階に正規化(一尺度化)
        cv2.normalize(self.roi_hist,self.roi_hist,0,255,cv2.NORM_MINMAX)
        plt.plot(self.roi_hist)
        plt.savefig(self.jnl('06_roi_hist_normalized'))

        #meanshiftの繰返し終了条件タプル
        # 反復が規定回数になるか要求精度を満たす場合に終了
        # 繰返し回数, 精度の順に指定
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)

    def track(self,func):
        try:
            print("start")
            while(True):
                rtn,frame = self.cap.read()
                frame = cv2.rotate(frame,cv2.ROTATE_180)
                if rtn == True:
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                    bp = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180], 1)
                    ret,self.window = cv2.meanShift(bp,self.window,self.term_crit)
                    x,y,w,h = self.window
                    cenx = int(x+w/2)
                    angle = (cenx-320)/320*100
                    print(str(cenx)+":"+str(int(angle)))
                    func(angle)

        except Exception as e:
            print(e)
        finally:
            self.finish()

    def meanShift(self):
        try:
            print("start")
            while(True):
                #画面取得
                rtn,frame = self.cap.read()
                frame = cv2.rotate(frame,cv2.ROTATE_180)
                if rtn == True:
                    #色相の特徴量(ヒストグラムの比)を逆投影
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                    bp = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180], 1)
                    #meanshift/特徴量が多い部分へ枠を移動
                    ret,self.window = cv2.meanShift(bp,self.window,self.term_crit)
                    #物体検出した枠と中心を描画
                    x,y,w,h = self.window
                    frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
                    cenx = int(x+w/2)
                    ceny = int(y+h/2)
                    cv2.circle(frame,(cenx,ceny),10,(0,180,0),-1)
                    #表示
                    cv2.imshow('bp',bp)
                    cv2.imshow('meanshift',frame)
                    #cv2.imwrite(self.jnl('d'+str(cnt)),img_dst)

                    key = cv2.waitKey(1)
                    if key == 27: break #ESC

        except Exception as e:
            print(e)
        finally:
            self.finish()
    
    def camShift(self):
        try:
            print("start")
            while(True):
                rtn,frame = self.cap.read()
                frame = cv2.rotate(frame,cv2.ROTATE_180)
                if rtn == True:
                    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                    bp = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180], 1)
                    ret,self.window = cv2.CamShift(bp,self.window,self.term_crit)
                    pts = cv2.boxPoints(ret)
                    pts = np.int0(pts)
                    frame = cv2.polylines(frame,[pts],True, 255,2)
                    cv2.imshow('bp',bp)
                    cv2.imshow('camshift',frame)
                    key = cv2.waitKey(1)
                    if key == 27: break #ESC

        except Exception as e:
            print(e)
        finally:
            self.finish()
    
    def finish(self):
        print('finish')
        self.cap.release()
        cv2.destroyAllWindows()

    def jnl(self,a):
        return self.jnlf+'/'+a+'.png'


# debug 
if __name__ == '__main__':
    import sys
    args = sys.argv
    if not len(args) == 2: quit()
    tr = Tracker(args[1])
    
    tr.meanShift()
    
    #def p(angle):
    #    print(angle)
    #tr.track(p)


