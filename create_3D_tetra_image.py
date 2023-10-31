from jupyter_jsmol import JsmolView
from ipywidgets import Layout, widgets, interact
from IPython.display import display
import os
from PIL import Image
import numpy as np
import time
from pynput.keyboard import Key, Controller
class create_3D_tetra_image:
    def __init__(self):
        self.folder_path=input('Please input path of your folder you take pdb files or sdf files').replace('\\','/').replace('"','')
        self.folder_save=input('Please input path of your folder you save images').replace('\\','/').replace('"','')
        
    def create_image(self):
        a=[]
        folder_path=self.folder_path
        folder_save=self.folder_save

        # Kiểm tra nếu thư mục tồn tại
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Mở thư mục/home/labhhc2/Documents/Workspace/D19/Chung/Jmol image/png/class/3d_cube/data_test_inactive
            with os.scandir(folder_path) as entries:
                # Lặp qua từng tệp tin trong thư mục
                for entry in entries:
                    if entry.is_file():
                        a.append(entry.name)

        
        for i in a:
            dem=0
            num_files_dir = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
            folder_path=folder_path.replace('\\','/')
            folder_path=folder_path.replace('"','')
            variable_name = "variable_" + i
            globals()[variable_name] = JsmolView.from_file(folder_path+'/'+i, inline=True)
            display(globals()[variable_name])
            globals()[variable_name].script('wireframe 0.15; spacefill 15%')

            #Hình đầu tiên, không xoay gì cả
            
            name_image=i.replace('.pdb','_1.png')
            file_path=folder_save+'/'+name_image
            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                
                dem=1
                globals()[variable_name].script('moveto 0 0 0 0 0;')
                globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                self.press_enter(0.5)
            #Hình thứ 2 xoay trục x 120 độ 
            
            name_image=i.replace('.pdb','_2.png')
            file_path=folder_save+'/'+name_image
            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                
                dem=1
                globals()[variable_name].script('moveto 0 1 0 0 120;')
                globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                self.press_enter(0.5)
            #Hình thứ 3 xoay trục x 240 độ    
            
            name_image=i.replace('.pdb','_3.png')
            file_path=folder_save+'/'+name_image
            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                
                dem=1
                globals()[variable_name].script('moveto 0 1 0 0 240;')
                globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                self.press_enter(0.5)
            #Hình thứ 4 xoay trục y 120 độ
            
            name_image=i.replace('.pdb','_4.png')
            file_path=folder_save+'/'+name_image
            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                
                dem=1
                globals()[variable_name].script('moveto 0 0 1 0 120;')
                globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                self.press_enter(0.5)       
            globals()[variable_name].close()

            if dem!=0:
                num_files_dir_new = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])

                if num_files_dir == num_files_dir_new:
                    time.sleep(0.5)
                    num_files_dir_new = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
                    if num_files_dir == num_files_dir_new:
                        print("Please check again! Error")
                        break
                        
    def check_duplicate_by_name(self):
        folder_path=self.folder_path
        folder_save=self.folder_save
        ds_path=[]
        ds_save=[]
        
        if os.path.exists(folder_save) and os.path.isdir(folder_save):
            for entry in os.scandir(folder_save):
                if entry.is_file():
                    ds_save.append(entry.name.replace('.png',''))


        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    ds_path.append(entry.name.replace('.pdb',''))

        #tạo ds_path mới vì ds path cũ chỉ có active_1 chứ không có active_1_1, active_1_2,...
        ds_path_2=[]
        for item in ds_path:
            for i in range(1, 5):
                ds_path_2.append(f'{item}_{i}')


        self.ds_not_enough= list(set(ds_path_2) - set(ds_save))
        self.ds_duplicate=list(set(ds_save) - set(ds_path_2))
        
        
    #code to create and download images which are not downloaded in first downloading
    def create_image_again(self):
        folder_path=self.folder_path
        folder_save=self.folder_save
        ds_not_enough=self.ds_not_enough


        #Từ ds_not_enough => xây dựng dict mới như sau, bao gồm các phân tử như 'active_1':[1,2,3,4]
        dict_moi={}
        for item in ds_not_enough:
            key, value = item.rsplit('_', 1)
            if key not in dict_moi:
                dict_moi[key] = []
            dict_moi[key].append(int(value))

        #tạo ds key là sẽ gồm các phần tử như active_1, active_2,...
        ds_key=list(dict_moi.keys())

        #Tạo vòng lặp bắt đầu để tạo nhưng hình bị thiếu
        
        self.check_stop=False
        for i in ds_key:
            num_files_dir = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
            
            folder_path=folder_path.replace('\\','/')
            folder_path=folder_path.replace('"','')
            variable_name = "variable_" + i
            globals()[variable_name] = JsmolView.from_file(folder_path+'/'+i+'.pdb', inline=True)
            display(globals()[variable_name])
            globals()[variable_name].script('wireframe 0.15; spacefill 15%')
            dem=0
            for m in dict_moi[i]:
                if m == 1:
                    #Hình đầu tiên, không xoay gì cả
                    
                    name_image=i+'_1.png'
                    file_path=folder_save+'/'+name_image
                    if os.path.exists(file_path):
                        globals()[variable_name].close()
                    else:

                        dem=1
                        
                        globals()[variable_name].script('moveto 0 0 0 0 0;')
                        globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                        self.press_enter(0.5)
                elif m == 2:
                    #Hình thứ 2 xoay trục x 120 độ 
                    
                    name_image=i+'_2.png'
                    file_path=folder_save+'/'+name_image
                    if os.path.exists(file_path):
                        globals()[variable_name].close()
                    else:
                        dem=1
                        
                        globals()[variable_name].script('moveto 0 1 0 0 120;')
                        globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                        self.press_enter(0.5)
                elif m==3:
                    #Hình thứ 3 xoay trục x 240 độ    
                    
                    name_image=i+'_3.png'
                    file_path=folder_save+'/'+name_image
                    if os.path.exists(file_path):
                        globals()[variable_name].close()
                    else:
                        dem=1
                        
                        globals()[variable_name].script('moveto 0 1 0 0 240;')
                        globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image)
                        self.press_enter(0.5)
                elif m==4:
                    #Hình thứ 4 xoay trục y 120 độ
                    
                    name_image=i+'_4.png'
                    file_path=folder_save+'/'+name_image
                    if os.path.exists(file_path):
                        globals()[variable_name].close()
                    else:
                        dem=1
                        
                        globals()[variable_name].script('moveto 0 0 1 0 120;')
                        globals()[variable_name].script('write IMAGE 224 224 PNG 100 '+name_image) 
                        self.press_enter(0.5)
            globals()[variable_name].close()

            if dem !=0:  
                num_files_dir_new = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])

                if num_files_dir == num_files_dir_new:
                    time.sleep(0.5)
                    num_files_dir_new = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
                    if num_files_dir == num_files_dir_new:
                        print("Please check again! Error")
                        self.check_stop=True
                        break

    def press_enter(self,time_relax):
        keyboard = Controller()
        time.sleep(time_relax)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        
