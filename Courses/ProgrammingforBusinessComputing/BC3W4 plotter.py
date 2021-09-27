import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk
import matplotlib.pyplot as pyplot
import os

class Plotter(tk.Frame):

  def __init__(self, master = None):
    tk.Frame.__init__(self, master) 
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    f = tkFont.Font(size = 16, family = "Courier New")
    
    self.lblX = tk.Label(self, text = "x:", height = 1, width = 3, font = f)
    self.lblY = tk.Label(self, text = "y:", height = 1, width = 3, font = f)

    self.txtX = tk.Text(self, height = 1, width = 40, font = f)
    self.txtY = tk.Text(self, height = 1, width = 40, font = f)
    
    self.btnLoad = tk.Button(self, text = "plot!", height = 1, width = 5, command = self.clickBtnLoad, font = f)
    self.cvsMain = tk.Canvas(self, width = 800, height = 600, bg = "white")
	
    self.lblX.grid(row = 0, column = 0, sticky = tk.E)
    self.lblY.grid(row = 1, column = 0, sticky = tk.E)
    self.txtX.grid(row = 0, column = 1, sticky = tk.NE + tk.SW)
    self.txtY.grid(row = 1, column = 1, sticky = tk.NE + tk.SW)
    self.btnLoad.grid(row = 0, rowspan = 2, column = 2, sticky = tk.NE + tk.SW)
    self.cvsMain.grid(row = 2, column = 0, columnspan = 3, sticky = tk.NE + tk.SW)
	
  def clickBtnLoad(self):
    x = self.txtX.get("1.0", tk.END).split(",")
    for i in range(len(x)):
      x[i] = float(x[i])
    
    y = self.txtY.get("1.0", tk.END).split(",")
    for i in range(len(y)):
      y[i] = float(y[i])
    
    self.makeScatter(x, y)

    self.imageMain = ImageTk.PhotoImage(file = "C:\\Users\\BERLIN CHEN\\Desktop\\BC- Python\\temp.png")
    self.cvsMain.create_image(400, 300, image = self.imageMain, anchor = tk.CENTER)
    os.system("del C:\\Users\\BERLIN CHEN\\Desktop\\BC- Python\\temp.png")

  def makeScatter(self, x, y): 
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
	
    rangeX = max(x) - min(x)
    ax.set_xlim(min(x) - rangeX * 0.1, max(x) + rangeX * 0.1)
    rangeY = max(y) - min(y)
    ax.set_ylim(min(y) - rangeY * 0.1, max(y) + rangeY * 0.1)

    pyplot.plot(x, y, 'bo')

    for i, j in zip(x, y):
      ax.annotate(str(i) + ", " + str(j), xy = (i + 0.1, j + 0.1))

    pyplot.savefig("C:\\Users\\BERLIN CHEN\\Desktop\\BC- Python\\temp.png") 
  
pl = Plotter()
pl.master.title("My Plotter")
pl.mainloop()