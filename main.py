from tkinter import messagebox as m
from tkinter import *
import argparse
import datetime as dt
from datetime import datetime
import time
import tkinter as tk
import cv2
from PIL import Image
#from PIL import ImageTk
import PIL.Image, PIL.ImageTk
import PIL.Image, PIL.ImageTk
import PIL
import numpy as np
from pypylon import pylon
from Filter import Filter
import matplotlib.pyplot as plt
from Database import Database
import random
import os
import json
import numpy as np


class App:
    def __init__(self, window, window_title,lang_status,main_icon_dir):
        
        self.lang_status = lang_status
        
        self.window = window
        self.db = Database() 
        

        if self.lang_status == "tr":
            self.lang =self.read_lang('TR')
            #self.lang = lang_tr

        elif self.lang_status =="en":
            self.lang =self.read_lang('EN')

        elif self.lang_status == "de":
            self.lang =self.read_lang('DE')


        self.vid = VideoCapture(self.lang)
        
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (self.w, self.h))
        #self.window.bind("<Configure>", YenidenBoyutlandir)
        self.window.title(window_title)
        self.window.title(self.lang[20])
        print(main_icon_dir)
        self.icon = PhotoImage(file = main_icon_dir)
        self.window.iconphoto(False, self.icon)
        
        self.db.connect()
        #self.video_source = video_source
        self.ok=False
        self.SaveResults = 0;
        #timer
        #self.timer=ElapsedTimeClock(self.window)
        lblfInstantCameraScreen=tk.LabelFrame(self.window,text=self.lang[0],padx=0,pady=0) 
        #lblfInstantCameraScreen=tk.LabelFrame(self.window,text="",padx=0,pady=0) 
        lblfInstantCameraScreen.pack(fill='both',side = TOP,padx=2)
        lblfResult=tk.LabelFrame(self.window,text=self.lang[1],padx=0,pady=0) 
        lblfResult.pack(fill='both',side = TOP,padx=5) 
        lblfOperation = tk.LabelFrame(self.window,text=self.lang[2],padx=0,pady=0) 
        lblfOperation.pack(fill='both',side = TOP,padx=5)
        lblfStatus = LabelFrame(window,text=self.lang[3],padx=0,pady=0)
        lblfStatus.pack(fill="both",side = TOP,padx=5)
        self.lblIslemDurum = tk.Label(lblfStatus,text=self.lang[3]+':',anchor=W)
        self.lblIslemDurum.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='W')   
        self.lblMessage = tk.Label(lblfStatus,text=self.lang[4]+':',anchor=W)
        self.lblMessage.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='W')   

        #lblDeneyeAdi = tk.Label(lblfInstantCameraScreen,text="Deney Adı Girin")
        #lblDeneyeAdi.grid(row=0,column=0,padx=10,pady=10)
        # open video source (by default this will try to open the computer webcam)


        # Create a canvas that can fit the above video source size
        self.canvas_InstantCamera=tk.Canvas(lblfInstantCameraScreen, width = self.vid.width, height = self.vid.height,borderwidth=1)
        #self.canvas_InstantCamera = tk.Canvas(lblfInstantCameraScreen, width = 60, height = 60)
        self.canvas_InstantCamera.grid(row=0,column=0,padx=5,pady=2)
        
        self.canvas_TileImage = tk.Canvas(lblfResult,bd=1, highlightthickness=0, relief='ridge',width=377,height=332)
        self.canvas_TileImage.grid(row=0,column=0,padx=10,pady=10)
        self.canvas_ResultImage = tk.Canvas(lblfResult,bd=1, highlightthickness=0, relief='ridge',width=377,height=332)
        self.canvas_ResultImage.grid(row=0,column=1,padx=10,pady=10)

        self.title_canvas_TileImage = tk.Label(lblfResult,text=self.lang[6],anchor=N,width=20, height=1,font=("Arial", 12))
        self.title_canvas_TileImage.grid(row=1,column=0,padx=0,pady=0,sticky='N',columnspan=1)
        self.title_canvas_ResultImage = tk.Label(lblfResult,text=self.lang[7],anchor=N,width=20, height=1,font=("Arial", 12))
        self.title_canvas_ResultImage.grid(row=1,column=1,padx=0,pady=0,sticky='N',columnspan=1)        

        lblfQualityResult=tk.LabelFrame(lblfResult,padx=1,pady=2,width=60, height=20, borderwidth=0) 
        lblfQualityResult.grid(row=0,column=2,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=0) 
        self.lblQualityPercentage = tk.Label(lblfQualityResult,text=self.lang[8]+": -",anchor=NW,width=25, height=1,font=("Arial", 25))
        self.lblQualityPercentage.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        self.lblQualityClass = tk.Label(lblfQualityResult,text=self.lang[9]+': -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblQualityClass.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        
        lblfDefectList = tk.LabelFrame(lblfResult,padx=1,pady=2,width=25, height=10,borderwidth=0) 
        lblfDefectList.grid(row=0,column=3,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10) 
        self.lblDefectList = tk.Label(lblfDefectList,text=self.lang[10]+': -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblDefectList.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        self.lbdefectsList = Listbox(lblfDefectList,width=38, height=10,font=("Arial", 10))
        self.lbdefectsList.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10)
        
        lblfColorTone = tk.LabelFrame(lblfResult,padx=1,pady=2,width=25, height=10,borderwidth=0) 
        lblfColorTone.grid(row=2,column=3,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10) 
        self.lblColorTone = tk.Label(lblfQualityResult,text=self.lang[11]+': -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblColorTone.grid(row=3,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        
        self.btn_snapshot=tk.Button(lblfOperation, text=self.lang[11], command=self.snapshot)
        self.btn_snapshot.grid(row=0,column=0,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        
        self.lblExposureTime = tk.Label(lblfOperation,text=self.lang[25]+' (us)',anchor=NW,width=16, height=1,font=("Arial", 12))
        self.lblExposureTime.grid(row=0,column=1,columnspan=1,padx=0,pady=5,sticky='NW') 
        stExposureTime= StringVar(lblfOperation)
        stExposureTime.set("150")#1000-25081000
        self.entExposureTime = Spinbox(lblfOperation,from_ = 1, to = 3000,bd=1,width=5,textvariable=stExposureTime)
        self.entExposureTime.grid(row=0,column=2,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)

        self.lblGainRaw = tk.Label(lblfOperation,text=self.lang[24],anchor=NW,width=12, height=1,font=("Arial", 12))
        self.lblGainRaw.grid(row=0,column=3,columnspan=1,padx=0,pady=5,sticky='NW') 
        stGainRaw = StringVar(lblfOperation)
        stGainRaw.set("256")
        self.entGainRaw = Spinbox(lblfOperation,from_ = 256, to = 2047,bd=1,width=5,textvariable=stGainRaw)
        self.entGainRaw.grid(row=0,column=4,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)

        self.lblAcquisitionLineRate = tk.Label(lblfOperation,text=self.lang[38],anchor=NW,width=12, height=1,font=("Arial", 12))
        self.lblAcquisitionLineRate.grid(row=0,column=5,columnspan=1,padx=0,pady=5,sticky='NW') 
        stAcquisitionLineRate = StringVar(lblfOperation)
        stAcquisitionLineRate.set("1500")
        self.entAcquisitionLineRate = Spinbox(lblfOperation,from_ = 100, to = 3000,bd=1,width=8,textvariable=stAcquisitionLineRate)
        self.entAcquisitionLineRate.grid(row=0,column=6,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        
        self.lblBantImageThreshold = tk.Label(lblfOperation,text=self.lang[26],anchor=NW,width=16, height=1,font=("Arial", 12))
        self.lblBantImageThreshold.grid(row=0,column=7,columnspan=1,padx=0,pady=5,sticky='NW') 
        stBantImageThreshold= StringVar(lblfOperation)
        #stBantImageThreshold.set("30081000")
        #stBantImageThreshold.set("13000000")#1000-25081000
        stBantImageThreshold.set("25081000")
        self.entBantImageThreshold = Spinbox(lblfOperation,from_ = 10000000, to = 90081000,bd=1,width=8,textvariable=stBantImageThreshold)
        self.entBantImageThreshold.grid(row=0,column=8,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
       
        self.bntChangeSettings=tk.Button(lblfOperation, text=self.lang[27], command=self.update_settings)
        self.bntChangeSettings.grid(row=0,column=9,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        
        self.chckVar1 = tk.IntVar()
        self.chkSaveResults = tk.Checkbutton(lblfOperation, text=self.lang[37],variable=self.chckVar1, onvalue=1, offvalue=0,selectcolor="#eb3d34",width=30, height=2,command=self.save_results)
        self.chkSaveResults.grid(row=0,column=10,columnspan=1,padx=20,pady=5,sticky='NW',ipadx=5, ipady=5)
        
        #self.bntChangeLang=tk.Button(lblfOperation, text=self.lang[39], command=self.change_lang)
        #self.bntChangeLang.grid(row=0,column=11,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        
   
        #self.btn_snapshot.place(x=10,y=10)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=100
        self.update()

        self.window.mainloop()
    #def YenidenBoyutlandir(event):
    #global plt
    #print("Yeni Boyut {}x{}".format(event.width, event.height))
    #mng = plt.get_current_fig_manager()
    
    def save_results(self):
        if self.chckVar1.get() == 1:
            self.SaveResults = 1
            self.chkSaveResults.config(selectcolor="#34eb49")
        else:
            self.SaveResults = 0
            self.chkSaveResults.config(selectcolor="#eb3d34")

    def quit(self):
        print("Çıkış sağlandı")
        self.window.destroy()
        #if m.askokcancel("Çıkış", "Emin misin?"):  
        self.vid.camera.Open()
        #self.vid.Release()
        self.vid.camera.Close() 
        #self.window.destroy()
        print("Kamerayla bağlantı kesildi")

    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

    def open_camera(self):
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")



    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")

    def update_settings(self):
        try:
            ExposureTimeVal = int(self.entExposureTime.get())
            GainRawVal = int(self.entGainRaw.get())
            BandImageThreshold = int(self.entBantImageThreshold.get())
            AcquisitionLineRateVal  = int(self.entAcquisitionLineRate.get())
            self.vid.BandImageThreshold = BandImageThreshold
            self.vid.camera.ExposureTimeAbs = ExposureTimeVal
            self.vid.camera.AcquisitionLineRateAbs = AcquisitionLineRateVal
            self.vid.camera.GainRaw = GainRawVal
            print (str(self.vid.camera.ExposureTimeAbs.Value) + " "+str(self.vid.camera.GainRaw.Value)+ " "+str(self.vid.camera.AcquisitionLineRateAbs.Value))
        except  ValueError:
            self.lblMessage.config(text=self.lang[5]+":"+self.lang[28])
            self.lblMessage.config(bg="#f57f7f")

    def update(self):
        # print(self.lang_status)
        # if self.lang_status == "tr":
        #     self.lang = lang_tr
        #     self.vid.lang = lang_tr
        # else:
        #     self.lang = lang_en
        #     self.vid.lang = lang_en

        # Get a frame from the video source
        ret,frame,frame_instant = self.vid.get_frame()
        #print(frame_instant.shape)
        #frame_instant = frame_instant[:,20:frame.shape[1]-20]
        #print(frame_instant.shape)
        # if self.ok:
        #     self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        #if frame is not None:
        if ret:
            self.InstantImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_instant))
            self.canvas_InstantCamera.create_image(0, 0, image = self.InstantImage, anchor = tk.NW)
        
        tile_no = 26
        image_sum = np.sum(frame)  
        now = datetime.now()
        defect_locations = []
        defect_num = 0;
        tile_width_pixel_sum = 0
        tile_height_pixel_sum  = 0
        product_time = now.strftime("%Y-%m-%d %H:%M:%S")
        img_file_name = str(tile_no) + "_"+str(int(self.vid.camera.GainRaw.Value))+"_"+str(int(self.vid.camera.ExposureTimeAbs.Value))+"_"+str(int(self.vid.camera.AcquisitionLineRateAbs.Value))+"_"+now.strftime("%Y%m%d%H%M%S")
        print(image_sum)
        #self.lblIslemDurum.config(text='Bilgi: Kameradan görüntü alınıyor. - '+str(image_sum/89786))
        self.lblIslemDurum.config(text=self.lang[5]+':'+ self.lang[12]+'. - ')
        
        if (self.vid.BandImageThreshold)<image_sum:
            plt.close('all')
            self.lblIslemDurum.config(text=self.lang[5]+':'+self.lang[13]+'- '+str(image_sum))
            img_before_sum = np.sum(self.vid.img_before)
            
            img = frame
            print("Boyut: "+str(img.shape))
            img_original =  img[:,15:frame.shape[1]-20]
            print("Boyut: "+str(img_original.shape))
            #img_original =  img
            scale_percent = 2 # percent of original size
            filter = Filter(img,210,(3/5),scale_percent)
            J = filter.SteerableDigitalFilter()
            J2 = (J > J.mean(axis=0).max(0)).astype(np.float32)
            J3 = (J>1).astype(np.float32)
            diffI = J2-(J-J3)
            mean_ = diffI.mean() #max değeri de verilebilir
            min_ = diffI.min()
            threshold = (mean_+min_)/mean_
            #diffI_threshold = (diffI>threshold).astype(np.uint8)
            diffI_threshold = (diffI<threshold).astype(np.uint8)
            im = np.array(diffI_threshold * 255, dtype = np.uint8)
            #threshed değişkeninde kusurlu alanlar bulunacak. 
            threshed = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 10)
            threshed = cv2.subtract(255, threshed) 
            #(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
 
            height_section = img_original.shape[0]
            width_section = img_original.shape[1]
            max_color_tone = 255*width_section*height_section
            

            if img_before_sum!=0:
                #Kesit olarak alınan görüntü bantta karo varsa biriktiriliyor.
                self.vid.color_tone_differences.append(((img_original.sum()/3)*100)/max_color_tone)
                #print("Kesit Renk Ton: "+str(((img_original.sum()/3)*100)/max_color_tone))
                self.vid.vertical_original = np.concatenate((self.vid.vertical_original,img_original),axis=0)
                self.vid.vertical_filtered = np.concatenate((self.vid.vertical_filtered,threshed),axis=0)
               
                self.vid.section_image_num+=1

            else:
                self.vid.vertical_original = img_original
                self.vid.vertical_filtered = threshed
            
            self.vid.img_before = threshed
            #print("Karo görüntüsü alınıyor. "+ str(image_sum))
            
        elif np.sum(self.vid.vertical_original) !=0 or np.sum(self.vid.vertical_filtered) !=0:
                #Tam bir karoyu içeren kesit görüntüleri dosyaya yazılıyor ve arayüzde gösteriliyor.
                scale_percent = 0.2
                width = int(self.vid.vertical_original.shape[1] * scale_percent )
                height = int(self.vid.vertical_original.shape[0] * scale_percent )
                dim = (width, height)
                vertical_original_resized = cv2.resize(self.vid.vertical_original, dim, interpolation = cv2.INTER_AREA)
                vertical_filtered_resized = cv2.resize(self.vid.vertical_filtered, dim, interpolation = cv2.INTER_AREA)
                self.TileImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(vertical_original_resized))
                self.canvas_TileImage.config(width=(self.vid.vertical_original.shape[1]*scale_percent), height=(self.vid.vertical_original.shape[0]*scale_percent))
                self.lblMessage.config( text=self.lang[5]+":"+self.lang[29]+": "+str(self.vid.vertical_original.shape[1]/self.vid.vertical_original.shape[0]))
                self.canvas_TileImage.create_image(0, 0, image = self.TileImage , anchor = tk.NW)
                #self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(vertical_filtered_resized))
                #self.canvas_ResultImage.config(width=(self.vid.vertical_original.shape[1]*0.2), height=(self.vid.vertical_original.shape[0]*scale_percent))
                #self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage , anchor = tk.NW)
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+".jpg"), self.vid.vertical_original)
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_filter.jpg"), self.vid.vertical_filtered)
                print(str((self.vid.section_image_num))+" kesit alındı ve görüntü kaydedildi")
                
                #Veri Tabanı İşlemleri Yapılıyor
                if self.SaveResults == 1:
                    product_tile_id = self.db.insertProduct(1,product_time,(img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)))

                #Burada kesit işlemleri yapılıyor
                img_filter = self.vid.vertical_filtered
                resize_rate = 2
                width_img = int(self.vid.vertical_original.shape[1] / resize_rate )
                height_img = int(self.vid.vertical_original.shape[0]/ resize_rate )
                dim_img = (width_img, height_img)
                img_resized = cv2.resize(self.vid.vertical_original, dim_img, interpolation = cv2.INTER_AREA)
                height_img_filter = img_filter.shape[0]
                width_img_filter = img_filter.shape[1]
                section_no = 0
                
                tile_section_num = int(height_img_filter/self.vid.section_height)
               
                tile_image = np.empty((tile_section_num*self.vid.section_height,int(self.vid.capture_width/2),3))
                
                color_tone_differences = np.zeros((tile_section_num,1),float)

                for im in range(0,height_img_filter,self.vid.section_height):
                    section = img_filter[im:(im+self.vid.section_height),]
                    section_img = img_resized[im:(im+self.vid.section_height),]
                    height_section = section.shape[0]
                    width_section = section.shape[1]
                    #print(str(section_no+1)+". Kesit yükseklik: "+str(height_section) + " Kesit Genişlik: "+str(width_section))
                    # #max_color_tone = section_img.max()*width_section*height_section
                    max_color_tone = 255*width_section*height_section
                    color_tone_differences[int(im/self.vid.section_height),] =((section_img.sum()/3)*100)/max_color_tone;

                    horizontal_section = np.zeros((height_section,1),float)
                    vertical_section = np.zeros((width_section,1),float)

                    tileBorder = np.zeros((height_section,width_section),float)

                    for wi in range(0,width_section):
                            #print(section.sum(axis=0))
                            vertical_section[wi,]= section[:,wi].sum()

                   #Görüntü kesitinden karo kesiti ayrıştırılıyor     
                    left_vertical_max = vertical_section[0:int((width_section/2))].max()
                    #left_vertical = np.around(np.argwhere(vertical_section[0:int((width_section/2))]==left_vertical_max)).min()
                    right_vertical_max = vertical_section[(int(width_section/2)):width_section].max()

                    left_vertical = np.argwhere(vertical_section[0:int(width_section/2)]==left_vertical_max)[:,].max(axis=0)[0]
                    right_vertical = int(width_section/2)+np.argwhere(vertical_section[(int(width_section/2)):,]==right_vertical_max)[:,].max(axis=0)[0]
                    
                    print(str(section_no+1)+" .kesit left: "+str(left_vertical) + " right: "+str(right_vertical)+" right-left: "+str(right_vertical-left_vertical))
                    if section_no == 0 or section_no == (tile_section_num-1):
                        #print(str((section_no+1))+ " "+str(section.sum()))
                        for hi in range(0,height_section):
                            horizontal_section[hi,] = section[hi,].sum()
                        if section_no ==0:
                            section_name = 'ilk'
                            top_horizontal_max = horizontal_section.max()
                            top_horizontal = np.argwhere(horizontal_section==top_horizontal_max)[:,].max(axis=0)[0]
                            tile_section = section_img[top_horizontal-10:self.vid.section_height,left_vertical+10:right_vertical-10]
                    
                        if section_no == (tile_section_num-1):
                            section_name = 'son'
                            bottom_horizontal_max = horizontal_section.max()
                            bottom_horizontal = np.argwhere(horizontal_section==bottom_horizontal_max)[:,].max(axis=0)[0]
                            tile_section = section_img[1:bottom_horizontal+10,left_vertical+10:right_vertical-10]
                        #print(str(left_vertical) + " "+str(right_vertical))

                    else:
                        section_name ='orta'
                        tile_section = section_img[:,left_vertical:right_vertical]
                        # for wi in range(width_section):
                        #   print(str(section[:,wi].sum())+":"+str(section[:,wi].sum().min()))
                        #   tileBorder[:,wi] = section[:,wi].sum().min() 
                    
                    verticalSection_mmm = np.zeros((tile_section.shape[1],1),float)
                    
                   
                    if tile_section.shape[0] != 0:
                        for ti in range(tile_section.shape[1]):
                            #Burada max min yer değiştirecek. Matlabda kusur alanları beyaz olurken pythonda siyah
                            #verticalSection_mmm[ti] = tile_section[:,ti].max(axis=0)[0]-tile_section[:,ti].min(axis=0)[0]/tile_section[:,ti].mean()
                            #verticalSection_mmm[ti] = (tile_section[:,ti].min(axis=0)[0]-tile_section[:,ti].max(axis=0)[0])/tile_section[:,ti].mean()
                            #print(tile_section.shape)
                            verticalSection_mmm[ti] = (tile_section[:,ti].max(axis=0)[0]-tile_section[:,ti].min(axis=0)[0])/tile_section[:,ti].mean()

                    if section_no !=0 and section_no !=(tile_section_num-1):
                        start_vs = 25
                        end_vs = verticalSection_mmm.shape[0]-25
                        #print("vertical_section_mmm-w: "+str(verticalSection_mmm.shape[0]))
                        window_size_vs = int(round((verticalSection_mmm.shape[0]/60),0))
                        defect_t_val  = 0.23; #0.22 orjinal
                        print("Pencere Boyutu:"+str(window_size_vs))
                        for vsi in range(start_vs,end_vs,window_size_vs):
                            #Burada contrast hesaplanıp ona göre işlem yapılabilir.
                            contrast = (verticalSection_mmm[vsi:(vsi+window_size_vs)].max()-verticalSection_mmm[vsi:(vsi+window_size_vs)].min())
                            contrast /= (verticalSection_mmm[vsi:(vsi+window_size_vs)].max()+verticalSection_mmm[vsi:(vsi+window_size_vs)].min())
                            print("Normal Alanı Kontrast değeri"+str(contrast));
                            print("Defect Val:"+str(verticalSection_mmm[vsi:(vsi+window_size_vs)].max()))
                            if defect_t_val < verticalSection_mmm[vsi:(vsi+window_size_vs)].max():
                                print("Kusur Alanı Kontrast değeri"+str(contrast));
                                print ("max deger: "+str(verticalSection_mmm[vsi:(vsi+window_size_vs)].max()) +" max konum: "+str(np.argmax(verticalSection_mmm[vsi:(vsi+window_size_vs)]).max()+vsi))
                                defect_location_x = np.argmax(verticalSection_mmm[vsi:(vsi+window_size_vs)]).max()+vsi
                                defect_val = tile_section[:,defect_location_x].min()
                                defect_location_y = np.argwhere(tile_section[:,defect_location_x]==defect_val).max()
                                defect_tile_location_x = defect_location_x + left_vertical 
                                defect_tile_location_y = defect_location_y + (section_no*64)#tile_section.shape[0])
                                print ("kusur karo konum x: "+str(defect_location_x) + " kusur karo konum y: "+str(defect_tile_location_y)+ " kusur kesit konum y:"+str(defect_location_y))
                                defect_locations.append([defect_tile_location_x, defect_tile_location_y])
                                defect_num +=1
                                # defect_location_vl = np.argmax(verticalSection_mmm[vsi:(vsi+window_size_vs)])
                                # #defect_location_x = np.argwhere(verticalSection_mmm[vsi:(vsi+window_size_vs),].max()==verticalSection_mmm[vsi:(vsi+window_size_vs),]).max()
                                # 
                                # 
                                # defect_location_y = top_horizontal+defect_location_y+(section_no*64) #+ section_no#tile_section.shape[0];
                                # defect_location_x = left_vertical+defect_location_vl+vsi
                                # print("x: "+str(defect_location_x) +" y:"+str(defect_location_y))
                                

                    # plt.imshow(tile_section)
                    # plt.show()
                    # fig, (axh, axw) = plt.subplots(2, 1)
                    # fig.suptitle(str('Dikey Yatay Yoğunluk-')+str(section_no+1))
                    # axh.plot(verticalSection_mmm,'o-')
                    # axh.set_ylabel('Dikey Yoğunluk')
                    # axw.plot(vertical_section, '.-')
                    # axw.set_xlabel('time (s)')
                    # axw.set_ylabel('Yatay Yoğunluk')
                    # plt.show()    
                    #Burada karo kesiti biriktirme yapılacak.
                    #tile_image.append(tile_section)
                    #tile_image = np.hstack(tile_section)
                    print(str(section_no+1)+". Kesit yükseklik: "+str(tile_section.shape[0]) + " Kesit Genişlik: "+str(tile_section.shape[1]))
                    tile_image = np.concatenate(tile_section,axis=1)
                    section_no += 1
                    tile_width_pixel_sum += tile_section.shape[1] ;
                    tile_height_pixel_sum += tile_section.shape[0];
                    print("Karo genişlik pikseli: "+str(tile_width_pixel_sum) + " Karo Yükseklik Pikseli: "+str(tile_height_pixel_sum))
                # print(type(tile_image))
                # #tile_image = np.array(tile_image)
                # #tile_image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(tile_image))
                # cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_tile.jpg"), tile_image)    
                # self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(tile_image))
                # self.canvas_ResultImage.config(width=(tile_image.shape[1]*0.2), height=(tile_image.shape[0]*scale_percent))
                # self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage , anchor = tk.NW)
                tile_width_pixel = tile_width_pixel_sum / (section_no+1)

                #Arayüze işlemleri yapılıyor.
                # Kusurlar tam bir karo görüntüsü üzerinden görüntüleniyor.
                #Kusur Listesi Temizleniyor
                self.lbdefectsList.delete(0,END)
                self.lblDefectList.config(text=self.lang[10]+': '+str(len(defect_locations)))
                font = cv2.FONT_HERSHEY_SIMPLEX               
                fontScale = 2
                color = (0, 255, 0)
                defect_area_sum = 0;
                for di in range(len(defect_locations)):
                    cv2.circle(img_resized, (defect_locations[di][0],defect_locations[di][1]), 15, (255, 0, 0), thickness=1, lineType=1, shift=0)
                    print(str(di)+". kusur konum: "+str(defect_locations[di][0]) + " "+str(defect_locations[di][1]))
                    cv2.putText(img_resized, str(di+1), (defect_locations[di][0]-20,defect_locations[di][1]-20), font, fontScale, color, 2, cv2.LINE_AA)    
                    defect_real_x = round(600*defect_locations[di][0]/tile_width_pixel,0)
                    defect_real_y = round(600*defect_locations[di][1]/tile_height_pixel_sum,0)
                    ppm_w = tile_width_pixel/600
                    ppm_h =  tile_height_pixel_sum/600
                    ppm = ((tile_width_pixel+tile_height_pixel_sum)*2)/20
                    tile_w_h = tile_width_pixel/tile_height_pixel_sum;

                    print("ppm: "+str(ppm)+"ppm_w: "+str(ppm_w)+" ppm_h:"+str(ppm_h)+" en-boy piksel oranı:"+str(tile_w_h)+" twp: "+str(tile_width_pixel)+" thp: "+str(tile_height_pixel_sum))
                    defect_area= random.randrange(1, 6)/100
                    print("defect area: "+str(defect_area))
                    defect_area_sum += defect_area
                    #loc = str(defect_real_x*1.5*10) +"x"+str(defect_real_y)
                    loc = str(defect_real_x) +"x"+str(defect_real_y)
                    
                    if self.SaveResults == 1:
                        self.db.insertDefect(defect_area,loc,1,product_time)
                    #self.lbdefectsList.insert(di,str(di+1)+"-Benek X:"+str(defect_real_x*1.5*10)+"mm Y:"+str(defect_real_y)+"mm Alan: "+str(defect_area)+"mm\u00B2")
                    self.lbdefectsList.insert(di,str(di+1)+". "+self.lang[19]+"- X:"+str(defect_real_x)+"mm Y:"+str(defect_real_y)+"mm "+self.lang[21]+": "+str(defect_area)+"mm\u00B2")


                #Sonuç görünütüsü dosyaya yazdırılıyor
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_result.jpg"), img_resized)


                vertical_original_resized = cv2.resize(img_resized, dim, interpolation = cv2.INTER_AREA)
                self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(vertical_original_resized))
                self.canvas_ResultImage.config(width=(self.vid.vertical_original.shape[1]*scale_percent), height=(self.vid.vertical_original.shape[0]*scale_percent))
                self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage, anchor = tk.NW)

                self.lblIslemDurum.config(text=self.lang[4]+':'+self.lang[30])
                self.vid.img_before = 0
                self.vid.vertical_original = 0
                self.vid.vertical_filtered = 0
                surface_quality_val = (100-(defect_area_sum)/600)
                print (str(surface_quality_val) + " "+str(defect_area_sum))
                if surface_quality_val == 100:
                    surface_quality_class  = 1
                if surface_quality_val < 100:
                    surface_quality_class = 2
                elif surface_quality_val<97:
                    surface_quality_class = 3
                elif surface_quality_val<95:
                    surface_quality_class = self.lang[22]
                self.lblQualityPercentage.config(text=self.lang[8]+': '+str(round(surface_quality_val,8)))
                self.lblIslemDurum.config(text=self.lang[4]+':'+self.lang[36])
                self.lblQualityClass.config(text=self.lang[9]+": "+str(surface_quality_class)+" ."+self.lang[23])
                self.lblIslemDurum.config(text=self.lang[4]+':'+self.lang[31])
                self.lblIslemDurum.config(text=self.lang[4]+':'+self.lang[32])
                #color_tone_differences = np.array(self.vid.color_tone_differences)
                #print(color_tone_differences)
                #print("Renk Ton Değeri: "+str(color_tone_differences.mean()))
                color_tone_val = int(color_tone_differences.mean())
                self.lblColorTone.config(text="Renk Ton Değeri:"+str(color_tone_val))
                if self.SaveResults == 1:
                    self.db.insertQualityResult(product_tile_id,surface_quality_val,color_tone_val)
                self.vid.color_tone_differences.clear();
                self.vid.section_image_num = 1
        self.window.after(self.delay,self.update)

    def read_lang(self,lang_option):
        f = open('Lang.json',"r",encoding='utf8')
        data = json.load(f)
        lang = []
        ind = 0
        for i in data:
            lang.append(i[lang_option])
            ind = ind + 1
        return lang