#     def fit(self):
#         start=time.time()
#         self.create_image()
#         while True:
#             self.check_duplicate_by_name()
#             ds_not_enough,ds_duplicate=self.ds_not_enough, self.ds_duplicate
#             if len(ds_not_enough)==0 and len(ds_duplicate)==0:
#                 end=time.time()
#                 print('thời gian chạy là:',end-start)
#                 print('enough')
#                 break
#             else:
            
#                 if len(ds_not_enough)!=0:
                    
#                     self.create_image_again()
#                     if self.check_stop==True:
#                         print('The amount of ds_not_enough:',len(self.ds_not_enough))
#                         print('The amount of ds_not_duplicate:',len(self.ds_duplicate))
#                         print('Please run fit_error')
#                         break

#                 if len(ds_duplicate)!=0:
#                     for i in ds_duplicate:
#                         path=self.folder_save+'/'+i+'.png'
#                         os.remove(path)
                        
    def fit(self):
        start=time.time()
        while True:
            self.check_duplicate_by_name()
            ds_not_enough,ds_duplicate=self.ds_not_enough, self.ds_duplicate
            if len(ds_not_enough)==0 and len(ds_duplicate)==0:
                end=time.time()
                print('thời gian chạy là:',end-start)
                print('enough')
                break
            else:
            
                if len(ds_not_enough)!=0:
                    
                    self.create_image_again()
                    if self.check_stop==True:
                        print('The amount of ds_not_enough:',len(self.ds_not_enough))
                        print('The amount of ds_not_duplicate:',len(self.ds_duplicate))
                        print('Please run fit_error again')
                        break

                if len(ds_duplicate)!=0:
                    for i in ds_duplicate:
                        path=self.folder_save+'/'+i+'.png'
                        os.remove(path)
