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
    QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QSplashScreen,
    QMdiArea, QDockWidget, QVBoxLayout, QWidget, QTextEdit, QSlider, 
    QProgressBar, QPushButton, QHBoxLayout, QTableWidget, QSizePolicy, QStatusBar,
    QTableWidgetItem, QDialog, QTreeView, QPlainTextEdit, QSpacerItem
)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QTextCharFormat, QColor, QSyntaxHighlighter, QAction, QTextCursor, QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt, QTimer, QRegularExpression, QModelIndex, QTranslator, pyqtSlot, QLocale, QSettings

# Vista
class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("img/ofusplash2.png"))
        # Establecer la apariencia de la ventana
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)

        # Crear y configurar un QProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, self.pixmap().height() - 30, self.pixmap().width() - 20, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2e2e2e;
                color: white;
                border-style: none;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 10px;
                margin: 1px;
            }
        """)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setValue(0)

        # Crear y configurar una QLabel para mostrar mensajes
        self.message_label = QLabel(self)
        self.message_label.setGeometry(10, self.pixmap().height() - 60, self.pixmap().width() - 20, 20)
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.message_label.setFont(QFont("Arial", 10))
        self.message_label.setText("Loading...")

    @pyqtSlot(int)
    def update_progress(self, value):
        """Update the progress bar value."""
        self.progress_bar.setValue(value)

    @pyqtSlot(str)
    def update_message(self, message):
        """Update the splash screen message."""
        self.message_label.setText(message)

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_formats()
        self.init_rules()

    def init_formats(self):
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("orange"))#self.hsl(300, 30, 68)
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("grey"))
        self.comment_format.setFontItalic(True)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("green"))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("blue"))

        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor("purple"))
        self.class_format.setFontItalic(True)
        self.class_format.setFontPointSize(int(9))
        self.class_format.setFontWeight(QFont.Weight.Bold)

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor("purple"))
        self.function_format.setFontItalic(True)
        self.function_format.setFontPointSize(int(9))
        self.function_format.setFontWeight(QFont.Weight.Bold)

        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor("red"))

        self.decorator_format = QTextCharFormat()
        self.decorator_format.setForeground(QColor(self.hsl(40, 94, 68)))
        self.decorator_format.setFontItalic(True)
        
    def hsl(self, hue: int, saturation: int, lightness: int, alpha=255):
        # Crear el color desde HSL con alpha
        color = QColor.fromHsl(hue, saturation, lightness, alpha)
    
        # Convertir el color a formato entero RGBA
        return color.rgba()

    def init_rules(self):
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", "False",
            "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or",
            "pass", "raise", "return", "True", "try", "while", "with", "self", "yield"
        ]
        keyword_pattern = "|".join([f"\\b{k}\\b" for k in keywords])
        rules = [
            (QRegularExpression("\\b" + "\\b|\\b".join(keywords) + "\\b"), self.keyword_format),
            (QRegularExpression("#[^\n]*"), self.comment_format),
            (QRegularExpression("\"\"\".*?\"\"\"|\'\'\'.*?\'\'\'"), self.string_format),  # Multiline strings
            (QRegularExpression("\"[^\"]*\"|\'[^\']*\'"), self.string_format),  # Single line strings
            (QRegularExpression("\\b[0-9]+(\\.[0-9]+)?\\b"), self.number_format),
            (QRegularExpression("'[^']*'|==|="), self.class_format),
            (QRegularExpression("\\bclass\\s+(\\w+)"), self.class_format),  # Highlight class names
            (QRegularExpression("\\bdef\\s+(\\w+)"), self.function_format),  # Highlight function names
            (QRegularExpression("[+\\-*/%=&|^~<>!]+"), self.operator_format),  # Operators
            (QRegularExpression("@\\w+"), self.decorator_format),  # Decorators
        ]
        self.rules = [(rx, fmt) for rx, fmt in rules]

    def highlightBlock(self, text):
        for expression, format in self.rules:
            expression_index = expression.match(text).capturedStart()
            while expression_index != -1:
                length = expression.match(text).capturedLength()
                self.setFormat(expression_index, length, format)
                expression_index = expression.match(text, expression_index + length).capturedStart()

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Obfuscator")
        self.setWindowIcon(QIcon("img/ofuspy.ico"))
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_toolbar()
        self.create_text_editor()
        self.create_dock_widget()
        self.create_status_bar()

    def create_menu(self):
        main_menu = self.menuBar()

        # File Menu
        self.file_menu = main_menu.addMenu("&File")
        open_action = QAction(QIcon("img/icons8-add-file-100.png"), "Open File", self)
        open_action.setShortcut("Ctrl+O")
        exit_action = QAction(QIcon("img/icons8-exit-100.png"), "Exit", self)
        exit_action.setShortcut("Ctrl+E")
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)

        # Tools Menu
        self.tools_menu = main_menu.addMenu("&Tools")
        syntax_highlight_action = QAction(QIcon("img/icons8-color-wheel-2-100.png"), "Syntax Highlight", self, checkable=True)
        syntax_highlight_action.setShortcut("Ctrl+H")
        syntax_highlight_action.setChecked(True)
        obfuscate_action = QAction(QIcon("img/icons8-cyber-security-100.png"), "Obfuscate", self)
        obfuscate_action.setShortcut("Ctrl+Shift+O")
        self.tools_menu.addAction(syntax_highlight_action)
        self.tools_menu.addAction(obfuscate_action)

        # View Menu
        self.view_menu = main_menu.addMenu("&View")
        show_logs_action = QAction(QIcon("img/icons8-expired-100.png"), "View Log", self)
        show_logs_action.setShortcut("Ctrl+L")
        toggle_toolbar_action = QAction(QIcon("img/icons8-menubar-100.png"), "Toggle Toolbar", self, checkable=True)
        toggle_toolbar_action.setShortcut("Ctrl+T")
        toggle_toolbar_action.setChecked(True)
        self.view_menu.addAction(show_logs_action)
        self.view_menu.addAction(toggle_toolbar_action)

        # Connect actions to controller
        self.open_action = open_action
        self.exit_action = exit_action
        self.syntax_highlight_action = syntax_highlight_action
        self.obfuscate_action = obfuscate_action
        self.show_logs_action = show_logs_action
        self.toggle_toolbar_action = toggle_toolbar_action

    def create_toolbar(self):
        self.toolbar = self.addToolBar("OfusPy Toolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.syntax_highlight_action)
        self.toolbar.addAction(self.obfuscate_action)
        self.toolbar.addAction(self.show_logs_action)

    def create_text_editor(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.highlighter = PythonSyntaxHighlighter(self.text_edit.document())

    def create_dock_widget(self):
        self.dock = QDockWidget("Class and Function Viewer", self)
        self.tree = QTreeView()
        self.tree.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.dock.setWidget(self.tree)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.dock_widget = QDockWidget("File Information and Controls Obfuscate", self)
        dock_widget_content = QWidget()
        layout = QVBoxLayout()

        self.file_name_label = QLabel("File: None")
        self.file_extension_label = QLabel("Extension: None")
        self.file_size_label = QLabel("Size: None")
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_name_label)
        file_layout.addWidget(self.file_extension_label)
        file_layout.addWidget(self.file_size_label)
        layout.addLayout(file_layout)

        compression_layout = QHBoxLayout()
        compression_label = QLabel("Compression Level:")
        self.compression_slider = QSlider(Qt.Orientation.Horizontal)
        self.compression_slider.setRange(1, 9)
        self.compression_slider.setValue(9)
        compression_layout.addWidget(compression_label)
        compression_layout.addWidget(self.compression_slider)
        layout.addLayout(compression_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # Botones adicionales
        self.obfuscate_button = QPushButton("Obfuscate")
        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(False)  # Initially disabled
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.obfuscate_button)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)

        dock_widget_content.setLayout(layout)
        self.dock_widget.setWidget(dock_widget_content)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_widget)

    def create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