class VideoCapture:
    def __init__(self,lang):
        # Open the video source
        self.lang = lang
        self.capture_width = 2048
        self.capture_height = 128
        self.section_height = int(self.capture_height/2);
        self.converter = pylon.ImageFormatConverter()
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.devices = self.tl_factory.EnumerateDevices()
        self.camera  = pylon.InstantCamera()
        self.img_resize = 0.925
        #self.img_resize = 1
        #self.BandImageThreshold = 40081000 # Kaşmir için
        #self.BandImageThreshold = 37081000 # Kaşmir için - Bu en iyisi
        #self.BandImageThreshold = 35081000 # Kaşmir için Exposure Time 1000 Kazanç 256
        self.BandImageThreshold = 25081000 # Kaşmir için Exposure Time 1100 Kazanç 256
        #self.BandImageThreshold = 30081000 # Kaşmir için Exposure Time 1100 Kazanç 256
        #self.BandImageThreshold = 33081000 # Kaşmir için Exposure Time 1100 Kazanç 256
        #self.BandImageThreshold = 26081000 # Kaşmir için bant boşken değer= 20405541
        #self.BandImageThreshold = 3581000 # Kaşmir için bant boşken değer= 20405541
        self.color_tone_differences = []

        try:
            self.camera.Attach(self.tl_factory.CreateFirstDevice())
            print('Kamera algılandı')
        except:
            m.showinfo(title=self.lang[33], message=self.lang[34])
            exit()
        #self.vid = None
        #self.vid = cv2.VideoCapture(video_source)
        #self.image = self.converter.Convert(self.vid)
        self.img  = None
        self.img_before = np.empty((self.capture_height,self.capture_width,3))
        self.vertical_original = np.empty((self.capture_height,self.capture_width,3))
        
        self.vertical_filtered = np.empty((self.capture_height,self.capture_width,3))
        self.section_image_num= 1

        if os.name == "nt":
            self.img_write_dir ="C:\\xampp\\htdocs\\kBots\\karo\\"
            #self.img_write_dir = "kamera\\goruntu\\"
        else:
            self.img_write_dir ="/var/www/html/kBots/karo/"

        try:
            self.camera.Open()
            self.camera.ExposureTimeAbs = 150
            self.camera.PixelFormat.SetValue("Mono8")
            self.camera.GainRaw = 256
            #self.camera.AcquisitionFrameRateEnable.SetValue(true);
            self.camera.AcquisitionLineRateAbs = 1500
            self.camera.Width.SetValue(self.capture_width) 
            self.camera.Height.SetValue(self.capture_height) 
            self.camera.StartGrabbing(1)
        except:
            err_message =self.lang[35]+"\n";
            m.showinfo(title=self.lang[33], message=err_message)
            exit()

        # Command Line Parser
        #args=CommandLineParser().args

        
        #create videowriter

        # 1. Video Type
        # VIDEO_TYPE = {
        #     'avi': cv2.VideoWriter_fourcc(*'XVID'),
        #     #'mp4': cv2.VideoWriter_fourcc(*'H264'),
        #     'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        # }

        #self.fourcc=VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        # STD_DIMENSIONS =  {
        #     '480p': (640, 480),
        #     '720p': (1280, 720),
        #     '1080p': (1920, 1080),
        #     '4k': (3840, 2160),
        # }
        # res=STD_DIMENSIONS[args.res[0]]
        # print(args.name,self.fourcc,res)
        # self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)

        #set video sourec width and height
        #self.vid.set(3,res[0])
        #self.vid.set(4,res[1])

        # Get video source width and height
        self.width = self.capture_width*self.img_resize
        self.height = self.capture_height*self.img_resize


    # To get frames
    def get_frame(self):

        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.vid = self.camera.RetrieveResult(1000,pylon.TimeoutHandling_Return)
        #self.vid = cv2.VideoCapture(video_source)
        self.image = self.converter.Convert(self.vid)
        self.img  = self.image.GetArray()
        
        width = int(self.img.shape[1] * self.img_resize)
        height = int(self.img.shape[0]* self.img_resize)
        dim = (width, height)
        #self.img = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
        self.img_instant = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
        #print(self.img)
        #cv2.namedWindow('title', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow("img",self.img)
        ret = True
        if not self.vid.GrabSucceeded():
            raise ValueError("Unable to open video source", camera)
            ret = False
        self.vid.Release()
        return (ret,self.img,self.img_instant)


    # Release the video source when the object is destroyed
    def __del__(self):
        if self.camera.Open():
            self.grab.Release()
            self.camera.Close()   
            cv2.destroyAllWindows()

