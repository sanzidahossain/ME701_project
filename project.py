
import sys
import platform
import numpy as np
from control import tf



from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QLineEdit, 
                             QVBoxLayout, QAction, QMessageBox,QFileDialog,
                             QSizePolicy, QComboBox)
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from PyQt5.QtGui import QIcon, QPixmap

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import control
from scipy.signal import lti, step

       

class MainWindow3(QMainWindow, QDialog) :
    
    def __init__(self, parent=None) :
        super(MainWindow3, self).__init__(parent)

        ########################################################################
        # ADD MENU ITEMS
        ########################################################################
        
        # Create the File menu
        self.filename = ""
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionSaveAs = QAction("&Save As", self)
        self.actionSaveAs.triggered.connect(self.saveas)
        self.actionQuit = QAction("&Quit", self)
        self.actionQuit.triggered.connect(self.close)
        self.menuFile.addActions([self.actionSaveAs, self.actionQuit])
        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.menuHelp.addActions([self.actionAbout])
        
        ########################################################################
        # CREATE CENTRAL WIDGET
        ########################################################################

        self.widget = QDialog()
        self.plot1 = MatplotlibCanvas1()
        self.plot2 = MatplotlibCanvas2()

#        self.edit1 = QLineEdit("enter the plot title here!")
#        self.edit2 = QLineEdit("ignore me for now")
        
        self.plant_edit = QLineEdit("tf([],[])")
        self.plant_edit.selectAll()
        self.parameter_edit = QLineEdit("tf([],[])")
        self.parameter_edit.selectAll()
        self.controller_edit = QLineEdit("tf([],[])")
        self.controller_edit.selectAll()
        self.feedback_edit = QLineEdit("0")
        self.feedback_edit.selectAll()
        self.input_edit = QLineEdit("1")
        self.input_edit.selectAll()
        self.output_edit = QLineEdit(" ")
        self.output_edit.selectAll()
        self.os_edit = QLineEdit("0")
        self.os_edit.selectAll()
        self.ts_edit = QLineEdit("0")
        self.ts_edit.selectAll()
        self.tr_edit = QLineEdit("0")
        self.tr_edit.selectAll()
        
        self.os_editn = QLineEdit("0")
        self.os_editn.selectAll()
        self.ts_editn = QLineEdit("0")
        self.ts_editn.selectAll()
        self.tr_editn = QLineEdit("0")
        self.tr_editn.selectAll()
        
        self.gm_edit = QLineEdit("0")
        self.gm_edit.selectAll()
        self.pm_edit = QLineEdit("0")
        self.pm_edit.selectAll()
        self.gc_edit = QLineEdit("0")
        self.gc_edit.selectAll()
        self.pc_edit = QLineEdit("0")
        self.pc_edit.selectAll()
        
        self.opo_edit = QTextEdit("0")
        self.opo_edit.selectAll()
        self.oze_edit = QTextEdit("0")
        self.oze_edit.selectAll()
        self.cpo_edit = QTextEdit("0")
        self.cpo_edit.selectAll()
        self.cze_edit = QTextEdit("0")
        self.cze_edit.selectAll()
        self.tf1_edit = QTextEdit("0")
        self.tf1_edit.selectAll()
        self.tf2_edit = QTextEdit("0")
        self.tf2_edit.selectAll()
#        self.widg = QLineEdit("kj", self)

