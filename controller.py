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
from PyQt6.QtGui import QIcon, QTextCharFormat, QColor, QSyntaxHighlighter, QAction, QTextCursor, QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt, QTimer, QRegularExpression, QModelIndex, QTranslator, QLocale, QSettings

# Controlador
class MainController:
    def __init__(self, model, view, log_model, msettings):
        self.model = model
        self.view = view
        self.log_model = log_model
        self. sett = msettings

        self.original_code = None

        # Definir la ruta del archivo .ini en el mismo directorio que el script principal
        ini_file_path = os.path.join(os.path.dirname(__file__), 'settings.ini')
        self.settings = QSettings(ini_file_path, QSettings.Format.IniFormat)

        self.connect_signals()        

    def connect_signals(self):
        """Connect UI signals to corresponding slots."""
        self.view.open_action.triggered.connect(self.open_file)
        self.view.exit_action.triggered.connect(self.exit_app)

        self.view.syntax_highlight_action.triggered.connect(self.toggle_syntax_highlight)
        self.view.toggle_toolbar_action.triggered.connect(self.toggle_toolbar)

        self.view.show_logs_action.triggered.connect(self.show_logs)

        self.view.obfuscate_action.triggered.connect(self.obfuscate_code)
        self.view.compression_slider.valueChanged.connect(self.update_compression_level)
        self.view.obfuscate_button.clicked.connect(self.obfuscate_code)
        self.view.save_button.clicked.connect(self.save_file)

    def toggle_toolbar(self):
        self.view.toolbar.hide() if self.view.toolbar.isVisible() else self.view.toolbar.show()

    def toggle_syntax_highlight(self):
        if self.view.highlighter:
            self.view.highlighter.setDocument(None if self.view.highlighter.document() else self.view.text_edit.document())       

    def open_file(self):
        """Open a Python file and display its content with line numbers."""
        options = QFileDialog.Option.ReadOnly        
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open Python File", "", "Python Files (*.py)", options=options)
        if file_path:
            try:
                self.namefileopen = os.path.splitext(file_path)[0]
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.original_code = file.read()

                # Display the text with line numbers
                numbered_lines = self.add_line_numbers(self.original_code)
                self.view.text_edit.setPlainText(numbered_lines)

                # Log the file opening
                self.log_model.log("INFO", f"Opened file: {file_path}")

                # Update the filename, extension, size label
                self.view.file_name_label.setText(f"File: {os.path.basename(file_path)}")
                self.view.file_extension_label.setText(f"Extension: {os.path.splitext(file_path)[1]}")
                self.view.file_size_label.setText(f"Size: {str(os.path.getsize(file_path))} bytes")

                # Update the tree view
                self.update_tree_view()
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Failed to open file: {str(e)}")
                self.log_model.log("ERROR", f"Failed to open file: {str(e)}")

    def add_line_numbers(self, code):
        """Adds line numbers to the given code."""
        return ''.join(f"{i + 1} {line}\n" for i, line in enumerate(code.splitlines()))

    def exit_app(self):
        self.log_model.log("INFO", "Application exited")
        QApplication.instance().quit()

    def update_tree_view(self):
        """Updates the tree view with classes and functions from the original code."""
        text = self.original_code

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Classes and Functions"])

        def add_items(parent, elements: list):
            for element in elements:
                if isinstance(element, ast.ClassDef):
                    class_item = QStandardItem(f"class {element.name}")
                    class_item.setForeground(QColor("blue"))
                    parent.appendRow(class_item)
                    add_items(class_item, element.body)
                elif isinstance(element, ast.FunctionDef):
                    func_item = QStandardItem(f"def {element.name}")
                    func_item.setForeground(QColor("red"))
                    parent.appendRow(func_item)
                elif hasattr(element, "body"):
                    add_items(parent, element.body)
        try:
            tree = ast.parse(text)
            add_items(model, tree.body)
        except SyntaxError as e:
            QMessageBox.critical(self.view, "Syntax Error", f"Failed to parse file: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"An unexpected error occurred: {str(e)}")
            self.log_model.log("ERROR", f"Unexpected error: {str(e)}")

        self.view.tree.setModel(model)
        self.view.tree.expandAll()

    def obfuscate_code(self):
        """Obfuscate the code with the specified compression level."""
        try:
            original_data = self.original_code.encode("utf-8") if self.original_code else None

            if original_data:
                compression_level = self.view.compression_slider.value()
        
                def progress_callback(progress):
                    self.view.progress_bar.setValue(progress)

                self.obfuscated_data = self.model.obfuscate(original_data, compression_level, progress_callback)
                # Display the text with line numbers
                numbered_lines = self.add_line_numbers(self.obfuscated_data.decode("utf-8"))
                self.view.text_edit.setPlainText(numbered_lines)
                self.log_model.log("INFO", "Code obfuscated")
                QMessageBox.information(self.view, "Success", "File obfuscated successfully.")
                self.view.save_button.setEnabled(True)  # Enable save button after obfuscation
            else:
                QMessageBox.critical(self.view, "Error", "No code to obfuscate.")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"An unexpected error occurred: {str(e)}")
            self.log_model.log("ERROR", f"Obfuscation failed: {str(e)}")

    def update_compression_level(self, value):
        """Log the updated compression level."""
        self.log_model.log("INFO", f"Compression level set to {value}")

    def save_file(self):
        obfuscated_text = self.obfuscated_data.decode("utf-8")
        filename, _ = QFileDialog.getSaveFileName(self.view, "Save Obfuscated File", f"{self.namefileopen}_obfuscated", "Python Files (*.py)")
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(obfuscated_text)
                QMessageBox.information(self.view, "Success", "File saved successfully.")
                self.log_model.log("INFO", f"Saved file: {filename}")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Failed to save file: {str(e)}")
                self.log_model.log("ERROR", f"Failed to save file: {str(e)}")

            self.view.save_button.setEnabled(False)  # Enable save button after obfuscation

    def show_logs(self):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Log Viewer")
        dialog_layout = QVBoxLayout()

        table_widget = QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Timestamp", "Level", "Message"])

        self.log_model.cur.execute("SELECT timestamp, level, message FROM logs ORDER BY id DESC LIMIT 10")
        logs = self.log_model.cur.fetchall()

        for row_num, (timestamp, level, message) in enumerate(logs):
            table_widget.insertRow(row_num)
            table_widget.setItem(row_num, 0, QTableWidgetItem(str(timestamp)))
            table_widget.setItem(row_num, 1, QTableWidgetItem(level))
            table_widget.setItem(row_num, 2, QTableWidgetItem(message))

        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()

        dialog_layout.addWidget(table_widget)
        dialog.setLayout(dialog_layout)

        dialog.setFixedSize(table_widget.horizontalHeader().length() + 50, table_widget.verticalHeader().length() + 50)
        
        dialog.exec()