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
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QSettings

# Modelo
class ObfuscatorModel:
    def __init__(self):
        self.salt = secrets.token_bytes(16)

    def obfuscate(self, original_data, compression_level=9, progress_callback=None):
        compressed_data = zlib.compress(original_data, compression_level)
        salt_encoded_data = self.salt.hex() + base64.b64encode(compressed_data).decode()
        ofuspy_template = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
#   OfusPy3 - Ofuscador Python 
#   3.0.1a14
#   Pacheco, Matias W. <mwpacheco@outlook.es>
#   Copyright (c) 2024 Wehaa Portal Soft.
#   Licencia GPL-3.0
#
#   ¡ADVERTENCIA! No modificar el contenido de este archivo.
#
################################################################################
import zlib, base64

base64_encoded = "{salt_encoded_data}"

salt_hex = base64_encoded[:32]
data_encoded = base64_encoded[32:]

assert len(salt_hex) == 32, "Invalid salt length"
assert all(c in '0123456789abcdef' for c in salt_hex), "Salt is not hexadecimal"

exec(zlib.decompress(base64.b64decode(data_encoded)))
'''
        return ofuspy_template.encode()

class LogModel:
    def __init__(self):
        self.conn = sqlite3.connect("OfusLogs.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level TEXT,
                message TEXT
            );
        """)
        self.conn.commit()

    def log(self, level, message):
        self.cur.execute("INSERT INTO logs (level, message) VALUES (?, ?)", (level, message))
        self.conn.commit()

    def fetch_logs(self):
        self.cur.execute("SELECT * FROM logs")
        return self.cur.fetchall()

class Model:
    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value