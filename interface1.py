import subprocess
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QSizePolicy, QPushButton
)
import sys
from PyQt5.QtGui import QFont,  QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Introduction à la méthode PERT")
        self.setGeometry(0, 0, 1900, 1000)
        self.setStyleSheet("background-color:white;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

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

        top_layout.addWidget(decoration1Label)
        top_layout.addStretch()  
        top_layout.addWidget(logoLabel)
        top_layout.addStretch()  
        top_layout.addWidget(decoration2Label)


        top_widget = QWidget()
        top_widget.setFixedHeight(250)
        top_widget.setLayout(top_layout)
     
        layout.addWidget(top_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        button_text_container = QWidget()
        button_text_layout = QVBoxLayout(button_text_container) 
        button_text_layout.setContentsMargins(0, 0, 0, 0) 
        button_text_layout.setSpacing(10)  
        button_text_container.setFixedHeight(500)  
        self.text_labels = []
        labeles = ["Définition et historique de la méthode PERT",
                    "Le But de Program Evaluation and Review Technique", 
                    "Projets Emblématiques ayant Bénéficié de la Méthode PERT"]
        textes = [
            " Le PERT (Program Evaluation and Review Technique) est une méthode de gestion de projet créée en 1957\npar la marine américaine  pour le programme Polaris. Elle permet de planifier, coordonner et suivre des \nprojets complexes en identifiant les tâches et leurs dépendances. En utilisant des estimations de temps\n optimistes, pessimistes et probables, PERT calcule les durées moyennes pour chaque tâche. L'objectif \nest de déterminer le chemin critique et d'optimiser l'exécution du projet.",
            "Le but du PERT est de faciliter la gestion des projets complexes en planifiant et en coordonnant  \nles différentes tâches nécessaires à leur réalisation. Il aide à estimer les durées, à identifier le chemin \n critique et à minimiser les risques de retards. Cette méthode optimise l'utilisation des ressources\n et améliore la visibilité sur les dépendances entre tâches. Elle permet ainsi de respecter les délais \ntout en maîtrisant les contraintes du projet.",
            "Le PERT a été utilisé pour plusieurs projets majeurs, notamment le programme Polaris de la marine\naméricaine pour développer des missiles balistiques.La NASA l’a également employé pour planifier \nles missions Apollo, y compris Apollo 11, le premier atterrissage sur la Lune. Disney a appliqué PERT pour \nla construction du parc Disney World en Floride, assurant le respect des délais. Il a aussi été utilisé dans \ndes projets industriels complexes, comme le développement des avions Boeing et dans des projets\n d'infrastructures majeures."
        ]
        for i in range(3):
            button = QPushButton(labeles[i])
            button.setFixedWidth(1300)
            button.setFixedHeight(60)
            button.setStyleSheet(""" 
                QPushButton {
                    background-color: #008CBA;
                    color: white;
                    font-size: 20px; 
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 10px;
                    transition:background-color 5s ease;
                }
                QPushButton::hover{
                    background-color: #5571d9;
                }
            """)

            horizontal_layout = QHBoxLayout()
            horizontal_layout.addWidget(button)
            text_label = QLabel(textes[i])
            text_label.setFont(QFont("Arial", 9))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFixedWidth(1300)
            text_label.setVisible(False)
            self.text_labels.append(text_label)

            text_label.setStyleSheet(""" 
                QLabel {
                    background-color:#f0f0f0; 
                    font-size: 10px;
                    padding: 10px; 
                    border-radius: 10px;
                    width: 0px;
                }
            """)

            text_label.state = 0
            button.clicked.connect(lambda cheked, btn=button, lbl=text_label: self.show_text(btn, lbl))

            button_text_layout.addLayout(horizontal_layout)
            button_text_layout.addWidget(text_label, alignment=Qt.AlignCenter | Qt.AlignTop)

        layout.addWidget(button_text_container, alignment=Qt.AlignCenter | Qt.AlignTop)
        bottom_layout = QHBoxLayout()

        oval_button = QPushButton("Suivant")
        
        oval_button.setStyleSheet("""
                QPushButton {
                    background-color: #008CBA;
                    color: white;
                    font-size: 18px;
                    margin-right:auto;
                    margin-left:auto;
                    padding: 10px 20px;
                    border-radius: 10px;
                    transition: background-color 0.3s ease;
                    margin-bottom:50px;
                }
                QPushButton:hover {
                    background-color: #005f73; 
                    margin-right:auto;
                    margin-left:auto;
                }
            """)
        oval_button.clicked.connect(self.open_second_window) 
        bottom_layout.setContentsMargins(800, 10, 10, 10)
        bottom_layout.addWidget(oval_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

        layout.addLayout(bottom_layout)

        central_widget.setLayout(layout)

    def show_text(self, button, label):
        for text_label in self.text_labels:
            if text_label != label:
                text_label.setVisible(False)
        if label.state == 0:
            label.setFont(QFont("Arial", 20, QFont.Normal))
            label.setStyleSheet(""" 
                QLabel {
                    background-color:#f0f0f0; 
                    font-size: 20px;
                        
                    padding: 10px 5px;
                    
                    border-radius: 10px;
                    width: 0px;
                }
            """)
            label.setFixedHeight(250) 
            label.setVisible(True)
            label.state = 2 

        else:
            label.setFont(QFont("Arial", 25))
            label.setFixedHeight(0)  
            label.setVisible(False)
            label.state = 0  
    
    def open_second_window(self):
        try:
            subprocess.Popen(["python", "interface2.py"])
        except Exception as e:
            print(f"Erreur lors de l'exécution de 'resulatPert.py' : {e}")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
