import tkinter as tk
from tkinter import filedialog
window=tk.Tk()
import os
from PIL import Image
import PIL
#import os
import glob
import fileinput
window.geometry("700x300")
window.title('NewGenIm Converter')
window.resizable(0, 0)
HTML_label = tk.Label(window, text="HTML Directory: ")
HTML_label.grid(row=2,column=0, sticky=tk.W, padx=20, pady=85)
html_directory_entry=tk.Entry(window,width=50)
html_directory_entry.grid(column=1,row=2,sticky=tk.E,padx=5,pady=85)


def convert_image(image_path, image_type):

    # 1. Opening the image:
    im = Image.open(image_path)
    # 2. Converting the image to RGB colour:
    im = im.convert('RGBA')
    # 3. Spliting the image path (to avoid the .jpg or .png being part of the image name):
    image_name = image_path.split('.')[0]
    print(f"This is the image name: {image_name}")

    # Saving the images based upon their specific type:
    if image_type == 'jpg' or image_type == 'png' or image_type=="jpeg":
        im.save(f"{image_name}.webp", 'webp')
    else:
        # Raising an error if we didn't get a jpeg or png file type!
        print("Error 404")

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    html_directory_entry.delete(0,tk.END)
    html_directory_entry.insert(0,filename)
    print(filename)
def Get_INFO():
    #d={'.jpg"':'.webp"','.jpeg"':'.webp"','.png"':'.webp"'}
    print(os.getcwd())
    root=html_directory_entry.get()
    for path, subdirs, files in os.walk(root):
        for name in files:
            gets=os.path.join(path, name)
            if gets.endswith('.jpg') or  gets.endswith('jpeg') or gets.endswith('.png'):
                print(os.path.join(path, name))
                if gets.endswith('jpg'):
                    convert_image(gets, image_type='jpg')
                elif gets.endswith('png'):
                    convert_image(gets, image_type='png')
                else:
                    print("Dang")
            elif gets.endswith('.gif'):
                clip=mp.VideoFileClip(gets)
                getsgif=gets.split('.')[0]
                getsgifweb=getsgif+".webm"
                clip.write_videofile(getsgifweb)
            elif gets.endswith('.html'):
                print("Editing",gets,"at the moment")
                with fileinput.FileInput(gets, inplace=True, backup='.bak') as file:
                    for line in file:
                        if '.jpg"' in line:
                            print(line.replace('.jpg"','.webp"'),end="")
                            #print("found jpg, replacing")
                            #print(line,end="")
                        elif '.jpeg"' in line:
                            print(line.replace('.jpeg"','.webp"'),end="")
                            #print(line,end="")
                        elif '.png"' in line:
                            print(line.replace('.png"','.webp"'),end="")
                            #print(line,end="")
                        elif '.jpg\'' in line:
                           print(line.replace('.jpg\'','.webp\''),end="")
                           #print(line,end="")
                        elif '.jpeg\'' in line:
                            print(line.replace('.jpeg\'','.webp\''),end="")
                            #print(line,end="")
                        elif '.png\'' in line:
                            print(line.replace('.png\'','.webp\''),end="")
                            #print(line,end="")
                        elif '.gif\'' in line:
                            print(line.replace('.gif\'','.webm\''),end="")
                        elif '.gif"' in line:
                            print(line.replace('.gif\"','.webm\"'),end="")


                        else:
                            print(line,end="")
                        #print(line,end="")
                print("Done with HTML Editing")
    tk.messagebox.showinfo("NewGenIm converter", "NewGenIm has successfully increased the perfomance of the website!")
browse_button=tk.Button(text="Choose HTML folder", command=browse_button)
browse_button.grid(row=3, column=1,padx=150)
display_button=tk.Button(text="Convert!", command=Get_INFO)
display_button.grid(row=4, column=1,padx=150)

window.mainloop()