#        combo = QComboBox(self)
#        
#        combo.setEditable(True)
#        combo.addItem("np.sin(2*np.pi*x)")
#        combo.addItem("np.cos(2*np.pi*x)")
#        combo.addItem("np.tan(2*np.pi*x)")
#        combo.addItem("user func")
        
        self.label1 = QLabel("Plant(G)")
        self.label2 = QLabel("Controller(C)")
        self.label3 = QLabel("Feedback(H)")
        self.label7 = QLabel("Input(F)")
        self.label4 = QLabel("% Overshoot")
        self.label5 = QLabel("Settling time(sec)")
        self.label6 = QLabel("Rising time(sec)")
        self.label4n = QLabel("% Overshoot")
        self.label5n = QLabel("Settling time(sec)")
        self.label6n = QLabel("Rising time(sec)")
        self.label8 = QLabel("Plant Chatacteristics")
        self.label9 = QLabel("Whole System Chatacteristics")
        self.label10 = QLabel("System Stability Mergins")
        self.label11 = QLabel("Whole System Chatacteristics")
        self.label12 = QLabel("Gain margin(dB)")
        self.label13 = QLabel("Phase Margin(deg)")
        self.label14 = QLabel("Gain Crossover Frequency(rad/sec)")
        self.label15 = QLabel("Phase Crossover Frequency(rad/sec)")
        
        self.label16 = QLabel("Plant")
        self.label17= QLabel("Whole System")
        self.label18= QLabel("Poles")
        self.label19= QLabel("Zeros")
        self.label20= QLabel("Poles")
        self.label21= QLabel("Zeros")
        
        
        label = QLabel(self)
        pixmap = QPixmap('image.jpeg')
        label.setPixmap(pixmap)
        
        self.pushButton1 = QPushButton("Plot")

        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
    
        
        self.tabs.addTab(self.tab1,"Edit Architecture")
        self.tabs.addTab(self.tab2,"step response")
        self.tabs.addTab(self.tab3,"Bode Plot")
        self.tabs.addTab(self.tab4,"Rootlocus")
        
        self.tab1.layout = QVBoxLayout(self)        
        self.tab1.layout.addWidget(label)
        self.tab1.layout.addWidget(self.label1)
        self.tab1.layout.addWidget(self.plant_edit)
        self.tab1.layout.addWidget(self.label2)
        self.tab1.layout.addWidget(self.controller_edit)
        self.tab1.layout.addWidget(self.label3)
        self.tab1.layout.addWidget(self.feedback_edit)
        self.tab1.layout.addWidget(self.label7)
        self.tab1.layout.addWidget(self.input_edit)
        self.tab1.layout.addWidget(self.pushButton1)
        
        self.tab1.setLayout(self.tab1.layout)
        
               
        self.tab2.layout = QGridLayout(self)
        self.tab2.layout.addWidget(self.plot1,1,0,4,4)
#        self.tab2.layout.addWidget(combo)
        self.tab2.layout.addWidget(self.label8,5,0)  
        self.tab2.layout.addWidget(self.label4,6,0)
        self.tab2.layout.addWidget(self.os_edit,6,1)
        self.tab2.layout.addWidget(self.label5,7,0)
        self.tab2.layout.addWidget(self.ts_edit,7,1)
        self.tab2.layout.addWidget(self.label6,8,0)
        self.tab2.layout.addWidget(self.tr_edit,8,1)
        
        self.tab2.layout.addWidget(self.label9,5,2)
        self.tab2.layout.addWidget(self.label4n,6,2)
        self.tab2.layout.addWidget(self.os_editn,6,3)
        self.tab2.layout.addWidget(self.label5n,7,2)
        self.tab2.layout.addWidget(self.ts_editn,7,3)
        self.tab2.layout.addWidget(self.label6n,8,2)
        self.tab2.layout.addWidget(self.tr_editn,8,3)
        
        
        
        
        self.tab2.setLayout(self.tab2.layout)
        
        
        self.tab3.layout = QGridLayout(self)
        self.tab3.layout.addWidget(self.plot2,1,0,4,4)
#        self.tab2.layout.addWidget(combo)
        self.tab3.layout.addWidget(self.label10,5,0)  
        self.tab3.layout.addWidget(self.label12,6,0)
        self.tab3.layout.addWidget(self.gm_edit,6,1)
        self.tab3.layout.addWidget(self.label13,7,0)
        self.tab3.layout.addWidget(self.pm_edit,7,1)
        self.tab3.layout.addWidget(self.label14,8,0)
        self.tab3.layout.addWidget(self.gc_edit,8,1)
        self.tab3.layout.addWidget(self.label15,9,0)
        self.tab3.layout.addWidget(self.pc_edit,9,1)
        
        
        self.tab3.setLayout(self.tab3.layout)
        
        
        
        self.tab4.layout = QGridLayout(self)
