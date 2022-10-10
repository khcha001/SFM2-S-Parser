# -*- coding: utf-8 -*-
#https://github.com/shinyeoeun/RPA_Tools_pakage/blob/master/Scripts/LogParser/LINE_api_logParser.py
#https://hongku.tistory.com/338

import sys
from parse import *
from parse import compile

import sys
from PyQt5.QtWidgets import *

import time
now = time


'''
SFM2-S SPC 업로드 불합리에 대한 현장 설비 집중성 파악
'''

'''
[LOG SAMPLE]
2022/09/03 04:18:28.703 eMEC_PBI_START
2022/09/03 04:18:29.531 RESULT - PcbSerial : 000000, Head[06] -< Cycle : 0055, Block : 01, Array : 005, X : 3.295(um), Y : -3.580(um), R : 0.0528(deg), Score : 0000 >


'''
 
 #CSV 추출 용 헤더
def get_csv_header():
    return "DATE,TIME,PCBID,HEAD,CYCLE,BLOCK,ARRAY,X(um),Y(um),R(deg),Score"


#로그 파싱
def parse(line):

    # LOG에서 추출하고자 하는 값이 포함된 문자열 존재여부 확인. 
    if line.find("RESULT") == -1:
        return

    # LOG 표시시각 취득
    date = line[0:10]
    time = line[12:23]
    print(time)

   
    # 추출대상 값들을 Parser의 {:w}로 파싱 > 각 값들은 배열로 반환됨
  
    result = search("PcbSerial : {}, Head[{}] -< Cycle : {}, Block : {}, Array : {}, X : {}(um), Y : {}(um), R : {}(deg), Score : {}", line)
    

    # 파싱결과값들을 CSV형식으로 편집
    if result: 
        
        data = str(date) + ',' + str(time) + ',' + str(result[0]) + ',' + str(result[1]) + ',' + str(result[2]) + ',' + str(result[3]) + ',' + str(result[4]) + ',' + str(result[5]) + ',' + str(result[6]) + ',' + str(result[7]) + ',' + str(result[8]) + "\n"
        return data

    # 파싱에 실패한 라인 출력
   
    print("Error >> ".format(line))
    return

def write_csv(input_file, output_file):
    # csv파일 작성
    csv_name = output_file
    csv = open(csv_name, 'w', encoding='utf-8')

    # csv 헤더 작성
    csv_head = get_csv_header() + "\n"
    csv.write(csv_head)

    # 로그파일 파싱 및 csv파일에 기록
    with open(input_file, 'r', encoding='utf-8') as log:

        while True:
            # 로그 라인 존재여부 확인
            line = log.readline()
            if not line: break

            # 해당 라인에 파싱 키워드 존재여부 확인
            csv_data = parse(line)
            if csv_data:

                while True:
                    line = log.readline()
                    if not line: break

                    # csv 기록
                    value = parse(line)
                    if value:
                        csv_data += value
                        print(csv_data)
                        csv.write(csv_data)
                        break

    csv.close()
    print('    ====== End ======')
    print('    >> Intput={}'.format(input_file))
    print('    >> Outputs={}'.format(csv_name))
    return


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
 
    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle('SFM2-S PBI Log Parser')
 
        self.pushButton = QPushButton('Please PBI Log Open')
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()
        self.label2 = QLabel() 
 
        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)

        self.setLayout(layout)
 
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self, "SFM2-S Log 파일을 열어주세요",'D:')
        #fname=QFileDialog.getOpenFileName(self,"FIS Log 파일을 열어주세요",'D:/ubuntu/disks','Text File(*.txt);; PPtx file(*ppt *pptx)' )
        outputpath = QFileDialog. getExistingDirectory(self,"파싱 결과를 저장할 위치 골라주세요")
        
        add_csv = "/"+now.strftime('%m%d %H%M%S')+"_result.csv"
        outputpath = outputpath + add_csv
        write_csv(fname[0], outputpath)
       
        self.label.setText("불러온 Log 입니다. :"+fname[0])
        self.label2.setText("파싱 결과 저장한 위치입니다. :"+outputpath)
 
if __name__=='__main__':

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
    
