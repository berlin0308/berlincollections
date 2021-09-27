import tkinter as tk
import tkinter.font as tkFont
import math

class Calculator(tk.Frame):

  def __init__(self):
    tk.Frame.__init__(self) 
    self.grid()
    self.createWidgets()

  def createWidgets(self):
    font1 = tkFont.Font(size = 16,family = "Courier New") 
    self.textbox = tk.Text(self, height = 1, width = 20, font = font1) 
    self.btnSqure = tk.Button(self, text = "square", height = 1, width = 10, font = font1, command = self.clickBtnSquare) 
    self.textbox.grid(row = 0, column = 0)
    self.btnSqure.grid(row = 1, column = 0)
	
  def clickBtnSquare(self):
    value = self.textbox.get("1.0", tk.END) #get the value of textbox
    square_value = str(int(math.pow(float(value), 2))) #calculate the square value
    self.textbox.delete("1.0", tk.END) #delete the value of textbox
    self.textbox.insert("1.0", square_value) #update the value

cal = Calculator()
cal.master.title("My Calculator")
cal.mainloop()