import tkinter as tk
import os
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image

class ImageToPDFConverter:

    def __init__(self,root):
        self.root=root
        self.imagepaths=[]
        self.output_pdfname=tk.StringVar()
        self.imgslist=tk.Listbox(root,selectmode=tk.MULTIPLE)
        self.number=0
        self.imgs_selected_label = None
        self.initialize_ui()

    def initialize_ui(self):
        t_label=tk.Label(self.root,text="Image to PDF Converter", font=("Helvetica" , 16, "bold"))
        t_label.pack(pady=10)

        select_img_btn=tk.Button(self.root,text="Select Images", command=self.selectImages)
        select_img_btn.pack(pady=(0,10))

        self.imgslist.pack(pady=(0,10),fill=tk.BOTH,expand=True)

        label=tk.Label(self.root,text="Enter output PDF name:")
        label.pack()

        pdf_name_entry=tk.Entry(self.root,textvariable=self.output_pdfname,width=40,justify='center')
        pdf_name_entry.pack()

        self.imgs_selected_label=tk.Label(self.root,text=f"Number of images selected : {self.number}")
        self.imgs_selected_label.pack()
        
        convert_btn=tk.Button(self.root,text="Convert to PDF", command=self.convert_img_to_pdf)
        convert_btn.pack(pady=(20,40))

    def selectImages(self):
        self.imagepaths=filedialog.askopenfilenames(title="Select Images",filetypes=[("Image files","*.png;*.jpg;*.jpeg")])
        self.update_imgslist() 

    def update_imgslist(self):
        self.imgslist.delete(0,tk.END)
        self.number=0
        for image_path in self.imagepaths:
            self.number+=1
            self.imgs_selected_label.config(text=f"Number of images selected : {self.number}")
            image_path=os.path.split(image_path)
            self.imgslist.insert(tk.END,image_path)
            
    def convert_img_to_pdf(self):
        if not self.imagepaths:
            return 
        outputname=self.output_pdfname.get()+".pdf" if self.output_pdfname.get() else "output.pdf"

        pdf=canvas.Canvas(outputname,pagesize=(612,792))

        for img_path in self.imagepaths:
            img = Image.open(img_path)
            available_width=540
            available_height=720
            scale_factor = min(available_width/img.width,available_height/img.height)
            new_width=img.width*scale_factor
            new_height=img.height*scale_factor
            x_center=(612-new_width)/2
            y_center=(792-new_height)/2

            pdf.setFillColorRGB(255,255,255)
            pdf.rect(0,0,612,792,fill=True)
            pdf.drawInlineImage(img,x_center,y_center,width=new_width,height=new_height)
            pdf.showPage()

        #Saving the pdf
        pdf.save()

def main():
    root=tk.Tk()
    root.title("Image to PDF")
    converter=ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()
        

