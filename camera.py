import RPi.GPIO as gp
import os
import cv2 as cv2 
import numpy as np
import time
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
adapter_info = {   "A":{   "i2c_cmd":"i2cset -y 0 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
                        "B":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
                        "C":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                        "D":{
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x07",
                                         "gpio_sta":[1,1,0],
                            },
                     } 
    
gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11,gp.OUT)
gp.setup(12,gp.OUT)
#os.system("i2cset -y 0 0x70 0x00 0x06")
#gpio_sta = [0,1,0]# gpio write
#gp.output(7, gpio_sta[0])
#gp.output(11, gpio_sta[1])
#gp.output(12, gpio_sta[2])





class VideoCamera(object):
    
    def select_channel(self):
        #channel_info = self.adapter_info.get(index)
        #if channel_info == None:
        #    print("Can't get this info")
        os.system("i2cset -y 0 0x70 0x00 0x05") # i2c write
        gpio_sta = [0,0,1] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])
        
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        width = 320
        height = 240
        self.video.set(3, width)
        self.video.set(4, height)
       
        success, image = self.video.read()
        print(success)
        self.select_channel()
        
        
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        
        #os.system("i2cset -y 0 0x70 0x00 0x05")
        #gpio_sta = [0,0,1]
        #gp.output(7, gpio_sta[0])
        #gp.output(11, gpio_sta[1])
        #gp.output(12, gpio_sta[2])
       # success, image2 = self.video.read()
       # print(success)
        #gray=cv2.cv2tColor(image,cv2.COLOR_BGR2GRAY)
        #image2=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        
        #image3 = cv2.vconcat([image,image2])
        
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
