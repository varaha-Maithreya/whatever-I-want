import RPi.GPIO as gp
import os
import cv2 as cv2 
import numpy as np
import time
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
    
#os.system("i2cset -y 0 0x70 0x00 0x06")
#gpio_sta = [0,1,0]# gpio write
#gp.output(7, gpio_sta[0])
#gp.output(11, gpio_sta[1])
#gp.output(12, gpio_sta[2])





class VideoCamera(object):
    
    camNum = 2
    adapter_info = [{   "i2c_cmd":"i2cset -y 0 0x70 0x00 0x04",
                                    "gpio_sta":[0,0,1],
                            },
                        {
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x05",
                                "gpio_sta":[1,0,1],
                            },
                        {
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x06",
                                "gpio_sta":[0,1,0],
                            },
                        {
                                "i2c_cmd":"i2cset -y 0 0x70 0x00 0x07",
                                "gpio_sta":[1,1,0],
                            }]
    width = 320
    height = 240 

    def choose_channel(self,index):
        channel_info = self.adapter_info[index]
        if channel_info == None:
            print("Can't get this info")
        os.system(channel_info["i2c_cmd"]) # i2c write
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])
    def select_channel(self,index):
        channel_info = self.adapter_info[index]
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])

    def __init__(self):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11,gp.OUT)
        gp.setup(12,gp.OUT)
        
        self.camera = cv2.VideoCapture(0)

        for i in range(self.camNum):
            self.choose_channel(i) 
            self.camera.set(3, self.width)
            self.camera.set(4, self.height)
            ret, frame = self.camera.read()
            print(f"Testing Camera {chr(65+i)}")
           
            if ret == True:
                print("camera %s init OK" %(chr(65+i)))
                pname = "image_"+ chr(65+i)+".jpg"
                time.sleep(1)
            else:
                print(f"camera {chr(65+i)} not OK")
            
    
    def __del__(self):
        self.camera.release()
        
    def get_frame(self):
        
        factor  = 0
        black = np.zeros((self.height, self.width*4, 3), dtype= np.uint8) 
        for i in range(self.camNum):
            self.select_channel(i)
            test = False
            ret, frame = None, None
            while (not test):
                ret, frame = self.camera.read()
                ret, frame = self.camera.read()
                #ret, frame = self.camera.read()
                ret, frame = self.camera.read()
                if (ret): test = True
                else: print("Uh Oh")
            frame.dtype=np.uint8
            if i == 3:
                black[factor:factor+self.height, 0:self.width, :] = frame
            elif i == 2:
                black[factor:factor+self.height, self.width:self.width*2,:] = frame
            elif i == 1:
                black[factor:factor+self.height, self.width*2:self.width*3,:] = frame
            elif i == 0:
                black[factor:factor+self.height, self.width*3:self.width*4,:] = frame
                
        ret, jpeg = cv2.imencode('.jpg', black)
        return jpeg.tobytes()
#     
#     def get_frame(self):
#         width = 320
#         height = 240
#         self.video.set(3, width)
#         self.video.set(4, height)
#        
#         success, image = self.video.read()
#         print(success)
#         self.select_channel()
#         
#         
#         image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
#         
#         #os.system("i2cset -y 0 0x70 0x00 0x05")
#         #gpio_sta = [0,0,1]
#         #gp.output(7, gpio_sta[0])
#         #gp.output(11, gpio_sta[1])
#         #gp.output(12, gpio_sta[2])
#        # success, image2 = self.video.read()
#        # print(success)
#         #gray=cv2.cv2tColor(image,cv2.COLOR_BGR2GRAY)
#         #image2=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
#         
#         #image3 = cv2.vconcat([image,image2])
#         
#         
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
# 
# 