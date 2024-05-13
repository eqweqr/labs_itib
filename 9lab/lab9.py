import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QGraphicsView
import sys
# from functools import 

class K_Mean:
     # Евклидова и Манхеттена метрики
    @staticmethod
    def evclid_metrics(dot, center):
        return ((dot[0]-center[0])**2+(dot[1]-center[1])**2)**0.5
        
    @staticmethod
    def manhetten_metrics(dot, center):
        return abs(dot[0]-center[0])+abs(dot[1]-center[1])
    
    method = 'E'

    def __init__(self, dots, centers):
        self.cluster_centers = centers
        self.clusters = None
        self.dots = dots
        self.no_diff = False
        

    def clusterize(self):
        new_cluster = [[] for i in range(len(self.cluster_centers))]
        for dot in self.dots:
            r = []
            for center_dot in self.cluster_centers:
                if self.method == 'E':
                    r.append(self.evclid_metrics(center_dot, dot))
                else:
                    r.append(self.manhetten_metrics(center_dot, dot))
            index_cluster = r.index(min(r))
            new_cluster[index_cluster].append(dot)
        self.clusters = new_cluster


    def next_step(self):
        '''
        Метрики задаются след образом:
        E == евклидова метрика
        M == метрика манхеттена
        '''

        new_clusters = [[] for _ in range(len(self.cluster_centers))]   

        for dot in self.dots:
            r = []
            for center_dot in self.cluster_centers:
                if self.method == 'E':
                    r.append(self.evclid_metrics(center_dot, dot))
                else:
                    r.append(self.manhetten_metrics(center_dot, dot))
            index_cluster = r.index(min(r))
            new_clusters[index_cluster].append(dot)
        
        new_cluster_centers = [0]*len(self.cluster_centers)
        i = 0
        for new_cluster in new_clusters:
            
            if len(new_cluster) == 0:
                new_cluster_centers[i]=self.cluster_centers[i]
            else:
                new_x = sum(map(lambda dot: dot[0], new_cluster))/len(new_cluster)
                new_y = sum(map(lambda dot: dot[1], new_cluster))/len(new_cluster)
                new_cluster_centers[i] = (int(new_x), int(new_y))

            i+=1

        for i in range(len(self.cluster_centers)):
            if abs(self.cluster_centers[i][0] - new_cluster_centers[i][0])>1\
                and abs(self.cluster_centers[i][1]-new_cluster_centers[i][1])>1:
                continue
            else:
                self.no_diff = True 
        
        self.clusters = new_clusters
        self.cluster_centers = new_cluster_centers


