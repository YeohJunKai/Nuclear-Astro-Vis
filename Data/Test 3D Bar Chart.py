# Creating Frames 
from math import asinh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QSlider, QLineEdit
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import csv
f=open("/Users/rafaeldesouza/Documents/GitHub/Nuclear-Astro-Vis/3D Bar Chart Frames/Frame 1.csv","r")
openf=list(csv.reader(f, delimiter=',', quotechar='|'))
totalframes=int(openf[5][1])
zmaxvalue=float(openf[2][0])
pronum=openf[0]
neunum=openf[1]
for i in range(209):
    pronum[i]=int(pronum[i])
    neunum[i]=int(neunum[i])
f.close()

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure(figsize=(10,10))

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # A slider to make time variations
        self.horizontalSlider = QSlider(Qt.Horizontal)
        self.horizontalSlider.valueChanged.connect(self.plot)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(totalframes-1)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)

        # Textbox for Slider
        self.textbox = QLineEdit()
        
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.textbox)
        layout.addWidget(self.horizontalSlider)
        self.setWindowTitle("Isotopic Abundance Ratios")
        self.setLayout(layout)

        # Generate the chart for t=0 when the window is opened
        self.plot()

    def plot(self):
        # Read the slider value
        timesno = int(self.horizontalSlider.value())+1
        f=open("/Users/rafaeldesouza/Documents/GitHub/Nuclear-Astro-Vis/3D Bar Chart Frames/Frame %d.csv" %timesno,"r")
        openf=list(csv.reader(f, delimiter=',', quotechar='|'))
            
        # Creating Frame
        time=float(openf[3][0])
        self.textbox.setText(str(time))
        abunnum=openf[2]
        
        for i in range(209):
            abunnum[i]=float(abunnum[i])
            
        asinhabunnum=list(map(asinh,abunnum))
        f.close()
        
        # Discards the old chart and display the new one
        top = asinhabunnum
        bottom = np.zeros_like(top)
        ax = self.figure.add_subplot(111,projection='3d')
        ax.hold(False)
        ax.bar3d(pronum, neunum, bottom, 1, 1, top)
        ax.set_title('Reaction Ratios')
        ax.set_xlabel('Proton Number')
        ax.set_ylabel('Neutron Number')
        ax.set_zlabel('Abundance Ratio')
        ax.set_zlim(0,1.1*(asinh(zmaxvalue)))

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())







