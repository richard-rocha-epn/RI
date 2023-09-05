from enum import auto
from tkinter import *
import re
import math
import tkinter.filedialog as filedialog
from tkinter import ttk
from tkinter.ttk import Style
import pandas as pd
from unidecode import unidecode

class VectorialModelGUI:
    def __init__(self):
        self.vocabulario = []
        self.documentos = []
        self.resultados = []
        self.stopwords = []
        self.ventana = Tk()
        self.ventana.title("Modelo Vectorial")
        
        # Etiqueta y entrada para definir el conjunto de descriptores (vocabulario)
        self.vocabulario_label = Label(self.ventana, text="Vocabulario:")
        self.vocabulario_label.grid(row=0, column=0)
        self.vocabulario_entry = Entry(self.ventana)
        self.vocabulario_entry.grid(row=0, column=1)
        self.vocabulario_button = Button(self.ventana, text="Definir", command=self.definir_vocabulario)
        self.vocabulario_button.grid(row=0, column=2)
        self.vocabulario_cargar_button = Button(self.ventana, text="Cargar desde archivo", command=self.cargar_vocabulario)
        self.vocabulario_cargar_button.grid(row=0, column=3)
        
        # Etiqueta y entrada para definir el conjunto de documentos
        self.documentos_label = Label(self.ventana, text="Documentos:")
        self.documentos_label.grid(row=1, column=0)
        self.documentos_entry = Entry(self.ventana)
        self.documentos_entry.grid(row=1, column=1)
        self.documentos_button = Button(self.ventana, text="Definir", command=self.definir_documentos)
        self.documentos_button.grid(row=1, column=2)
        self.documentos_cargar_button = Button(self.ventana, text="Cargar desde archivo", command=self.cargar_documentos)
        self.documentos_cargar_button.grid(row=1, column=3)
        
        # Etiqueta y entrada para cargar archivo de stopwords
        self.stopwords_label = Label(self.ventana, text="Stopwords:")
        self.stopwords_label.grid(row=2, column=0)
        self.stopwords_entry = Entry(self.ventana)
        self.stopwords_entry.grid(row=2, column=1)
        self.stopwords_cargar_button = Button(self.ventana, text="Cargar stopwords", command=self.cargar_stopwords)
        self.stopwords_cargar_button.grid(row=2, column=2)
        
        # Etiqueta y entrada para ingresar la consulta
        self.consulta_label = Label(self.ventana, text="Consulta:")
        self.consulta_label.grid(row=3, column=0)
        self.consulta_entry = Entry(self.ventana)
        self.consulta_entry.grid(row=3, column=1)
        self.consulta_button = Button(self.ventana, text="Buscar", command=self.buscar_documentos)
        self.consulta_button.grid(row=3, column=2)
        
        # Botón para limpiar los campos y la tabla
        self.limpiar_button = Button(self.ventana, text="Limpiar", command=self.limpiar_campos)
        self.limpiar_button.grid(row=3, column=3)
        
        # Tabla para mostrar los resultados
        self.resultados_tabla = ttk.Treeview(self.ventana, columns=("Documento", "Producto Interno", "Magnitud Documento", "Magnitud Consulta", "Similitud", "Producto de Módulos", "Número de Palabras", "Producto Interno Normalizado"))
        self.resultados_tabla.heading("#0", text="Índice")
        self.resultados_tabla.heading("Documento", text="#Doc")
        self.resultados_tabla.heading("Producto Interno", text="Producto Interno")
        self.resultados_tabla.heading("Magnitud Documento", text="|d|")
        self.resultados_tabla.heading("Magnitud Consulta", text="|q|")
        self.resultados_tabla.heading("Similitud", text="Similitud")
        self.resultados_tabla.heading("Producto de Módulos", text="|q|.|d|")
        self.resultados_tabla.heading("Número de Palabras", text="W_d")
        self.resultados_tabla.heading("Producto Interno Normalizado", text="Producto Interno Normalizado")
        self.resultados_tabla.column("#0", width=50)
        self.resultados_tabla.column("Documento", width=50)
        self.resultados_tabla.column("Producto Interno", width=110)
        self.resultados_tabla.column("Magnitud Documento", width=50)
        self.resultados_tabla.column("Magnitud Consulta", width=50)
        self.resultados_tabla.column("Similitud", width=70)
        self.resultados_tabla.column("Producto de Módulos", width=50)
        self.resultados_tabla.column("Número de Palabras", width=50)
        self.resultados_tabla.column("Producto Interno Normalizado", width=180)
        
        self.resultados_tabla.grid(row=4, columnspan=5)
        
        # Botón para guardar los resultados en un archivo Excel
        self.guardar_button = Button(self.ventana, text="Guardar en Excel", command=self.guardar_resultados)
        self.guardar_button.grid(row=5, column=0, columnspan=5)

        # Sección de conclusión
        self.conclusion_label = Label(self.ventana, text="Conclusión:")
        self.conclusion_label.grid(row=6, column=0)
        self.conclusion_text = Text(self.ventana, height=13, width=50, state="disabled")
        self.conclusion_text.grid(row=7, columnspan=5, pady=20)
        self.ventana.mainloop()

    def calcular_nuevamente(self):
        self.resultados_tabla.delete(*self.resultados_tabla.get_children())
        self.resultados = []
        self.buscar_documentos()

    def mostrar_conclusion(self):
        self.conclusion_text.config(state="normal")  # Habilitar edición del texto
        self.conclusion_text.delete(1.0, END)
        if len(self.resultados) == 0:
            self.conclusion_text.insert(END, "No se encontraron resultados.")
        else:
            self.resultados.sort(key=lambda x: x[4], reverse=True)  # Ordenar por similitud descendente
            self.conclusion_text.insert(END, "Documentos ordenados\n1. Similitud\n")
            for resultado in self.resultados:
                self.conclusion_text.insert(END, f"Documento #{resultado[0]} - Similitud: {resultado[4]}\n")
            self.resultados.sort(key=lambda x: x[7], reverse=True)  # Ordenar por producto interno normalizado descendente
            self.conclusion_text.insert(END, "\n2. Producto Interno Normalizado (PIN):\n")
            for resultado in self.resultados:
                self.conclusion_text.insert(END, f"Documento #{resultado[0]} - PIN: {resultado[7]}\n")
            

        self.conclusion_text.config(state="disabled")  # Deshabilitar edición del texto

    
    def definir_vocabulario(self):
        vocabulario_texto = self.vocabulario_entry.get()
        self.vocabulario = vocabulario_texto.split()
        print("Vocabulario definido:", self.vocabulario)
        
    def cargar_vocabulario(self):
        archivo = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        with open(archivo, 'r') as f:
            vocabulario_texto = f.read()
            # Eliminar tildes, convertir a minúsculas y eliminar plurales del vocabulario
            vocabulario_texto = unidecode(vocabulario_texto.lower())
            vocabulario_texto = self.eliminar_plurales(vocabulario_texto)
        
        self.vocabulario_entry.delete(0, END)
        self.vocabulario_entry.insert(END, vocabulario_texto)
        self.definir_vocabulario()
        
    def definir_documentos(self):
        documentos_texto = self.documentos_entry.get()
        self.documentos = documentos_texto.splitlines()
        print("Documentos definidos:", self.documentos)
        
    
    def cargar_documentos(self):
        archivo = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        with open(archivo, 'r') as f:
            documentos_texto = f.readlines()
            documentos_texto = [documento.strip() for documento in documentos_texto]  # Eliminar espacios en blanco al inicio y final de cada línea
            documentos_texto = [unidecode(documento.lower()) for documento in documentos_texto]  # Eliminar tildes y convertir a minúsculas
            documentos_texto = [self.eliminar_plurales(documento) for documento in documentos_texto]  # Eliminar plurales de los documentos
        
        self.documentos_entry.delete(0, END)
        self.documentos_entry.insert(END, '\n'.join(documentos_texto))
        self.definir_documentos()
        
    def cargar_stopwords(self):
        archivo = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        with open(archivo, 'r') as f:
            stopwords_texto = f.read()
        self.stopwords_entry.delete(0, END)
        self.stopwords_entry.insert(END, stopwords_texto)
        self.stopwords = stopwords_texto.split()
        print("Stopwords cargados:", self.stopwords)
        self.vocabulario = [palabra for palabra in self.vocabulario if palabra not in self.stopwords]
        self.vocabulario = [re.sub(r'[^\w\s]+', '', palabra) for palabra in self.vocabulario]
        print("Vocabulario después de eliminar stopwords:", self.vocabulario)
        self.documentos = [palabra for palabra in self.documentos if palabra not in self.stopwords]
        self.documentos = [re.sub(r'[^\w\s]+', '', palabra) for palabra in self.documentos]
        print("Documento después de eliminar stopwords:", self.documentos)
    

    def buscar_documentos(self):
        consulta = self.consulta_entry.get()
        consulta_vector = self.calcular_vector(consulta)

        self.resultados = []
        for i, documento in enumerate(self.documentos):
            documento_vector = self.calcular_vector(documento)
            producto_interno = self.calcular_producto_interno(consulta_vector, documento_vector) #q*d
            magnitud_documento = self.calcular_magnitud(documento_vector)
            magnitud_consulta = self.calcular_magnitud(consulta_vector)
            if magnitud_consulta == 0 or magnitud_documento == 0:
                similitud = 0  # O cualquier valor predeterminado que desees asignar en caso de división por cero
            else:
                similitud = round(producto_interno / (magnitud_consulta * magnitud_documento), 3)
            producto_modulos = self.calcular_producto_interno(consulta_vector, documento_vector)
            numero_palabras = len(documento.split())
            producto_interno_normalizado = round(producto_interno / (numero_palabras if numero_palabras != 0 else 1), 3)
            self.resultados.append([i + 1, producto_interno, magnitud_documento, magnitud_consulta, similitud, producto_modulos, numero_palabras, producto_interno_normalizado])
        
        
        self.mostrar_resultados()
        self.mostrar_conclusion()
    def calcular_vector(self, texto):
        vector = []
        for palabra in self.vocabulario:
            frecuencia = texto.lower().split().count(palabra)
            vector.append(frecuencia)
        return vector
    
    def calcular_producto_interno(self, vector1, vector2):
        producto = 0
        for i in range(len(vector1)):
            producto += vector1[i] * vector2[i]
        return producto
    
    def calcular_magnitud(self, vector):
        suma_cuadrados = sum([x**2 for x in vector])
        return round(math.sqrt(suma_cuadrados),3)
    
    def mostrar_resultados(self):
        self.resultados_tabla.delete(*self.resultados_tabla.get_children())
        for resultado in self.resultados:
            self.resultados_tabla.insert("", END, text=resultado[0], values=(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6], resultado[7]))
    
    def limpiar_campos(self):
        self.vocabulario_entry.delete(0, END)
        self.documentos_entry.delete(0, END)
        self.consulta_entry.delete(0, END)
        self.stopwords_entry.delete(0, END)
        self.resultados_tabla.delete(*self.resultados_tabla.get_children())
        self.vocabulario = []
        self.documentos = []
        self.resultados = []
        self.conclusion_text.config(state="normal")
        self.conclusion_text.delete(1.0, END)
        self.conclusion_text.config(state="disable")

    def eliminar_plurales(self, texto):
        palabras = texto.split()
        palabras_singular = []
        for palabra in palabras:
            # Eliminar plurales conservando solo la raíz de la palabra
            if palabra.endswith("s"):
                palabra = palabra[:-1]
            palabras_singular.append(palabra)
        return ' '.join(palabras_singular)

    def guardar_resultados(self):
        if not self.resultados:
            return
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
        if archivo:
            df = pd.DataFrame(self.resultados, columns=["Documento", "Producto Interno", "Magnitud Documento", "Magnitud Consulta", "Similitud", "Producto de Módulos", "Número de Palabras", "Producto Interno Normalizado"])
            df.to_excel(archivo, index=False)
            print("Resultados guardados en:", archivo)


VectorialModelGUI()
