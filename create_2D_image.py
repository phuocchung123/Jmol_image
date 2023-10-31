from jupyter_jsmol import JsmolView
from ipywidgets import Layout, widgets, interact
from IPython.display import display
import os
from PIL import Image
import numpy as np
import time
from pynput.keyboard import Key, Controller

class create_2D_image:
    def __init__(self,time_relax=0.5):
        self.folder_path=input('Please input path of your folder you take pdb files or sdf files').replace('\\','/').replace('"','')
        self.folder_save=input('Please input path of your folder you save images').replace('\\','/').replace('"','')
    
    #code to create and download image
    def create_image(self):
        folder_path=self.folder_path
        folder_save=self.folder_save
        a=[]

        # Kiểm tra nếu thư mục tồn tại
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Mở thư mục
            with os.scandir(folder_path) as entries:
                # Lặp qua từng tệp tin trong thư mục
                for entry in entries:
                    if entry.is_file():
                        a.append(entry.name)

        num_files_dir = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
        
        for i in a:
            dem=0
            folder_path=folder_path.replace('\\','/')
            folder_path=folder_path.replace('"','')
            variable_name = "variable_" + i
            globals()[variable_name] = JsmolView.from_file(folder_path+'/'+i, inline=True)
            display(globals()[variable_name])
            globals()[variable_name].script('wireframe 0.15; spacefill 15%')
            name_image=i.replace('.sdf','.png')

            file_path=folder_save+'/'+name_image

            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                dem+=1
                
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
                else:
                    num_files_dir = num_files_dir_new
                    
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
                    ds_path.append(entry.name.replace('.sdf',''))
        self.ds_not_enough= list(set(ds_path) - set(ds_save))
        self.ds_not_enough_1=list(set(ds_save) - set(ds_path))

        
        
        
    #code to create and download images which are not downloaded in first downloading
    def create_image_again(self):
        folder_path=self.folder_path
        folder_save=self.folder_save
        ds_not_enough=self.ds_not_enough

        
        
        num_files_dir = len([f for f in os.listdir(folder_save) if os.path.isfile(os.path.join(folder_save, f))])
        self.check_stop=False
        for i in ds_not_enough:
            dem=0
            folder_path=folder_path.replace('\\','/')
            folder_path=folder_path.replace('"','')
            variable_name = "variable_" + i
            globals()[variable_name] = JsmolView.from_file(folder_path+'/'+i+'.sdf', inline=True)
            display(globals()[variable_name])
            globals()[variable_name].script('wireframe 0.15; spacefill 15%')
            name_image=i+'.png'

            file_path=folder_save+'/'+name_image

            if os.path.exists(file_path):
                globals()[variable_name].close()
            else:
                
                dem+=1
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
                else:
                    num_files_dir = num_files_dir_new
        return self.check_stop
        
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
#             ds_not_enough,ds_duplicate=self.ds_not_enough, self.ds_not_enough_1
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
#                         print('The amount of ds_not_duplicate:',len(self.ds_not_enough_1))
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
            ds_not_enough,ds_duplicate=self.ds_not_enough, self.ds_not_enough_1
            if len(ds_not_enough)==0 and len(ds_duplicate)==0:
                end=time.time()
                print('thời gian chạy là:',end-start)
                print('enough')
                break
            else:
            
                if len(ds_not_enough)!=0:
                    
                    self.create_image_again()
                    if self.check_stop==True:
                        break

                if len(ds_duplicate)!=0:
                    for i in ds_duplicate:
                        path=self.folder_save+'/'+i+'.png'
                        os.remove(path)
        

