import tkinter as tk
import tkinter as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.pyplot import step
import numpy as np
from vis import drawChar
import json
import sys

class Application(tk.Frame):
    def __init__(self, master=None, text=None):
        super().__init__(master)
        self.master = master
        self.master.title('Tefumi Viewer')
                    
        #-----------------------------------------------
        frame = tk.Frame(self.master)        
        self.fig = Figure()
        # self.fig.set_size_inches(5, 20)
        self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        frame.pack(expand=True, side=tk.LEFT)
        
        #-----------------------------------------------
        tk.Label(self.master, text="Text").pack(anchor=tk.NW)
        self.text = tk.Entry()
        if text is not None:
            self.text.insert(tk.END, text)
        self.text.bind('<Return>', self.on_enter)
        self.text.pack(anchor=tk.NW)
        #-----------------------------------------------
        frame = tk.Frame(self.master)

        tk.Label(frame, text="Radius").grid(row=0, column=0)
        slider_radius = tk.Scale(
            frame, from_=1, to=200, orient=tk.HORIZONTAL, 
            command = self.slider_changed)
        self.radius = 100
        slider_radius.set(self.radius)
        slider_radius.grid(row=0, column=1)
        
        #-----------------------------------------------
        self.radius_by_pressure = tk.BooleanVar(value = True)
        self.cb_radius_by_pressure = tk.Checkbutton(frame, text="Radius by Pressure", variable=self.radius_by_pressure, command=self.draw)
        self.cb_radius_by_pressure.grid(row=1, column=1)
        
        #-----------------------------------------------
        tk.Label(frame, text="Alpha").grid(row=2, column=0)
        slider_alpha = tk.Scale(
            frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, 
            command = self.slider_alpha_changed)
        self.alpha = 1
        slider_alpha.set(self.alpha)
        slider_alpha.grid(row=2, column=1)
        
        #-----------------------------------------------
        tk.Label(frame, text="N_sample").grid(row=3, column=0)
        slider_n_sample = tk.Scale(
            frame, from_=1, to=100, orient=tk.HORIZONTAL, 
            command = self.slider_n_sample_changed)
        self.n_sample = 30
        slider_n_sample.set(self.n_sample)
        slider_n_sample.grid(row=3, column=1)

        frame.pack(anchor=tk.NW)
        
        #-----------------------------------------------
        self.radio_value = tk.IntVar(value = 0)
        self.method_values = {
            "pressure_raw": 0,
            "pressure_uniform": 1,
            "density": 2
        }
        self.method = list(self.method_values.keys())[0]
        for k, value in self.method_values.items():
            ttk.Radiobutton(
                self.master, text = k, variable = self.radio_value, value = value, 
                command = self.method_changed).pack(anchor=tk.NW)
        
        ### load stroke data -----------------------------------------------
        with open("data.json", "r") as f:
            self.data = json.load(f)

        ### draw -----------------------------------------------
        self.axes = []
        for i in range(len(self.text.get())):
            self.axes += [self.fig.add_subplot(len(self.text.get()), 1, i+1)]
            self.axes[i].set_aspect('equal') 
            self.axes[i].cla()
            self.axes[i].tick_params(labelbottom=False, labelleft=False)
            self.axes[i].tick_params(bottom=False, left=False, right=False, top=False)
        self.draw()
        
        #-----------------------------------------------
            
    def draw(self):
        for ax, char_ in zip(self.axes, self.text.get()):
            drawChar(
                self.data, char_, ax, 
                method=self.method, 
                radius=self.radius, 
                alpha=self.alpha, 
                n_sample=self.n_sample,
                radius_by_pressure=self.radius_by_pressure.get())
        self.fig_canvas.draw()
        
    def slider_changed(self, v):
        self.radius = int(v)
        self.draw()
        
    def slider_alpha_changed(self, v):
        self.alpha = float(v)
        self.draw()
    
    def slider_n_sample_changed(self, v):
        self.n_sample = float(v)
        self.draw()
        
    def method_changed(self):
        methods = list(self.method_values.keys())
        self.method = methods[int(self.radio_value.get())]
        self.draw()
        
    def on_enter(self, v):
        self.fig.clf()
        self.axes = []
        for i in range(len(self.text.get())):
            self.axes += [self.fig.add_subplot(len(self.text.get()), 1, i+1)]
            self.axes[i].set_aspect('equal') 
            self.axes[i].cla()
            self.axes[i].tick_params(labelbottom=False, labelleft=False)
            self.axes[i].tick_params(bottom=False, left=False, right=False, top=False)
        self.draw()
    
    def resize(self, event):
        global window_width, window_height
        if event.widget.widgetName == "toplevel":
            if (window_width != event.width) and (window_height != event.height):
                window_width, window_height = event.width,event.height
                print(f"The width of Toplevel is {window_width} and the height of Toplevel "
                    f"is {window_height}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root, text="美")
    app.mainloop()