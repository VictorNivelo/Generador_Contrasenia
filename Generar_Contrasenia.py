import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QListWidget,
    QMessageBox,
    QInputDialog,
    QGridLayout,
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import pyperclip


class GeneradorContrasenas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Contraseñas Seguras")
        self.setFixedSize(600, 800)
        self.modo_oscuro = False
        self.contrasenas_generadas = []
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.crear_widgets()
        self.aplicar_tema()

    def crear_widgets(self):
        titulo = QLabel("Generador de Contraseñas")
        titulo.setFont(QFont("Arial", 28, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(titulo)
        layout_longitud = QHBoxLayout()
        self.layout_principal.addLayout(layout_longitud)
        etiqueta_longitud = QLabel("Longitud:")
        etiqueta_longitud.setFont(QFont("Arial", 14))
        layout_longitud.addWidget(etiqueta_longitud)
        self.entrada_longitud = QLineEdit("20")
        self.entrada_longitud.setFixedWidth(60)
        self.entrada_longitud.setFont(QFont("Arial", 14))
        layout_longitud.addWidget(self.entrada_longitud)
        layout_checkboxes = QGridLayout()
        self.layout_principal.addLayout(layout_checkboxes)
        opciones = ["Mayúsculas", "Minúsculas", "Números", "Símbolos"]
        for i, texto in enumerate(opciones):
            check = QCheckBox(texto)
            check.setFont(QFont("Arial", 14))
            check.setChecked(True)
            layout_checkboxes.addWidget(check, i // 2, i % 2)
            setattr(self, f"check_{texto.lower()}", check)
        self.boton_generar = QPushButton("Generar Contraseña")
        self.boton_generar.setFont(QFont("Arial", 16, QFont.Bold))
        self.boton_generar.clicked.connect(self.generar_contrasena)
        self.layout_principal.addWidget(self.boton_generar)
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setReadOnly(True)
        self.entrada_contrasena.setAlignment(Qt.AlignCenter)
        self.entrada_contrasena.setFont(QFont("Courier", 18))
        self.layout_principal.addWidget(self.entrada_contrasena)
        layout_botones = QHBoxLayout()
        self.layout_principal.addLayout(layout_botones)
        for texto, funcion in [
            ("Copiar", self.copiar_contrasena),
            ("Limpiar", self.limpiar_contrasenas),
            ("Generar Múltiples", self.generar_multiples_contrasenas),
            ("Copiar Todas", self.copiar_todas_las_contrasenas),
        ]:
            boton = QPushButton(texto)
            boton.setFont(QFont("Arial", 12))
            boton.clicked.connect(funcion)
            layout_botones.addWidget(boton)
        self.boton_tema = QPushButton("Cambiar Tema")
        self.boton_tema.setFont(QFont("Arial", 12))
        self.boton_tema.clicked.connect(self.cambiar_tema)
        self.layout_principal.addWidget(self.boton_tema)
        self.lista_contrasenas = QListWidget()
        self.lista_contrasenas.setFont(QFont("Courier", 14))
        self.layout_principal.addWidget(self.lista_contrasenas)

    def generar_contrasena(self):
        caracteres = ""
        if self.check_mayúsculas.isChecked():
            caracteres += string.ascii_uppercase
        if self.check_minúsculas.isChecked():
            caracteres += string.ascii_lowercase
        if self.check_números.isChecked():
            caracteres += string.digits
        if self.check_símbolos.isChecked():
            caracteres += string.punctuation
        if not caracteres:
            self.entrada_contrasena.setText("Seleccione al menos una opción")
            return
        longitud = int(self.entrada_longitud.text())
        contrasena = "".join(random.choice(caracteres) for _ in range(longitud))
        self.entrada_contrasena.setText(contrasena)
        self.contrasenas_generadas.append(contrasena)
        self.lista_contrasenas.addItem(contrasena)

    def generar_multiples_contrasenas(self):
        cantidad, ok = QInputDialog.getInt(
            self, "Generar múltiples contraseñas", "Número de contraseñas:", 5, 1, 20
        )
        if ok:
            for _ in range(cantidad):
                self.generar_contrasena()

    def copiar_contrasena(self):
        contrasena = self.entrada_contrasena.text()
        if contrasena and contrasena != "Seleccione al menos una opción":
            pyperclip.copy(contrasena)
            self.mostrar_mensaje("Contraseña copiada al portapapeles")

    def copiar_todas_las_contrasenas(self):
        if self.contrasenas_generadas:
            todas_contrasenas = "\n".join(self.contrasenas_generadas)
            pyperclip.copy(todas_contrasenas)
            self.mostrar_mensaje("Todas las contraseñas copiadas al portapapeles")
        else:
            self.mostrar_mensaje("No hay contraseñas para copiar.")

    def limpiar_contrasenas(self):
        self.entrada_contrasena.clear()
        self.lista_contrasenas.clear()
        self.contrasenas_generadas.clear()

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def aplicar_tema(self):
        if self.modo_oscuro:
            self.setStyleSheet(
                """
                QWidget {
                    background-color: #2C2C2C;
                    color: #E0E0E0;
                }
                QLineEdit, QListWidget {
                    background-color: #3D3D3D;
                    border: 1px solid #555555;
                    color: #E0E0E0;
                }
                QPushButton {
                    background-color: #4A4A4A;
                    color: #E0E0E0;
                    border: 1px solid #555555;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #5A5A5A;
                }
                QCheckBox {
                    color: #E0E0E0;
                }
                QCheckBox::indicator {
                    border: 1px solid #555555;
                    background: #3D3D3D;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QWidget {
                    background-color: #F0F0F0;
                    color: #333333;
                }
                QLineEdit, QListWidget {
                    background-color: white;
                    border: 1px solid #CCCCCC;
                }
                QPushButton {
                    background-color: #E0E0E0;
                    border: 1px solid #CCCCCC;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #D0D0D0;
                }
                QCheckBox::indicator {
                    border: 1px solid #CCCCCC;
                    background: white;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                }
            """
            )
        self.boton_generar.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorContrasenas()
    ventana.show()
    sys.exit(app.exec_())
