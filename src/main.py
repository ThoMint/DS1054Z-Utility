import tkinter as tk
from ds1054z import DS1054Z
from jds6600 import *
from PIL import Image, ImageOps, ImageEnhance
import time
import io
import os

from jds6600 import jds6600


class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.gen = None
		self.scope = None
		self.grid()
		self.createWidgets()
		self.master.after(50,self.handle)

	def createWidgets(self):
		# Scope
		self.scopeAddressEntry = tk.Entry(self)
		self.scopeAddressEntry.grid(column=0, row=0)

		self.connectScopeButton = tk.Button(self, text="Connect Scope", command=self.connectScope)
		self.connectScopeButton.grid(column=1, row=0)

		self.scopeConnected = tk.Label(self, text="N/A")
		self.scopeConnected.grid(column=2, row=0)

		# Generator
		self.genAddressEntry = tk.Entry(self)
		self.genAddressEntry.grid(column=0, row=1)

		self.connectGenButton = tk.Button(self, text="Connect Gen", command=self.connectGen)
		self.connectGenButton.grid(column=1, row=1)

		self.genConnected = tk.Label(self, text="N/A")
		self.genConnected.grid(column=2, row=1)

		# Save Screen
		self.saveScreenNameEntry = tk.Entry(self)
		self.saveScreenNameEntry.grid(column=0, row=2)

		self.saveScreenButton = tk.Button(self, text="Save Screen", state="disabled", command=self.saveScreen)
		self.saveScreenButton.grid(column=1, row=2)

		# Gen frequency response
		self.frequencyResponseButton = tk.Button(self, text="Frequ Response", state="disabled", command=self.launchFrequResponse)
		self.frequencyResponseButton.grid(column=1, row=3)

		self.frequencyResponseEnable = tk.Label(self, text="N/A")
		self.frequencyResponseEnable.grid(column=2, row=3)
		

	def handle(self):
		# print("handling")
		self.master.after(50,self.handle)

	def saveScreen(self):
		fmt = 'out/ds1054z-scope-display_{ts}.png'
		ts = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
		if self.saveScreenNameEntry.get():
			filename = "out/" + self.saveScreenNameEntry.get()
		else:
			filename = fmt.format(ts=ts)
		# need to find out file extension for Pillow on Windows...
		ext = os.path.splitext(filename)[1]
		if not ext:
			print('could not detect the image file type extension from the filename')
			return
		# getting and saving the image
		im = Image.open(io.BytesIO(self.scope.display_data))
		im.putalpha(255)
		im = Image.merge("RGB", im.split()[0:3])
		im = ImageOps.invert(im)
		# im = ImageEnhance.Color(im).enhance(0)
		# im = ImageEnhance.Brightness(im).enhance(0.95)
		# im = ImageEnhance.Contrast(im).enhance(2)
		# im = im.convert('L')
		# im = im.point(lambda x: x if x<252 else 255)
		im.save(filename, format=ext[1:])
		print("Saved file: " + filename)

	def launchFrequResponse(self):
		print("Frequ response")

	def connectScope(self):
		if self.scopeAddressEntry.get():
			self.scope = DS1054Z(self.scopeAddressEntry.get())
			if self.scope:
				self.connectScopeButton.configure(state="disabled")
				self.saveScreenButton.configure(state="normal")
				self.scopeConnected.configure(text="OK")
				print("Connected to Scope at " + self.scopeAddressEntry.get())
				if self.gen:
					self.frequencyResponseButton.configure(state="normal")
					self.frequencyResponseEnable.configure(text="OK")

	def connectGen(self):
		if self.genAddressEntry.get():
			self.gen = jds6600(self.genAddressEntry.get())
			if self.gen:
				self.connectGenButton.configure(state="disabled")
				self.genConnected.configure(text="OK")
				print("Connected to Gen at " + self.genAddressEntry.get())
				if self.scope:
					self.frequencyResponseButton.configure(state="normal")
					self.frequencyResponseEnable.configure(text="OK")

app = Application()
app.master.title("DS1054Z-Utility")
app.mainloop()