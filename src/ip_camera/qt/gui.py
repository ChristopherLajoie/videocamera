import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class RTSPPlayer(QWidget):
    def __init__(self):
        super().__init__()
    
    def startRTSPPlayer(self, ip_list):
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()  

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)  
        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget) 
        if not ip_list:
            rtsp_url = "rtmp://192.168.226.1/live/test" 
            self.mediaPlayer.setMedia(QMediaContent(QUrl(rtsp_url)))
            self.mediaPlayer.play()
            self.show()  
        else:
            rtsp_url = f"rtsp://192.168.144.{ip_list[1]}:8554/main.264"
            self.mediaPlayer.setMedia(QMediaContent(QUrl(rtsp_url)))
            self.mediaPlayer.play()
            self.show()  

class IPInputDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.rtspPlayer = RTSPPlayer()
        self.inputFields = {}

        layout = QVBoxLayout()
        for i in range(4):
            label = QLabel(f"Camera IP")
            lineEdit = QLineEdit()
            lineEdit.setMaxLength(3)  
            self.inputFields[i] = lineEdit
            layout.addWidget(label)
            layout.addWidget(lineEdit)

        confirmButton = QPushButton("Confirm")
        confirmButton.clicked.connect(self.confirmClicked)
        layout.addWidget(confirmButton)

        self.setLayout(layout)
        self.setWindowTitle("Login")

    def confirmClicked(self):
        ip_list = []
        for i in range(4):
            input_text = self.inputFields[i].text()
            if input_text:  
                try:
                    ip_part = int(input_text)
                    ip_list.append(ip_part)
                except ValueError:
                    pass  
            else:
                pass 

        self.rtspPlayer.startRTSPPlayer(ip_list)
        self.close() 


if __name__ == '__main__':
    app = QApplication(sys.argv)

    inputDialog = IPInputDialog()

    inputDialog.show()

    sys.exit(app.exec_())