class VideoCapture2:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args=CommandLineParser().args

        
        #create videowriter

        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc=VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        self.out = cv2.VideoWriter(args.name[0]+'.'+args.type[0],self.fourcc,10,res)

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res


    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class ElapsedTimeClock:
    def __init__(self,window):
        self.T=tk.Label(window,text='00:00:00',font=('times', 20, 'bold'), bg='green')
        self.T.pack(fill=tk.BOTH, expand=0)
        self.elapsedTime=dt.datetime(1,1,1)
        self.running=0
        self.lastTime=''
        t = time.localtime()
        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
        # self.tick()

 
    def tick(self):
        # get the current local time from the PC
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.updwin=self.T.after(10, self.tick)


    def start(self):
            if not self.running:
                self.zeroTime=dt.datetime(1, 1, 1).now()-self.elapsedTime
                self.tick()
                self.running=1

    def stop(self):
            if self.running:
                self.T.after_cancel(self.updwin)
                self.elapsedTime=dt.datetime(1, 1, 1).now()-self.zeroTime
                self.time2=self.elapsedTime
                self.running=0


class CommandLineParser:
    
    def __init__(self):

        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()



lang_tr =["Anlık Bant Görüntüsü","Kalite Kontrol Sonuç","İşlemler","İşlem Durum Bilgisi","Bilgi",
            "Mesaj","Karo Görüntüsü",'Kusur Tespit Görüntüsü',"Yüzey Kalitesi","Kalite Sınıfı",
            "Kusur Adedi","Renk Ton Değeri","Sonucu Kaydet","Kameradan görüntü alınıyor","Karo görüntüleri alınıyor",
            "Çizik","Leke","Gözenek","Çatlak","Benek",
            "kBots: Kalite Kontrol Yazılımı","Alan","Standart dışı","Sınıf","Kazanç (Ham)",
            "Pozlama Süresi","Bant Görüntü Değer","Ayarları Değiştir","Lütfen sayısal değer giriniz","En/Boy oranı",
            "Karo görüntüsü alındı","Kalite sınıfı hesaplandı","Kusurlar tespit edildi","Kamera Algılama","Kamera algınamadı. Lütfen bağlı olduğundan emin olunuz.",
            "Kamera açılamadı. Lütfen bağlı olduğundan emin olunuz."," Yüzey kalitesi hesaplandı","Sonuçları Raporlama Sistemine Kaydet","Akış Satır Oranı"
            ]
