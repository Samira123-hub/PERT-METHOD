import sys
from PyQt5.QtGui import QPixmap
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView,QSizePolicy
from PyQt5.QtCore import Qt
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1900, 1000)
        self.setWindowTitle("La saisie des données")
        self.setStyleSheet("background-color:white;")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        headerLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        decoration1Label = QLabel(self)
        decoration1 = QPixmap("images/image2.jpg").scaled(250,250,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        decoration1Label.setPixmap(decoration1)
        decoration1Label.setScaledContents(True)
        decoration1Label.setFixedSize(250, 250)
        
        logo = QPixmap('images/logo.jpg').scaled(300,350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logoLabel = QLabel(self)
        logoLabel.setPixmap(logo)
        logoLabel.setAlignment(Qt.AlignCenter)
        logoLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)



        

        decoration2Label = QLabel(self)
        decoration2 = QPixmap("images/image1.jpg").scaled(250,250,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        decoration2Label.setPixmap(decoration2)
        decoration2Label.setScaledContents(True)
        decoration2Label.setFixedSize(250, 250)

        headerLayout.addWidget(decoration1Label)
        headerLayout.addStretch()  
        headerLayout.addWidget(logoLabel)
        headerLayout.addStretch() 
        headerLayout.addWidget(decoration2Label)

        mainLayout.addLayout(headerLayout)

        contentLayout = QHBoxLayout()
        formLayout = QFormLayout()
        self.taskInput = QLineEdit()
        self.durationInput = QLineEdit()
        self.precedingInput = QLineEdit()      
        formLayout.addRow("Tâche:", self.taskInput)
        formLayout.addRow("Durée:", self.durationInput)
        formLayout.addRow("Précédent:", self.precedingInput)
        submitButton = QPushButton("Terminer")
        submitButton.clicked.connect(self.add_to_table)
        formLayout.addRow(submitButton)

        formWidget = QWidget()
        formWidget.setLayout(formLayout)

        formWidget.setFixedWidth(600)   


        formWidget.setStyleSheet("""
            QWidget {
                font-size: 18px;
                background-color: #E4F4FC;
                padding: 10px;
                margin-top:50px;
                margin-left:10px;
                margin-bottom:30px;
                margin-right:40px;
                border-radius:10px;
            }
            QLineEdit {
                height: 30px;
                font-size: 16px;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                margin-bottom: 15px;
                min-width: 300px; 
                max-width: 350px;  
            }
            QLineEdit:hover {
                border: 2px solid black;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 10px;
                margin: 20px; 
                text-align:center;
                min-width: 80px; 
                max-width: 50px;   
                }
            QPushButton:hover {
                background-color: #45a049; 
            }
        """)

        contentLayout.addWidget(formWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Tâche", "Durée", "Précédent"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.tableWidget.verticalHeader().setVisible(False)
     

        self.tableWidget.setStyleSheet("""
            QTableWidget {
                font-size: 20px;
                font-weight: bold;
                background-color: #f9f9f9;
                border: none;
                padding: 15px;
                margin-bottom:30px;
                margin-top: 50px;
                margin-right: 10px; 
                border-left:20px;

            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-size: 20px;
                font-weight: bold;
                padding: 5px;
                border: 2px solid #ddd;
            }
        """)

        contentLayout.addWidget(self.tableWidget)

        mainLayout.addLayout(contentLayout)

        nextButton = QPushButton("Suivant")
        nextButton.setStyleSheet("""
                QPushButton {
                    background-color: #008CBA;
                    color: white;
                    font-size: 18px;
                    padding: 10px 20px;
                    border-radius: 10px;
                    transition: background-color 0.3s ease;
                    margin-bottom:50px;
                }
                QPushButton:hover {
                    background-color: #005f73; 
                }
            """)   
        nextButton.clicked.connect(self.open_second_window)
        mainLayout.addWidget(nextButton, alignment=Qt.AlignCenter)

    def add_to_table(self):
        task = self.taskInput.text()
        duration = self.durationInput.text()
        preceding = self.precedingInput.text()

        if task and duration:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(task))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(duration))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(preceding))

            self.taskInput.clear()
            self.durationInput.clear()
            self.precedingInput.clear()

            self.save_to_excel()
    def save_to_excel(self):
        rows = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                row_data.append(item.text() if item else "")
            rows.append(row_data)

        for row_data in rows:
            row_data.extend(["", "","","","","",""])  

        df = pd.DataFrame(rows, columns=["Tâche", "Durée", "Précédent", "ES" ,"LS" ,"EF" ,"LF", "Marge Totale","Marge Libre", "Tâche Critique"])

        try:
            df.to_excel("input.xlsx", index=False)
            print("Données enregistrées dans tableau_donnees.xlsx")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement dans le fichier Excel : {e}")


    def open_second_window(self):
        try:
            subprocess.run(["python", "resultatPert.py"], check=True)
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
        except Exception as e:
            print(f"Erreur lors de l'exécution de 'resulatPert.py' : {e}")



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


