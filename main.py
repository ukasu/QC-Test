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


class App:
    def __init__(self, window, window_title):
        
        self.window = window
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (self.w, self.h))
        #self.window.bind("<Configure>", YenidenBoyutlandir)
        self.window.title(window_title)
        self.window.title("kBots Kalite Kontrol Yazılımı")
        self.icon = PhotoImage(file = "C:\PythonExamples\DoktoraPython\icon\kbots_logo_no_text.png")
        self.window.iconphoto(False, self.icon)
        self.db = Database() 
        self.db.connect()
        #self.video_source = video_source
        self.ok=False
        #timer
        #self.timer=ElapsedTimeClock(self.window)
        lblfInstantCameraScreen=tk.LabelFrame(self.window,text="Anlık Bant Görüntüsü",padx=0,pady=0) 
        lblfInstantCameraScreen.pack(fill='both',side = TOP,padx=2)
        lblfResult=tk.LabelFrame(self.window,text="Kalite Kontrol Sonuç",padx=0,pady=0) 
        lblfResult.pack(fill='both',side = TOP,padx=5) 
        lblfOperation = tk.LabelFrame(self.window,text="İşlemler",padx=0,pady=0) 
        lblfOperation.pack(fill='both',side = TOP,padx=5)
        lblfStatus = LabelFrame(window,text='İşlem Durum Bilgisi',padx=0,pady=0)
        lblfStatus.pack(fill="both",side = TOP,padx=5)
        self.lblIslemDurum = tk.Label(lblfStatus,text='Bilgi:',anchor=W)
        self.lblIslemDurum.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='W')   
        self.lblMessage = tk.Label(lblfStatus,text='Mesaj:',anchor=W)
        self.lblMessage.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='W')   

        #lblDeneyeAdi = tk.Label(lblfInstantCameraScreen,text="Deney Adı Girin")
        #lblDeneyeAdi.grid(row=0,column=0,padx=10,pady=10)
        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture()

        # Create a canvas that can fit the above video source size
        self.canvas_InstantCamera=tk.Canvas(lblfInstantCameraScreen, width = self.vid.width, height = self.vid.height,borderwidth=1)
        #self.canvas_InstantCamera = tk.Canvas(lblfInstantCameraScreen, width = 60, height = 60)
        self.canvas_InstantCamera.grid(row=0,column=0,padx=5,pady=2)
        
        self.canvas_TileImage = tk.Canvas(lblfResult,bd=1, highlightthickness=0, relief='ridge',width=377,height=332)
        self.canvas_TileImage.grid(row=0,column=0,padx=10,pady=10)
        self.canvas_ResultImage = tk.Canvas(lblfResult,bd=1, highlightthickness=0, relief='ridge',width=377,height=332)
        self.canvas_ResultImage.grid(row=0,column=1,padx=10,pady=10)

        self.title_canvas_TileImage = tk.Label(lblfResult,text='Karo Görüntüsü',anchor=N,width=20, height=1,font=("Arial", 12))
        self.title_canvas_TileImage.grid(row=1,column=0,padx=0,pady=0,sticky='N',columnspan=1)
        self.title_canvas_ResultImage = tk.Label(lblfResult,text='Kusur Tespit Görüntüsü',anchor=N,width=20, height=1,font=("Arial", 12))
        self.title_canvas_ResultImage.grid(row=1,column=1,padx=0,pady=0,sticky='N',columnspan=1)        

        lblfQualityResult=tk.LabelFrame(lblfResult,padx=1,pady=2,width=60, height=20, borderwidth=0) 
        lblfQualityResult.grid(row=0,column=2,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=0) 
        self.lblQualityPercentage = tk.Label(lblfQualityResult,text='Yüzey Kalitesi: -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblQualityPercentage.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        self.lblQualityClass = tk.Label(lblfQualityResult,text='Kalite Sınıfı: -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblQualityClass.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        
        lblfDefectList = tk.LabelFrame(lblfResult,padx=1,pady=2,width=25, height=10,borderwidth=0) 
        lblfDefectList.grid(row=0,column=3,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10) 
        self.lblDefectList = tk.Label(lblfDefectList,text='Kusur Adedi: -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblDefectList.grid(row=0,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 
        self.lbdefectsList = Listbox(lblfDefectList,width=38, height=10,font=("Arial", 10))
        self.lbdefectsList.grid(row=1,column=0,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10)
        
        lblfColorTone = tk.LabelFrame(lblfResult,padx=1,pady=2,width=25, height=10,borderwidth=0) 
        lblfColorTone.grid(row=2,column=3,columnspan=1,padx=0,pady=0,sticky='NW',ipadx=10, ipady=10) 
        self.lblColorTone = tk.Label(lblfQualityResult,text='Renk Ton Değeri: -',anchor=NW,width=20, height=1,font=("Arial", 25))
        self.lblColorTone.grid(row=3,column=0,columnspan=1,padx=0,pady=0,sticky='NW') 


        # # Button that lets the user take a snapshot
        
        self.btn_snapshot=tk.Button(lblfOperation, text="Sonucu Kaydet", command=self.snapshot)
        self.btn_snapshot.grid(row=0,column=0,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        self.lblExposureTime = tk.Label(lblfOperation,text='Pozlama Süresi (us)',anchor=NW,width=16, height=1,font=("Arial", 12))
        self.lblExposureTime.grid(row=0,column=1,columnspan=1,padx=0,pady=5,sticky='NW') 
        self.lblGainRaw = tk.Label(lblfOperation,text='Kazanç (Ham)',anchor=NW,width=12, height=1,font=("Arial", 12))
        self.lblGainRaw.grid(row=0,column=3,columnspan=1,padx=0,pady=5,sticky='NW') 
        self.lblBantImageThreshold = tk.Label(lblfOperation,text='Bant Görüntü Değer',anchor=NW,width=16, height=1,font=("Arial", 12))
        self.lblBantImageThreshold.grid(row=0,column=5,columnspan=1,padx=0,pady=5,sticky='NW') 
        stExposureTime= StringVar(lblfOperation)
        stExposureTime.set("850")#1000-25081000
        stGainRaw = StringVar(lblfOperation)
        stGainRaw.set("256")
        stBantImageThreshold= StringVar(lblfOperation)
        #stBantImageThreshold.set("30081000")
        stBantImageThreshold.set("13000000")#1000-25081000
        self.entExposureTime = Spinbox(lblfOperation,from_ = 1, to = 3000,bd=1,width=5,textvariable=stExposureTime)
        self.entExposureTime.grid(row=0,column=2,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        self.entGainRaw = Spinbox(lblfOperation,from_ = 256, to = 2047,bd=1,width=5,textvariable=stGainRaw)
        self.entGainRaw.grid(row=0,column=4,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        self.entBantImageThreshold = Spinbox(lblfOperation,from_ = 10000000, to = 90081000,bd=1,width=8,textvariable=stBantImageThreshold)
        self.entBantImageThreshold.grid(row=0,column=6,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)
        self.bntChangeSettings=tk.Button(lblfOperation, text="Ayarları Değiştir", command=self.update_settings)
        self.bntChangeSettings.grid(row=0,column=7,columnspan=1,padx=0,pady=5,sticky='NW',ipadx=5, ipady=5)

        self.delay=100
        self.update()

        self.window.mainloop()

    def quit(self):
        print("Çıkış sağlandı")
        #if m.askokcancel("Çıkış", "Emin misin?"):  
        self.vid.camera.Open()
        #self.vid.Release()
        self.vid.camera.Close() 
        self.window.destroy()
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
            self.vid.BandImageThreshold = BandImageThreshold
            self.vid.camera.ExposureTimeAbs = ExposureTimeVal
            self.vid.camera.GainRaw = GainRawVal
            print (str(self.vid.camera.ExposureTimeAbs.Value) + " "+str(self.vid.camera.GainRaw.Value))
        except  ValueError:
            self.lblMessage.config(text="Mesaj: Lütfen sayısal değer giriniz.")
            self.lblMessage.config(bg="#f57f7f")
       
    def update(self):
        
        # Get a frame from the video source
        ret,frame,frame_instant = self.vid.get_frame()
        
        if ret:
            self.InstantImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_instant))
            self.canvas_InstantCamera.create_image(0, 0, image = self.InstantImage, anchor = tk.NW)
        
        tile_no = 26
        image_sum = np.sum(frame)  
        now = datetime.now()
        defect_locations = []
        defect_num = 0;
        tile_width_pixel = 0
        tile_height_pixel  = 0
        product_time = now.strftime("%Y-%m-%d %H:%M:%S")
        img_file_name = str(tile_no) + "_"+str(int(self.vid.camera.GainRaw.Value))+"_"+str(int(self.vid.camera.ExposureTimeAbs.Value))+"_"+now.strftime("%Y%m%d%H%M%S")
        print(image_sum)
        #self.lblIslemDurum.config(text='Bilgi: Kameradan görüntü alınıyor. - '+str(image_sum/89786))
        self.lblIslemDurum.config(text='Bilgi: Kameradan görüntü alınıyor. - ')
        if (self.vid.BandImageThreshold)<image_sum:
            plt.close('all')
            self.lblIslemDurum.config(text='Bilgi: Karo görüntüsü alınıyor.- '+str(image_sum))
            img_before_sum = np.sum(self.vid.img_before)
            
            img = frame
            print("Boyut: "+str(img.shape))
            img_original =  img[:,17:frame.shape[1]-17]
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
                self.lblMessage.config( text="Mesaj: En/Boy oranı: "+str(self.vid.vertical_original.shape[1]/self.vid.vertical_original.shape[0]))
                self.canvas_TileImage.create_image(0, 0, image = self.TileImage , anchor = tk.NW)
                #self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(vertical_filtered_resized))
                #self.canvas_ResultImage.config(width=(self.vid.vertical_original.shape[1]*0.2), height=(self.vid.vertical_original.shape[0]*scale_percent))
                #self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage , anchor = tk.NW)
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+".jpg"), self.vid.vertical_original)
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_filter.jpg"), self.vid.vertical_filtered)
                print(str((self.vid.section_image_num))+" kesit alındı ve görüntü kaydedildi")
                
                #Veri Tabanı İşlemleri Yapılıyor
                product_tile_id = self.db.insertProduct(1,product_time,(self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)))

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
                        start_vs = 20
                        end_vs = verticalSection_mmm.shape[0]-20
                        #print("vertical_section_mmm-w: "+str(verticalSection_mmm.shape[0]))
                        window_size_vs = int(round((verticalSection_mmm.shape[0]/60),0))
                        defect_t_val  = 0.22; #0.22 orjinal
                        print("Pencere Boyutu:"+str(window_size_vs))
                        for vsi in range(start_vs,end_vs,window_size_vs):
                            if defect_t_val < verticalSection_mmm[vsi:(vsi+window_size_vs)].max():
                                
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
                    tile_width_pixel += tile_section.shape[1] ;
                    tile_height_pixel += tile_section.shape[0];
                    print("Karo genişlik pikseli: "+str(tile_width_pixel) + " Karo Yükseklik Pikseli: "+str(tile_height_pixel))
                # print(type(tile_image))
                # #tile_image = np.array(tile_image)
                # #tile_image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(tile_image))
                # cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_tile.jpg"), tile_image)    
                # self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(tile_image))
                # self.canvas_ResultImage.config(width=(tile_image.shape[1]*0.2), height=(tile_image.shape[0]*scale_percent))
                # self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage , anchor = tk.NW)
                
                #Arayüze işlemleri yapılıyor.
                # Kusurlar tam bir karo görüntüsü üzerinden görüntüleniyor.
                #Kusur Listesi Temizleniyor
                self.lbdefectsList.delete(0,END)
                self.lblDefectList.config(text='Kusur Adedi: '+str(len(defect_locations)))
                font = cv2.FONT_HERSHEY_SIMPLEX               
                fontScale = 2
                color = (0, 255, 0)
                defect_area_sum = 0;
                for di in range(len(defect_locations)):
                    cv2.circle(img_resized, (defect_locations[di][0],defect_locations[di][1]), 15, (255, 0, 0), thickness=1, lineType=1, shift=0)
                    print(str(di)+". kusur konum: "+str(defect_locations[di][0]) + " "+str(defect_locations[di][1]))
                    cv2.putText(img_resized, str(di+1), (defect_locations[di][0]-20,defect_locations[di][1]-20), font, fontScale, color, 2, cv2.LINE_AA)    
                    defect_real_x = round(600*defect_locations[di][0]/tile_width_pixel,0)
                    defect_real_y = round(600*defect_locations[di][1]/tile_height_pixel,0)
                    
                    defect_area= random.randrange(1, 6)/100
                    print("defect area: "+str(defect_area))
                    defect_area_sum += defect_area
                    loc = str(defect_real_x*1.5*10) +"x"+str(defect_real_y)
                    self.db.insertDefect(defect_area,loc,1,product_time)
                    self.lbdefectsList.insert(di,str(di+1)+"-Benek X:"+str(defect_real_x*1.5*10)+"mm Y:"+str(defect_real_y)+"mm Alan: "+str(defect_area)+"mm\u00B2")

                #Sonuç görünütüsü dosyaya yazdırılıyor
                cv2.imwrite((self.vid.img_write_dir+img_file_name+"_"+str(self.vid.BandImageThreshold)+"_"+str(self.vid.section_image_num)+"_result.jpg"), img_resized)
                
                vertical_original_resized = cv2.resize(img_resized, dim, interpolation = cv2.INTER_AREA)
                self.ResultImage = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(vertical_original_resized))
                self.canvas_ResultImage.config(width=(self.vid.vertical_original.shape[1]*scale_percent), height=(self.vid.vertical_original.shape[0]*scale_percent))
                self.canvas_ResultImage.create_image(0, 0, image = self.ResultImage, anchor = tk.NW)

                self.lblIslemDurum.config(text='Bilgi: Karo görüntüsü alındı.')
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
                    surface_quality_class = "Standart Dışı"
                self.lblQualityPercentage.config(text='Yüzey Kalitesi: '+str(surface_quality_val))
                self.lblIslemDurum.config(text='Bilgi: Yüzey kalitesi hesaplandı.')
                self.lblQualityClass.config(text="Kalite Sınıfı: "+str(surface_quality_class)+" .sınıf")
                self.lblIslemDurum.config(text='Bilgi: Kalite sınıfı hesaplandı.')
                self.lblIslemDurum.config(text='Bilgi: Kusurlar tespit edildi.')
                #color_tone_differences = np.array(self.vid.color_tone_differences)
                #print(color_tone_differences)
                #print("Renk Ton Değeri: "+str(color_tone_differences.mean()))
                color_tone_val = int(color_tone_differences.mean())
                self.lblColorTone.config(text="Renk Ton Değeri:"+str(color_tone_val))
                self.db.insertQualityResult(product_tile_id,surface_quality_val,color_tone_val)
                self.vid.color_tone_differences.clear();
                self.vid.section_image_num = 1

        self.window.after(self.delay,self.update)