#        self.tab2.layout.addWidget(combo)
        self.tab4.layout.addWidget(self.label16,5,0)  
        self.tab4.layout.addWidget(self.tf1_edit,6,0,2,0)
        self.tab4.layout.addWidget(self.label18,8,0)  
        self.tab4.layout.addWidget(self.opo_edit,9,0,2,0)
        self.tab4.layout.addWidget(self.label19,11,0)
        self.tab4.layout.addWidget(self.oze_edit,12,0,2,0)
        
        self.tab4.layout.addWidget(self.label17,5,2)  
        self.tab4.layout.addWidget(self.tf2_edit,6,2,2,2)
        self.tab4.layout.addWidget(self.label20,8,2)  
        self.tab4.layout.addWidget(self.cpo_edit,9,2,2,2)
        self.tab4.layout.addWidget(self.label21,11,2)
        self.tab4.layout.addWidget(self.cze_edit,12,2,2,2)

        
        
        self.tab4.setLayout(self.tab4.layout)
        
        

        
#        combo.currentIndexChanged[str].connect(self.updateUi)
#        combo.activated[str].connect(self.updateUi)
        
        
        # signals + slots ()
#        self.edit1.returnPressed.connect(self.update)
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.tabs)
#        layout.addWidget(self.plot)
#        layout.addWidget(self.label1)
#        layout.addWidget(self.parameter_edit)
#        layout.addWidget(self.label2)         
#        layout.addWidget(combo)  
#        layout.addWidget(self.label3)
#        layout.addWidget(self.output_edit) 
        
        self.widget.setLayout(layout)        
        self.setCentralWidget(self.widget) 
        
        self.pushButton1.clicked.connect(self.updateUi)

        
        self.setWindowTitle("Control System Manipulation Tool")
        self.x = None
        self.f = None
        self.str = None
        self.outstring = None
        

    def saveas(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        print(fileName)

        if not fileName.endswith(".txt"):
            fileName += ".txt"
        print(fileName)
        if fileName:
            print(fileName)     
            
#        file = open(filename,'w')
#        text = self.parameter_edit.toPlainText()
#        file.write(text)
#        file.close()
        
        with open(fileName, 'w') as f:
            text = str(self.outstring)
            f.write(text)
            
    def about(self):
        QMessageBox.about(self, 
            "About Control System Manipulation Tool",
            """<b>Control System Manipulation Tool</b>
               <p>Copyright &copy; 2017 Sanzida Hossain, All Rights Reserved.
               <p>Python %s -- Qt %s -- PyQt %s on %s""" %
            (platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))


    
    def updateUi(self) :
    #try : 
#        self.str = text
#        self.widg.setText(text)
        self.x = str(self.plant_edit.text())
        self.y = str(self.controller_edit.text())
        self.f = str(self.feedback_edit.text())
        self.inp = str(self.input_edit.text())
        g = eval(self.x) 
        
        f = eval(self.f) 
        inp = eval(self.inp)
        c = 1
        if (self.y!="tf([],[])")   :
            c = eval(self.y)
#        if len(x) > 1 :
#            x = np.array(x)
#        # Is there a cleaner way?
#        
#        f = eval(str(self.str))
        
#        
#        self.f = str(f)
#        self.f = self.f.replace("[","").replace("]","")
#        self.f = ",".join(self.f.split())
#        self.output_edit.setText(self.f)
        t, s = control.step_response(g)
        os = ((s.max()/s[-1]-1)*100)
        ts = (t[next(len(s)-i for i in range(2,len(s)-1) if abs(s[-i]/s[-1])>1.02)]-t[0])
        tr = (t[next(i for i in range(0,len(s)-1) if s[i]>s[-1]*.90)]-t[0])
        
        self.os = str(os)
        self.ts = str(ts)
        self.tr = str(tr)
        
        self.os_edit.setText(self.os)
        self.ts_edit.setText(self.ts)
        self.tr_edit.setText(self.tr)
        tgc= c*g
        new = control.feedback(tgc,f,-1)
        final = inp*new
        t1,s1 = control.step_response(final)
        
        self.outstring = "Time(sec)    Amplitude \n"
        for i in range(len(t1)):
            self.outstring += "%0.3f    %0.3f \n"%(t1[i],s1[i])
            print (self.outstring)
        
        osn = ((s1.max()/s1[-1]-1)*100)
        tsn = (t1[next(len(s1)-i for i in range(2,len(s1)-1) if abs(s1[-i]/s1[-1])>1.02)]-t1[0])
        trn = (t1[next(i for i in range(0,len(s1)-1) if s1[i]>s1[-1]*.90)]-t1[0])
        
        y1 = control.margin(final)
        
        if y1[0] == None :
            gm = "None"
        else: 
            gm = 20* np.log10(y1[0])
        
        if y1[1] == None :
            pm = "None"
        else: 
            pm = -(360-y1[1])
        
        if y1[2] == None :
            gc = "None"
        else: 
            gc = y1[2]
        
        if y1[3] == None :
            pc = "None"
        else: 
            pc = y1[3]
        
        self.osn = str(osn)
        self.tsn = str(tsn)
        self.trn = str(trn)
        
        self.os_editn.setText(self.osn)
        self.ts_editn.setText(self.tsn)
        self.tr_editn.setText(self.trn)
        
        self.gm_edit.setText(str(gm))
        self.pm_edit.setText(str(pm))
        self.gc_edit.setText(str(gc))
        self.pc_edit.setText(str(pc))
        
        
        op = control.pole(g)
        oz = control.zero(g)
        cp = control.pole(final)
        cz = control.zero(final)
        
        if len(op)==0:
            op = "No poles"
        if len(oz)==0:
            oz = "No zero"
        if len(cp)==0:
            cp = "No poles"
        if len(cz)==0:
            cz = "No zeros"
        
            
        self.tf1_edit.setText(str(g))
        self.tf2_edit.setText(str(final))
        self.opo_edit.setText(str(op))
        self.oze_edit.setText(str(oz))
        self.cpo_edit.setText(str(cp))
        self.cze_edit.setText(str(cz))
#        
        
        
        
        self.plot1.redraw(t, s, t1, s1)
        mag,ph,om= control.bode(final,Plot=False)
        self.plot2.redraw( mag, ph, om)

        control.root_locus(final)
 
        
    
        

class MatplotlibCanvas1(FigureCanvas) :
    """ This is borrowed heavily from the matplotlib documentation;
        specifically, see:
        http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """
    def __init__(self):
        
        # Initialize the figure and axes
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        # Give it some default plot (if desired).  
        x = np.arange(0.0, 3.0, 0.01)
        y = x**2
        y1 = x**3
        self.axes.plot(x, y, x, y1)
        self.axes.set_xlabel('time(sec)')
        self.axes.set_ylabel('amplitude') 
#        self.axes.legend("Plant","Whole System")

        # Now do the initialization of the super class
        FigureCanvas.__init__(self, self.fig)
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
         
        
    def redraw(self, x, y, x1, y1) :
        """ Redraw the figure with new x and y values.
        """
        # clear the old image (axes.hold is deprecated)
        self.axes.clear()
        self.axes.set_xlabel('time(sec)')
        self.axes.set_ylabel('amplitude') 
        self.axes.plot(x, y, label ='Plant')
        self.axes.plot(x1, y1, label ='Whole System')
        self.axes.legend() 
        self.draw()    
        
        
class MatplotlibCanvas2(FigureCanvas) :
    """ This is borrowed heavily from the matplotlib documentation;
        specifically, see:
        http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """
    def __init__(self):
        
        # Initialize the figure and axes
        self.fig = Figure()
        self.axes1 = self.fig.add_subplot(211)
        self.axes2 = self.fig.add_subplot(212)
        # Give it some default plot (if desired).  
        x = np.arange(0.0, 3.0, 0.01)
        y = x**2
        y1 = x**3
        self.axes1.plot(x, y)
        self.axes1.set_xlabel('Frequency(rad/s)')
        self.axes1.set_ylabel('Magnitude(dB') 
        
        self.axes2.plot(x, y1)
        self.axes2.set_xlabel('Frequency(rad/s)')
        self.axes2.set_ylabel('Phase(deg)') 
#        self.axes.legend("Plant","Whole System")

        # Now do the initialization of the super class
        FigureCanvas.__init__(self, self.fig)
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
         
        
    def redraw(self, mag, ph, om) :
        """ Redraw the figure with new x and y values.
        """
        # clear the old image (axes.hold is deprecated)
        mag= 20* np.log10(mag)
        self.axes1.clear()
        self.axes2.clear()
        self.axes1.set_ylabel('Magnitude(dB') 

        self.axes2.set_xlabel('Frequency(rad/s)')
        self.axes2.set_ylabel('Phase(deg)') 
        self.axes1.semilogx(om, mag)
        self.axes2.semilogx(om, ph)   
        self.axes1.grid(True,which= "both",ls = "-")
        self.axes2.grid(True,which= "both",ls = "-")
        self.draw()

        
        
app = QApplication(sys.argv)
form3 = MainWindow3()
form3.show()


app.exec_()
