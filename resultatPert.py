import sys
import re
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,  QVBoxLayout, QWidget, QHBoxLayout,  QTableWidget, QTableWidgetItem, QHeaderView,QSizePolicy
from PyQt5.QtCore import Qt






class Tache(object):
    def __init__(self, nom, duree, precedents):
        self.nom = nom
        self.precedents = precedents
        self.duree = duree
        self.ES = 0 #early start date 
        self.EF = 0 #early finished date  
        self.successeurs = []
        self.LS = 0
        self.LF = 0
        self.marge_totale = 0
        self.marge_libre = 0
        self.critique = ''

    
    def calcMargeTotale(self):
        self.marge_totale = self.LF - self.duree - self.ES
        self.critique = '✅' if self.marge_totale == 0 else '❌' 
    def calcMargeLibre(self, liste_taches):
        if self.successeurs:
            es_successeurs = []
            for successeur_nom in self.successeurs:
                for tache in liste_taches:
                    if tache.nom == successeur_nom:
                        es_successeurs.append(tache.ES)
            self.marge_libre = min(es_successeurs) - self.EF
        else:
            self.marge_libre = self.marge_totale


def lireData(excel_file):
    df = pd.read_excel(excel_file)
    return df

def creerTaches(df):
    liste_taches = []
    for i in range(len(df)):
        liste_taches.append(Tache(df['Tâche'][i],df['Durée'][i], df['Précédent'][i]))
    return liste_taches

def parcoursEnAvant(liste_taches):
    for tache in liste_taches:
        if isinstance(tache.precedents, str):
            tache.precedents = tache.precedents.upper()
            ef = []
            for j in tache.precedents:
                for t in liste_taches:
                    if t.nom == j:
                        ef.append(t.EF)
                tache.ES = max(ef)
        else:
            tache.ES = 0
        tache.EF = tache.ES + tache.duree

def parcoursEnArriere(liste_taches):
    pred = []
    eF = []
    for tache in liste_taches:
        if isinstance(tache.precedents, str):
            for j in tache.precedents:
                pattern = re.compile(r'[a-zA-Z]')
                match = pattern.finditer(j)
                for r in match:
                    pred.append(j)
                    for m in liste_taches:
                        if m.nom == j:
                            m.successeurs.append(tache.nom)
        eF.append(tache.EF)

    for tache in reversed(liste_taches):
        if tache.nom not in pred:
            tache.LF = max(eF)
        else:
            minLs = []
            for x in tache.successeurs:
                for t in liste_taches:
                    if t.nom == x:
                        minLs.append(t.LS)
            tache.LF = min(minLs)
        tache.LS = tache.LF - tache.duree

def margeTotale(liste_taches):
    for tache in liste_taches:
        tache.calcMargeTotale()
def margeLibre(liste_taches):
    for tache in liste_taches:
        tache.calcMargeLibre(liste_taches)

def MAJdataFrame(df, liste_taches):
    df2 = pd.DataFrame({
        'Tâche': df['Tâche'],
        'Durée': df['Durée'],
        'Précédent': df['Précédent'],
        'ES': pd.Series([tache.ES for tache in liste_taches]),
        'LS': pd.Series([tache.LS for tache in liste_taches]),
        'EF': pd.Series([tache.EF for tache in liste_taches]),
        'LF': pd.Series([tache.LF for tache in liste_taches]),
        'Marge Totale': pd.Series([tache.marge_totale for tache in liste_taches]),
        'Marge Libre': pd.Series([tache.marge_libre for tache in liste_taches]),
        'Tâche Critique': pd.Series([tache.critique for tache in liste_taches]),

    })
    return df2

























class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1900, 1000)
        self.setWindowTitle("Le resultat")
        self.setStyleSheet("background-color:white;")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 0)
        headerLayout.setSpacing(0)
        decoration1Label = QLabel(self)
        decoration1 = QPixmap("image2.jpg").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        decoration1Label.setPixmap(decoration1)
        decoration1Label.setScaledContents(True)
        decoration1Label.setFixedSize(250, 250)  
        logo = QPixmap('logo.jpg').scaled(300, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logoLabel = QLabel(self)
        logoLabel.setPixmap(logo)
        logoLabel.setAlignment(Qt.AlignCenter)
        logoLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        decoration2Label = QLabel(self)
        decoration2 = QPixmap("image1.jpg").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        decoration2Label.setPixmap(decoration2)
        decoration2Label.setScaledContents(True)
        decoration2Label.setFixedSize(250, 250)

        headerLayout.addWidget(decoration1Label)
        headerLayout.addStretch() 
        headerLayout.addWidget(logoLabel)
        headerLayout.addStretch()  
        headerLayout.addWidget(decoration2Label)

        mainLayout.addLayout(headerLayout)

        mainLayout.addStretch() 
        contentLayout = QVBoxLayout()
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentLayout.setSpacing(10)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setFixedWidth(1700)   
        self.tableWidget.setFixedHeight(650)

        self.tableWidget.setStyleSheet("""
            QTableWidget {
                font-size: 20px;
                font-weight: bold;
                background-color: #f9f9f9;
                border: none;
                padding: 15px;
                margin-top:0px;
                margin-bottom:20px;
                margin-right: 10px; 
                border-left:20px;

            }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-size: 22px;
                font-weight: bold;
                padding: 5px;
                border: 2px solid #ddd;
            }
        """)

        self.minimalDurationLabel = QLabel(self)
        self.minimalDurationLabel.setStyleSheet("font-size:30px; font-weight:bold; color:#000000; margin-bottom:100px;")
        contentLayout.addWidget(self.tableWidget, alignment=Qt.AlignHCenter)
        contentLayout.addWidget(self.minimalDurationLabel, alignment=Qt.AlignHCenter)
        mainLayout.addLayout(contentLayout)

        self.load_data_from_excel("output.xlsx")


    
    def load_data_from_excel(self,file_path):
            try:
                
                df = pd.read_excel(file_path)
                self.tableWidget.setRowCount(len(df))
                self.tableWidget.setColumnCount(len(df.columns))

                self.tableWidget.setHorizontalHeaderLabels(df.columns)

                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        if pd.isna(value):
                            value=""
                        item = QTableWidgetItem(str(value))
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        self.tableWidget.setItem(row_idx, col_idx, item)
                        duree_minimale_projet = df['EF'].max()

                        self.minimalDurationLabel.setText(f"➡️La durée Minimale de votre projet est : {duree_minimale_projet} jours")

            except Exception as e:
                print(f"Erreur lors du chargement des données : {e}")

    



def main():

    excel_file = 'input.xlsx'
    df = lireData(excel_file)
    print('Loaded data:')
    print(df)
    liste_taches = creerTaches(df)
    parcoursEnAvant(liste_taches)
    parcoursEnArriere(liste_taches)
    margeTotale(liste_taches)
    margeLibre(liste_taches)
    finaldf = MAJdataFrame(df, liste_taches)
    print("Results:")
    print(finaldf)
    print('Results saved to output.xlsx')
    finaldf.to_excel('output.xlsx', index=False)
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


