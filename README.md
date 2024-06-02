[![GitHub License](https://img.shields.io/github/license/wehaaportal/OfusPy-3)](https://github.com/wehaaportal/OfusPy-3/blob/main/LICENSE) 
[![GitHub Release](https://img.shields.io/github/v/release/wehaaportal/OfusPy-3?include_prereleases)](https://github.com/wehaaportal/OfusPy-3/releases)
![GitHub Size](https://img.shields.io/github/repo-size/wehaaportal/OfusPy-3)

# OfusPy 3

![OfusPy3 Captura](https://github.com/wehaaportal/OfusPy-3/blob/main/assets/Code_Obfuscator.png "OfusPy3.0.1a14")

**OfusPy 3** es una aplicación diseñada para la ofuscación de código Python, brindando una capa adicional de seguridad a través de la tecnología de compresión ZIP y la codificación Base64, complementadas con un "salt" para una protección más robusta.

## Características Principales

1. **Interfaz de Usuario:**
   - **Botones de Acción:**
     - **Open File:** Permite seleccionar el archivo de Python (.py) que se desea ofuscar.
     - **Syntax Highlight:** Resalta la sintaxis del código fuente para facilitar su lectura y análisis.
     - **Obfuscate:** Inicia el proceso de ofuscación del código seleccionado.
     - **View Log:** Muestra un registro de las acciones realizadas y los mensajes de error o éxito generados durante el proceso.

2. **Visor de Clases y Funciones:**
   - Muestra un árbol jerárquico donde se pueden ver los nombres de las clases y funciones (def) presentes en el archivo seleccionado, facilitando la navegación y comprensión del código estructurado.

3. **Visualización del Código:**
   - **Visor de Código:** Una caja de texto de solo lectura donde se puede ver el código completo del archivo seleccionado, con numeración de líneas para facilitar la revisión. Esta caja no permite la edición directa del código, asegurando que el archivo original no se modifique accidentalmente.

4. **Información del Archivo:**
   - **Nombre del Archivo, Extensión y Tamaño:** Un dock en la parte inferior de la interfaz muestra información detallada del archivo seleccionado, incluyendo su nombre, extensión y tamaño.
   - **Nivel de Compresión:** Un control deslizante permite ajustar el nivel de compresión aplicado durante el proceso de ofuscación.

5. **Controles de Ofuscación:**
   - **Botón de Ofuscación:** Inicia el proceso de ofuscación aplicando las técnicas mencionadas (ZIP, Base64, y salt).
   - **Botón de Guardado:** Permite guardar el archivo ofuscado resultante en la ubicación deseada.

## Tecnología y Arquitectura

- **Modelo-Vista-Controlador (MVC):** OfusPy 3 está escrito siguiendo el patrón de diseño MVC, separando claramente la lógica de la aplicación (Modelo), la interfaz de usuario (Vista), y el manejo de eventos (Controlador). Esto facilita el mantenimiento y la escalabilidad de la aplicación.
- **PyQt6:** La interfaz gráfica de usuario (GUI) está desarrollada utilizando PyQt6, una biblioteca que permite crear aplicaciones gráficas de alta calidad en Python, aprovechando las ventajas de Qt6.

## Funcionamiento

1. **Selección del Archivo:**
   - El usuario selecciona un archivo de Python a través del botón "Open File".
   - La aplicación carga el archivo y muestra sus clases y funciones en el visor correspondiente.

2. **Configuración de Ofuscación:**
   - El usuario ajusta el nivel de compresión deseado usando el control deslizante.
   - Puede visualizar y resaltar la sintaxis del código antes de proceder.

3. **Proceso de Ofuscación:**
   - Al presionar "Obfuscate", la aplicación aplica la compresión ZIP, la codificación Base64, y agrega un salt para asegurar la ofuscación del código.
   - El resultado es un archivo de Python ofuscado que es difícil de leer o entender sin el proceso inverso de deofuscación.

4. **Guardado del Archivo Ofuscado:**
   - Finalmente, el usuario puede guardar el archivo resultante usando el botón "Save", eligiendo la ubicación y el nombre deseados para el archivo ofuscado.

**OfusPy 3** es una herramienta poderosa y fácil de usar para desarrolladores que buscan proteger su código Python, manteniendo la simplicidad y eficiencia gracias a su diseño MVC y la robustez de PyQt6.

# Wehaa Portal Soft.

  - Pacheco, Matias W.
  - <mwpacheco@outlook.es>
  - GPL-3.0

# Tecnologias:

  - Python3                3.11.6
      - sqlite3
  - PyQt6                  6.4.2