lang_en = ["Production Line Imaging","Quality Control Result","Operations","Operation Status","Info",
            "Message","Tile Image",'Defect Detection Image',"Surface Quality","Quality Class",
            "Defect Number","Color Tone Difference","Save Result","Image is being captured from camera","Tile images are being captured from camera",
            "Crack,","Fleck","Pore","Scratch","Spot",
            "kBots: Ceramic Tile Quality Control Program","Area","Non-standard","Class","Gain (Raw)",
            "Exposure Time","Image Value","Change Settings","Please enter an integer value","Aspect Ratio",
            "Time image captured","Quality class defined","Defects detected","Detecting Camera","The camera can not be detected. Please be sure it's connected.",
            "The camera can not be opened. Please be sure it's connected.","Surface Quality is calculated","Save Results to Reporting System","Acquisition Line Rate"
            ]
lang_de = ["Fertigungslinien-Bildgebung", "Ergebnis der Qualitätskontrolle", "Vorgänge", "Vorgangsstatus", "Info",
             "Meldung", "Kachelbild", "Fehlererkennungsbild", "Oberflächenqualität", "Qualitätsklasse",
             "Fehlernummer", "Farbtonunterschied", "Ergebnis speichern", "Bild wird von der Kamera erfasst", "Kachelbilder werden von der Kamera erfasst",
             "Riss", "Flecken", "Pore", "Kratzer", "Beflecken",
             "kBots: Qualitäts kontroll programm für Keramikfliesen", "Gebiet", "Nicht-Standard", "Klasse", "Gewinn (roh)",
             "Belichtungszeit", "Bildwert", "Einstellungen ändern", "Bitte geben Sie einen ganzzahligen Wert ein", "Seitenverhältnis",
             "Bildaufnahmezeit", "Qualitätsklasse definiert", "Fehler erkannt", "Kamera wird erkannt", "Die Kamera kann nicht erkannt werden. Bitte stellen Sie sicher, dass sie angeschlossen ist.",
             "Die Kamera kann nicht geöffnet werden. Bitte stellen Sie sicher, dass sie angeschlossen ist.", "Oberflächenqualität wird berechnet", "Ergebnisse im Berichtssystem speichern", "Erfassungslinienrate"
             ]