class VideoCapture:
    def __init__(self):
        # Open the video source
        self.capture_width = 2048
        self.capture_height = 128
        self.section_height = int(self.capture_height/2);
        self.converter = pylon.ImageFormatConverter()
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.devices = self.tl_factory.EnumerateDevices()
        self.camera  = pylon.InstantCamera()
        self.img_resize = 0.925

        self.BandImageThreshold = 25081000 # Kaşmir için Exposure Time 1100 Kazanç 256

        self.color_tone_differences = []

        try:
            self.camera.Attach(self.tl_factory.CreateFirstDevice())
            print('Kamera algılandı')
        except:
            m.showinfo(title="Kamera Algılama", message="Kamera algınamadı. Lütfen bağlı olduğundan emin olunuz.")
            exit()
        self.vid = None

        self.img  = None
        self.img_before = np.empty((self.capture_height,self.capture_width,3))
        self.vertical_original = np.empty((self.capture_height,self.capture_width,3))
        
        self.vertical_filtered = np.empty((self.capture_height,self.capture_width,3))
        self.section_image_num= 1
        #self.img_write_dir = "kamera\\goruntu\\"
        self.img_write_dir ="C:\\xampp\\htdocs\\kBots\\karo\\"
        try:
            self.camera.Open()
            self.camera.ExposureTimeAbs = 1000
            self.camera.PixelFormat.SetValue("Mono8")
            self.camera.GainRaw = 256
            self.camera.Width.SetValue(self.capture_width) 
            self.camera.Height.SetValue(self.capture_height) 
            self.camera.StartGrabbing(1)
        except:
            err_message ="Kamera açılamadı. Lütfen bağlı olduğundan emin olunuz.\n";
            m.showinfo(title="Kamera Algılama", message=err_message)
            exit()

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

def main():
    # Create a window and pass it to the Application object
    App(tk.Tk(),'kBots Kalite Kontrol Yazılımı')

main()