class Ui_Form(object):
        # evclidButton = True
        # evclidButtonClicked = True

        def __init__(self, obj):
            super().__init__()
            self.setupUi(obj)
            self.retranslateUi(obj)
            self.graphicsView = QGraphicsView(obj)
            self.graphicsView.setGeometry(QtCore.QRect(10, 10, 500, 500))
            self.graphicsView.setObjectName("graphicsView")
            self.scene = QtWidgets.QGraphicsScene()
            self.graphicsView.setScene(self.scene)
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
            for i in range(-248, 248):
                r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
                r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
            self.scene.addRect(r1, pen)
            self.scene.addRect(r2, pen)
            self.alghorithm = K_Mean([], [])

        def setupUi(self, Form):
            Form.setObjectName("Form")
            self.evclidButton = QPushButton(Form)
            self.evclidButton.clicked.connect(self.evclidButtonClicked)
            self.evclidButton.setGeometry(QtCore.QRect(560, 10, 211, 41))
            self.evclidButton.setObjectName("EvclidButtton")

            self.manhatButton = QPushButton(Form)
            self.manhatButton.clicked.connect(self.manhatButtonClicked)
            self.manhatButton.setGeometry(QtCore.QRect(560, 60, 211, 41))
            self.manhatButton.setObjectName("manhatButton")

            self.stepButton = QPushButton(Form)
            self.stepButton.clicked.connect(self.stepButtonClicked)
            self.stepButton.setGeometry(QtCore.QRect(560, 110, 211, 41))
            self.stepButton.setObjectName("stepButton")
            self.stepButton.setEnabled(False)
            
            self.resetButton = QPushButton(Form)
            self.resetButton.clicked.connect(self.resetButtonClicked)
            self.resetButton.setGeometry(QtCore.QRect(560, 160, 211, 41))
            self.resetButton.setObjectName("resetButton")
            
            self.cordsTextBox = QtWidgets.QPlainTextEdit(Form)
            self.cordsTextBox.setGeometry(QtCore.QRect(560, 230, 211, 71))
            self.cordsTextBox.setObjectName("cordsTextBox")
            
            self.cordsButton = QPushButton(Form)
            self.cordsButton.clicked.connect(self.cordsButtonClicked)
            self.cordsButton.setGeometry(QtCore.QRect(560, 310, 211, 31))
            self.cordsButton.setObjectName("cordsButton")
            
            self.label = QtWidgets.QLabel(Form)
            self.label.setGeometry(QtCore.QRect(560, 210, 200, 21))
            self.label.setObjectName("label")
            
            self.centersTextBox = QtWidgets.QPlainTextEdit(Form)
            self.centersTextBox.setGeometry(QtCore.QRect(560, 380, 211, 71))
            self.centersTextBox.setObjectName("centersTextBox")
            
            self.centersButton = QPushButton(Form)
            self.centersButton.clicked.connect(self.centersButtonClicked)
            self.centersButton.setGeometry(QtCore.QRect(560, 460, 211, 31))
            self.centersButton.setObjectName("centersButton")

            self.label_2 = QtWidgets.QLabel(Form)
            self.label_2.setGeometry(QtCore.QRect(560, 350, 200, 21))
            self.label_2.setObjectName("label_2")
            
            self.retranslateUi(Form)
            QtCore.QMetaObject.connectSlotsByName(Form)

        def retranslateUi(self, Form):
            _translate = QtCore.QCoreApplication.translate
            Form.setWindowTitle(_translate("Form", "Form"))
            self.evclidButton.setText(_translate("Form", "Евклид"))
            self.stepButton.setText(_translate("Form", "Шаг"))
            self.manhatButton.setText(_translate("Form", "Манхэттен"))
            self.resetButton.setText(_translate("Form", "RESET"))
            self.cordsButton.setText(_translate("Form", "Add cords"))
            self.label.setText(_translate("Form", "Format: (x1, y1);(x2, y2);(x3, y3);..."))
            self.centersButton.setText(_translate("Form", "Add Centers"))
            self.label_2.setText(_translate("Form", "Format: (x1, y1);(x2, y2);(x3, y3);..."))

        def addCordsToGraph(self, cords, f):
            pen = None
            brush = None
            if f == 'm':
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
                brush = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
            else:
                pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
                brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
            side = 3
            for i in cords:
                self.scene.addEllipse(i[0] * side - 3, -1* i[1] * side - 3, 7, 7, pen, brush)

        def parseStringToCords(self, s, tb):
            cords_l = None
            try:
                cords_string_array = s.split(';')
                cords_l = []
                for i in cords_string_array:
                    l = [int(k) for k in i.strip('()').split(',')]
                    cords_l.append(l)
            except:
                if tb == 'c':
                    self.cordsTextBox.clear()
                else:
                    self.centersTextBox.clear()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Format Error")
                msg.setInformativeText('Follow the format!')
                msg.setWindowTitle("Error")
                msg.setStyleSheet("QLabel{font-size: 20px;}")
                msg.exec_()
                pass
            return cords_l

        def cordsButtonClicked(self):
            cords = self.cordsTextBox.toPlainText()
            cords_list = self.parseStringToCords(cords, 'c')
            print(cords_list)
            if cords_list is not None:
                self.alghorithm.dots = cords_list.copy()
                self.addCordsToGraph(cords_list, 'm')

        def drawLineToDot(self):
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
            brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
            pen.setWidth(2)
            pen.setColor(QtCore.Qt.GlobalColor.green)
            for i in range(len(self.alghorithm.cluster_centers)):
                for dot_in_cluster in self.alghorithm.clusters[i]:
                    self.scene.addLine(QtCore.QLineF(3* dot_in_cluster[0], -3* dot_in_cluster[1], 3*self.alghorithm.cluster_centers[i][0], -
                        3*self.alghorithm.cluster_centers[i][1]), pen)        

        def centersButtonClicked(self):
            cords = self.centersTextBox.toPlainText()
            cords_list = self.parseStringToCords(cords, 'm')
            if cords_list is not None:
                self.alghorithm.cluster_centers = cords_list.copy()
                print (cords_list)
                self.addCordsToGraph(cords_list, 'c')

        def evclidButtonClicked(self):
            if self.alghorithm.dots is None or self.alghorithm.cluster_centers is None:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Empty Error")
                msg.setInformativeText('Not enough dots!')
                msg.setWindowTitle("Error")
                msg.setStyleSheet("QLabel{font-size: 20px;}")
                msg.exec_()
                return
            self.alghorithm.method = 'E'
            self.alghorithm.clusterize()
            # self.drawLineToDot()
            self.evclidButton.setEnabled(False)
            self.manhatButton.setEnabled(False)
            self.cordsButton.setEnabled(False)
            self.centersButton.setEnabled(False)
            self.stepButton.setEnabled(True)

        def manhatButtonClicked(self):
            if self.alghorithm.dots is None or self.alghorithm.cluster_centers is None:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Empty Error")
                msg.setInformativeText('Not enough dots!')
                msg.setWindowTitle("Error")
                msg.setStyleSheet("QLabel{font-size: 20px;}")
                msg.exec_()
                return
            self.alghorithm.method = 'M'
            self.alghorithm.clusterize()
            # self.drawLineToDot()
            self.evclidButton.setEnabled(False)
            self.manhatButton.setEnabled(False)
            self.cordsButton.setEnabled(False)
            self.centersButton.setEnabled(False)
            self.stepButton.setEnabled(True)


        def stepButtonClicked(self):
            if self.alghorithm.dots is None or self.alghorithm.cluster_centers is None:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Empty Error")
                msg.setInformativeText('Not enough dots!')
                msg.setWindowTitle("Error")
                msg.setStyleSheet("QLabel{font-size: 20px;}")
                msg.exec_()
                return
            self.alghorithm.next_step()
            self.redrow(False)
            print(self.alghorithm.cluster_centers)
            self.addCordsToGraph(self.alghorithm.cluster_centers, 'r')
            self.drawLineToDot()
            
            # если больше не меняется классы, то выполняется это
            if self.alghorithm.no_diff:
                self.stepButton.setEnabled(False)
                self.stepButton.clearFocus()

        def resetButtonClicked(self):
            self.evclidButton.setEnabled(True)
            self.manhatButton.setEnabled(True)
            self.cordsButton.setEnabled(True)
            self.centersButton.setEnabled(True)
            self.stepButton.setEnabled(True)
            self.redrow(True)
            self.alghorithm = K_Mean([], [])

        def redrow(self, full):
            self.scene.clear()
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
            for i in range(-248, 248):
                r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
                r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
                self.scene.addRect(r1, pen)
                self.scene.addRect(r2, pen)
            if not full:
                pen2 = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
                brush2 = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
                
                side = 3
                for i in self.alghorithm.dots:
                    self.scene.addEllipse(i[0] * side - 3, -1 * i[1] * side - 3, 7, 7, pen2, brush2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    app2 = Ui_Form(widget)
    widget.setWindowTitle("Network")
    widget.setFixedWidth(795)
    widget.setFixedHeight(520)
    widget.show()
    exit(app.exec_())
    # dots = [(143, 213);(180, 220);(183, 249);(271, 253);(226, 253);(315, 275);(266, 297)]
    
    # centers = [(159, 238);(270, 189)]

    # k_m = K_Mean(dots, centers)
    # while not k_m.no_diff:
    #     k_m.next_step()
    #     print(k_m.cluster_centers)