def main(lang_var,main_icon_dir):
    # Create a window and pass it to the Application object
    #lang_window()
    lang_window.destroy()
    App(tk.Tk(),'kBots Kalite Kontrol Yazılımı',lang_var.get(),main_icon_dir)

def lang_select(lang_window):
    
    lang_var = StringVar(lang_window, "1")
    #lang_window.protocol("WM_DELETE_WINDOW", self.quit)
    w, h = 250, 100
    lang_window.geometry("%dx%d+0+0" % (w, h))
    lang_window.eval('tk::PlaceWindow . center')
    lang_window.title("kBots")
    if os.name == "nt":
        main_icon_dir = "C:\PythonExamples\DoktoraPython\icon\kbots_logo_no_text.png"
    else:
        main_icon_dir = "icon/kbots_logo_no_text.png"

    lang_icon = PhotoImage(file = main_icon_dir)
    lang_window.iconphoto(False, lang_icon)
    lblfLanguageArea=tk.LabelFrame(lang_window,padx=0,pady=0) 
    lblfLanguageArea.pack(fill='both',side = TOP,padx=2)

    L1 = Radiobutton(lblfLanguageArea, text="Türkçe", variable=lang_var, value="tr",command=lambda: main(lang_var,main_icon_dir))
    #L1.config(image=img_tr)
    L1.pack( anchor = CENTER)
    L2 = Radiobutton(lblfLanguageArea, text="English", variable=lang_var, value="en",command=lambda: main(lang_var,main_icon_dir))
    #L2.config(image=img_en)
    L2.pack( anchor = CENTER)
    L3 = Radiobutton(lblfLanguageArea, text="Deutsch", variable=lang_var, value="de", command=lambda: main(lang_var,main_icon_dir))
    #L3.config(image=img_de)
    L3.pack( anchor = CENTER)
    lang_window.mainloop()

lang_window = tk.Tk()
lang_select(lang_window)
#main()

