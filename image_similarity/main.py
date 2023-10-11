from re import L
import sys
# pip install PyQt6
import cv2
import numpy as np
from PyQt6 import QtGui,QtWidgets,QtCore
from PyQt6.QtCore import QThread, pyqtSignal, Qt,QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow,QListWidgetItem
from facerec_ipcamera_knn import *
from mainUI import Ui_MainWindow
from model.employee_history import *
from controller.employee_history_controller import *
from helpers.common import *
import os
from model.camera import *;
import threading
from popup import Ui_PopupWindow
import urllib
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel
)
import requests
import os, sys

class Static:
    idCameraSelected = 1;
class MainWindow(QMainWindow):
    thisdict = {
      
    }
    t1 = None; 
    cameras = [Camera('rtsp://admin:kido1234@10.20.65.154/onvif1',1,"CAMERA OUT", True) 
            #    , Camera('rtsp://admin:kido1234@10.20.65.154/onvif1',2,"CAMERA CHECK OUT", True) 
            ]
    datetimeCurrent = datetime.now();
    def __init__(self):
        super().__init__()
        self.loadDefault();
        self.loadData();
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.btnOut.clicked.connect(self.onClickedButtonOut)
        self.uic.btnIn.clicked.connect(self.onClickedButtonIn)
        self.uic.btnIn.setStyleSheet("background-color: gray")
        self.uic.btnOut.setStyleSheet("background-color: white")
        self.w = None  # No external window yet.

        self.thread = {}
        self.start_capture_video();
        self.loadUI();
        self.t1 = threading.Thread(target=self.asyncData);
        self.t1.start();
        self.uic.listWidget.itemClicked.connect(self.Clicked)
        # self.updateUI();
     
    def loadUI(self):
        self.uic.listWidget.clear();
        for key in self.thisdict:
            inOut = self.thisdict[key];
            self.addItemToList(inOut);
            # self.uic.listWidget.setModel()
            
    def Clicked(self,item):
        widget : QtWidgets.QWidget = self.uic.listWidget.itemWidget(item);
        label : QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "label")
        key = label.text();
        inOut = self.thisdict[key];
        url_image = inOut.image
        if self.w is None:
            MainWindow = QtWidgets.QMainWindow()           
            self.w = Ui_PopupWindow()
            self.w.setupUi(MainWindow)
        else:
            self.w.hide();
        image = QPixmap()
        if "http" not in url_image: 
            image = url_image;
        else:
            image.loadFromData(requests.get(url_image).content) 
        print('item',url_image); 
        self.w.label.setPixmap(QtGui.QPixmap(image))
        self.w.show()

        # ui.setupUi(self);
        # ui.show();
        # data = urllib.urlopen(image).read()
        # pixmap = QPixmap()
        # pixmap.loadFromData(data)

    def onClickedButtonIn(self):
        print('onClickedButtonIn');
        Static.idCameraSelected = 1;
        self.uic.btnIn.setStyleSheet("background-color: gray")
        self.uic.btnOut.setStyleSheet("background-color: white")
        #self.uic.btnIn.setStyleSheet()
    def onClickedButtonOut(self):
        print('onClickedButtonOut');
        Static.idCameraSelected = 2;  
        self.uic.btnIn.setStyleSheet("background-color: white")
        self.uic.btnOut.setStyleSheet("background-color: gray")
    def loadData(self):
        controller = EmployeeHistoryController();
        self.thisdict =  controller.getInOutEmployee();
    
    def loadDefault(self):
        controller = EmployeeHistoryController();
        # controller.delete();
        controller.updateEmployeeHistoryDictionary();
        
    def asyncData(self):

        controller = EmployeeHistoryController();
        # controller.delete();
        controller.asyncImage();
        controller.asyncServer();

    def reload(self):
        self.loadData();
        self.loadUI();
        
    def printInOut(self):
        for key in self.thisdict:
            print('print InOUT',self.thisdict[key])
    def updateDataAndUI(self,inOut,isCheckIn):
        print('updateDataAndUI');
        # check if past day => reload data daily;
        datetimeNow = datetime.now();
        if(self.compareDateTimeByDay(datetimeNow,self.datetimeCurrent)):
            self.loadDefault();
            self.reload();
            self.datetimeCurrent = datetimeNow;
            return;
        inOutCurrent = self.thisdict.get(inOut.id);
        # if inOutCurrent:
        #     print('inOutCurrent IIII',inOutCurrent);
        if inOutCurrent == None:
            inOutCurrent = inOut;
            self.thisdict[inOut.id] = inOutCurrent;
            self.addItemToList(inOutCurrent);
        else:
            if isCheckIn:
                inOutCurrent.inDate = inOut.inDate;
            else:
                inOutCurrent.outDate = inOut.outDate;
            inOutCurrent.image = inOut.image;
            self.thisdict[inOut.id] = inOutCurrent;
            self.updateListWidget(inOutCurrent)

        # if inOutCurrent:
        #     print('inOutCurrent IIII',inOutCurrent);
        # self.printInOut();
        
    def getIndexFromDict(self,id): 
        index: int = 0;
        for key in self.thisdict:
              if key == id:
                  return index;
              index = index +1;
        return -1;
    def addItemToList(self,inOut):
        self.newItem = QListWidgetItem();
            # self.newItem.setToolTip();
        self.newItem.setSizeHint(QSize(0,130))

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(530, 0))
        self.frame.setMaximumSize(QtCore.QSize(530, 551))
        self.frame.setStyleSheet("QFrame {\n"
    "    background-color: white; \n"
    "    border-radius : 10\n"
    "}")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_3.setStyleSheet("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_2 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_2.setGeometry(QtCore.QRect(0, 10, 91, 81))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.imageAvatar = QtWidgets.QLabel(parent=self.frame_2)
        self.imageAvatar.setGeometry(QtCore.QRect(13, 3, 65, 71))
        self.imageAvatar.setStyleSheet("")
        self.imageAvatar.setText("")
        self.imageAvatar.setPixmap(QtGui.QPixmap("image_similarity/assets/avatar/{0}".format(inOut.id)))
        self.imageAvatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageAvatar.setObjectName("imageAvatar")
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(180, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label = QtWidgets.QLabel(parent=self.frame_4)
        self.label.setGeometry(QtCore.QRect(10, 20, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.lblCode = QtWidgets.QLabel(parent=self.frame_4)
        self.lblCode.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.lblCode.setStyleSheet("")
        self.lblCode.setObjectName("lblCode")
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(parent=self.frame)
        self.frame_5.setStyleSheet("")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setLineWidth(0)
        self.frame_5.setObjectName("frame_5")
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_5)
        self.frame_7.setGeometry(QtCore.QRect(0, 20, 111, 51))
        self.frame_7.setAutoFillBackground(False)
        self.frame_7.setStyleSheet("QFrame {\n"
    "    border-radius: 23;    \n"
    "    background-color: green; \n"
    "    color : white\n"
    "}")
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.label_6 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_6.setGeometry(QtCore.QRect(80, 10, 21, 31))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("tickCircle.png"))
        self.label_6.setObjectName("label_6")
        self.checkInTime = QtWidgets.QLabel(parent=self.frame_7)
        self.checkInTime.setGeometry(QtCore.QRect(20, 10, 54, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.checkInTime.setFont(font)
        self.checkInTime.setStyleSheet("")
        self.checkInTime.setObjectName("checkInTime")
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame)
        self.frame_6.setStyleSheet("")
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.frame_6.setObjectName("frame_6")
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_8.setGeometry(QtCore.QRect(0, 20, 111, 51))
        self.frame_8.setAutoFillBackground(False)
            
            
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.checkOutTime = QtWidgets.QLabel(parent=self.frame_8)
        self.checkOutTime.setGeometry(QtCore.QRect(20, 10, 60, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.checkOutTime.setFont(font)
        self.checkOutTime.setStyleSheet("")
        self.checkOutTime.setObjectName("checkOutTime")
        self.label_7 = QtWidgets.QLabel(parent=self.frame_8)
        self.label_7.setGeometry(QtCore.QRect(80, 10, 21, 31))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("tickCircle.png"))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame)
        
        _translate = QtCore.QCoreApplication.translate
        inDateStr = '--:--'
        # inColor = 'gray'
        if  inOut.inDate:
            inDateStr  = datetime.strftime(inOut.inDate,'%H:%M')            
            self.frame_7.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: green; \n"
                    "    color : white\n"
                    "}")
        else:
            self.frame_7.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: gray; \n"
                    "    color : white\n"
                    "}")
        outDateStr = '--:--'
        if  inOut.outDate:
            outDateStr = datetime.strftime(inOut.outDate,'%H:%M')
            self.frame_8.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: blue; \n"
                    "    color : white\n"
                    "}")
        else:
            self.frame_8.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: gray; \n"
                    "    color : white\n"
                    "}")
        self.label.setText(_translate("MainWindow", inOut.name))
        self.lblCode.setText(_translate("MainWindow", "Mã NV: {0}".format(inOut.id)))
        self.checkInTime.setText(_translate("MainWindow", inDateStr))
        self.checkOutTime.setText(_translate("MainWindow", outDateStr))
            # self.label_7.show();
            
            
        self.uic.listWidget.insertItem(0,self.newItem);
            # self.log_in = QtWidgets.QWidget(self.centralwidget)
        self.uic.listWidget.setItemWidget(self.newItem, self.centralwidget);
    def updateListWidget(self,inOut):
        index = self.getIndexFromDict(inOut.id);
        if index == -1:
            return;
        listWidget = self.uic.listWidget;
        item : QtWidgets.QListWidgetItem= listWidget.item(index);
        widget : QtWidgets.QWidget = listWidget.itemWidget(item);
        checkInTime : QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "checkInTime")
        checkOutTime : QtWidgets.QLabel = widget.findChild(QtWidgets.QLabel, "checkOutTime")
        frame_8 : QtWidgets.QLabel = widget.findChild(QtWidgets.QFrame, "frame_8")
        frame_7 : QtWidgets.QLabel = widget.findChild(QtWidgets.QFrame, "frame_7")

        _translate = QtCore.QCoreApplication.translate
        inDateStr = '--:--' 
        if  inOut.inDate:
            inDateStr  = datetime.strftime(inOut.inDate,'%H:%M')            
            frame_7.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: green; \n"
                    "    color : white\n"
                    "}")
        else:
            frame_7.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: gray; \n"
                    "    color : white\n"
                    "}")
        outDateStr = '--:--'
        if inOut.outDate:
            outDateStr = datetime.strftime(inOut.outDate,'%H:%M')
            frame_8.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: blue; \n"
                    "    color : white\n"
                    "}")
        else:
            frame_8.setStyleSheet("QFrame {\n"
                    "    border-radius: 23;    \n"
                    "    background-color: gray; \n"
                    "    color : white\n"
                    "}")        
        checkInTime.setText(_translate("MainWindow", inDateStr))
        checkOutTime.setText(_translate("MainWindow", outDateStr))
        # print('updateData IIII',self.thisdict);
        # self.uic.Button_stop.clicked.connect(self.stop_capture_video)
    def start_capture_video(self):
        for camera in self.cameras:  
            id = camera.id;     
            self.thread[id] = capture_video(camera=camera)
            self.thread[id].start()
            self.thread[id].signal.connect(self.show_wedcam)
        self.thread[3] = capture_video_new(index = 3)
        self.thread[3].start()
        self.thread[3].signal.connect(self.show_wedcam_new)   
            
        
    def closeEvent(self, event):
        self.stop_capture_video()
    def stop_capture_video(self):
        self.thread[1].stop()
    
    def show_wedcam(self, tup):
        cv_img = tup[0];
        type = tup[1];
        isCheckIn = tup[2];
        id = tup[3];
        if type == 'image':
            if id != Static.idCameraSelected:
                return;
            qt_img = self.convert_cv_qt(cv_img)
            self.uic.label.setPixmap(qt_img)
        else:
            # print('cv_img',cv_img);
            # cv2.imwrite("frame${0}.jpg", cv_img)     # save frame as JPEG file      
            self.updateDataAndUI(cv_img,isCheckIn);
            
    def show_wedcam_new(self, tup):

        cv_img = tup[0];
        type = tup[1];
        isCheckIn = tup[2];
        if type == 'image':
            if Static.idCameraSelected != 2:
                return;
            qt_img = self.convert_cv_qt(cv_img)
            self.uic.label.setPixmap(qt_img)
        else:
            # print('cv_img',cv_img);
            # cv2.imwrite("frame${0}.jpg", cv_img)     # save frame as JPEG file      
            self.updateDataAndUI(cv_img,isCheckIn);

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line,QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(1400, 800, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def compareDateTimeByDay(self,firstDate : datetime,lastDate: datetime):
        return datetime(firstDate.year,firstDate.month,firstDate.day) > datetime(lastDate.year,lastDate.month,lastDate.day)
class capture_video(QThread):
    signal = pyqtSignal(tuple)
    camera : Camera
    def __init__(self, camera: Camera):
        self.camera = camera;
        # print("start threading", self.index)
        super(capture_video, self).__init__()
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    def run(self):
        print('url',self.camera.url );
        cap = None;
        if self.camera.url == '':
            cap = cv2.VideoCapture(0)  # 'D:/8.Record video/My Video.mp4'
        else:
            cap = cv2.VideoCapture(self.camera.url,cv2.CAP_FFMPEG)
        # url = 'rtsp://admin:kido1234@10.20.65.154/onvif1'
        print("Width: %d, Height: %d, FPS: %d" % (cap.get(3), cap.get(4), cap.get(5)))
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame from the camera.")
                continue  # Skip this iteration and try the next frame
            isCheckIn = self.camera.isCheckIn;
            id = self.camera.id;
            isSelected = Static.idCameraSelected == id;
            if isSelected == True:
                frame = convert_image(frame,isCheckIn,isSelected,self.signal.emit)
                tup = (frame, "image" , isCheckIn, id)
                self.signal.emit(tup)
            else:
                write_data(frame, isCheckIn,self.signal.emit)
               
                # tup = (frame, "image" , isCheckIn, id)
                # self.signal.emit(tup)
                # convert_image(frameNew,isCheckIn,isSelected,self.signal.emit)

    def stop(self):
        print("stop threading", self.camera.id)
        self.terminate()
class capture_video_new(QThread):
    signal = pyqtSignal(tuple)
    def __init__(self,index):
        # print("start threading", self.index)
        super(capture_video_new, self).__init__()
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    def run(self):
        cap = cv2.VideoCapture('rtsp://admin:kido1234@10.20.65.145/onvif1',cv2.CAP_FFMPEG)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame from the camera.")
                continue  # Skip this iteration and try the next frame
            if Static.idCameraSelected == 2:
                frame = convert_image(frame,False,True,self.signal.emit)
                tup = (frame, "image" , False, )
                self.signal.emit(tup)
            else:
                write_data(frame,False,self.signal.emit)
                # tup = (frame, "image" , True, 3)
                # self.signal.emit(tup)
    def stop(self):
        self.terminate()
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window 1 d")
        layout.addWidget(self.label)
        self.setLayout(layout)
if __name__ == "__main__":
    print("Training KNN classifier...")
    # classifier = train("knn_examples/train", model_save_path="trained_knn_model.clf", n_neighbors=2)
    print("Training complete!")
    # os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"
    app = QApplication(sys.argv)
    main_win = MainWindow()
    size = app.primaryScreen().size();
    print('size',size);
    main_win.setFixedSize(size);
    print('heigt',size.height())
    main_win.uic.label.setGeometry(QtCore.QRect(0, 0,size.width() - 650,size.height()-100))
    # MainWindow(size.width,size.height);
    main_win.show()
    app.exec()
