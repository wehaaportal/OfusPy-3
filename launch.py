#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
#   OfusPy3 - Ofuscador Python 
#   3.0.1a14
#   Pacheco, Matias W. <mwpacheco@outlook.es>
#   Copyright (c) 2024 Wehaa Portal Soft.
#   Licencia GPL-3.0
#
################################################################################

# Import 
import os, sys, sqlite3, zlib, base64, ast, secrets

# PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel,
    QMdiArea, QDockWidget, QVBoxLayout, QWidget, QTextEdit, QSlider,
    QProgressBar, QPushButton, QHBoxLayout, QTableWidget, QSizePolicy, QStatusBar,
    QTableWidgetItem, QDialog, QTreeView, QPlainTextEdit, QSpacerItem
)
from PyQt6.QtGui import QIcon, QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QAction, QTextCursor, QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt, QTimer, QRegularExpression, QModelIndex, QTranslator, QLocale, QSettings

# Internal Import
from model import ObfuscatorModel, LogModel, Model
from views import SplashScreen, MainView
from controller import MainController

# Inicialización de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()

    # Simular una carga inicial con actualizaciones periódicas
    def load():
        for i in range(101):
            QTimer.singleShot(i * 50, lambda value=i: splash.update_progress(value))
            if i == 20:
                QTimer.singleShot(i * 50, lambda: splash.update_message("Loading modules..."))
            elif i == 50:
                QTimer.singleShot(i * 50, lambda: splash.update_message("Initializing..."))
            elif i == 80:
                QTimer.singleShot(i * 50, lambda: splash.update_message("Starting application..."))

    QTimer.singleShot(100, load)

    obfuscator = ObfuscatorModel()
    log_model = LogModel()
    main_view = MainView()
    controller = MainController(obfuscator, main_view, log_model, Model)

    app.setStyle('Fusion')
    
    QTimer.singleShot(4000, lambda: main_view.show())
    QTimer.singleShot(4000, lambda: splash.finish(main_view))

    sys.exit(app.exec())