import customtkinter as ctk
from tkinter import messagebox
import joblib
import numpy as np
import pandas as pd
from PIL import Image
import os

# Configurar apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class InterfazRefraccion(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Predictor Ojeda-Belette de Coeficiente de Refracción KL")
        self.geometry("800x700")
        self.resizable(True, True)
        
        # Cargar modelo y componentes
        self.cargar_modelo()
        
        # Crear interfaz
        self.crear_interfaz()
        
    def cargar_modelo(self):
        """Cargar el modelo entrenado y sus componentes"""
        try:
            self.modelo = joblib.load('C:\\Users\\Nene\\Downloads\\Modelo Belette\\modelo_refraccion.pkl')
            self.scaler = joblib.load('C:\\Users\\Nene\\Downloads\\Modelo Belette\\scaler_refraccion.pkl')
            self.error_medio = joblib.load('C:\\Users\\Nene\\Downloads\\Modelo Belette\\error_medio.pkl')
            self.error_maximo = joblib.load('C:\\Users\\Nene\\Downloads\\Modelo Belette\\error_maximo.pkl')
            self.columnas = joblib.load('C:\\Users\\Nene\\Downloads\\Modelo Belette\\columnas_modelo.pkl')
            self.modelo_cargado = True
            print(" Modelo cargado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el modelo: {str(e)}")
            self.modelo_cargado = False
    
    def crear_interfaz(self):
        """Crear todos los elementos de la interfaz"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(
            self.main_frame, 
            text="PREDICTOR OJEDA-BELETTE DE COEFICIENTE DE REFRACCIÓN (KL)",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame de entrada de datos
        self.crear_seccion_entrada()
        
        # Frame de resultados
        self.crear_seccion_resultados()
        
        # Frame de información del modelo
        self.crear_seccion_informacion()
        
    def crear_seccion_entrada(self):
        """Crear sección para entrada de datos"""
        entrada_frame = ctk.CTkFrame(self.main_frame)
        entrada_frame.pack(fill="x", padx=10, pady=10)
        
        titulo_entrada = ctk.CTkLabel(
            entrada_frame, 
            text="DATOS DE ENTRADA",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo_entrada.pack(pady=10)
        
        # Grid para inputs
        grid_frame = ctk.CTkFrame(entrada_frame)
        grid_frame.pack(padx=20, pady=10, fill="x")
        
        # Hora
        self.lbl_hora = ctk.CTkLabel(grid_frame, text="Hora del día (6-18):")
        self.lbl_hora.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ent_hora = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 10")
        self.ent_hora.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Altura
        self.lbl_altura = ctk.CTkLabel(grid_frame, text="Altura (m):")
        self.lbl_altura.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ent_altura = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 250.0")
        self.ent_altura.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Temperatura
        self.lbl_temp = ctk.CTkLabel(grid_frame, text="Temperatura (°C):")
        self.lbl_temp.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ent_temp = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 28.0")
        self.ent_temp.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Presión
        self.lbl_presion = ctk.CTkLabel(grid_frame, text="Presión (hPa):")
        self.lbl_presion.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ent_presion = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 745.0")
        self.ent_presion.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # Humedad
        self.lbl_humedad = ctk.CTkLabel(grid_frame, text="Humedad (%):")
        self.lbl_humedad.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ent_humedad = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 14.0")
        self.ent_humedad.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # Gradiente
        self.lbl_gradiente = ctk.CTkLabel(grid_frame, text="Gradiente Vertical:")
        self.lbl_gradiente.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.ent_gradiente = ctk.CTkEntry(grid_frame, placeholder_text="Ej: 0.11")
        self.ent_gradiente.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        # Configurar peso de columnas
        grid_frame.columnconfigure(1, weight=1)
        
        # Botones
        btn_frame = ctk.CTkFrame(entrada_frame)
        btn_frame.pack(pady=15)
        
        self.btn_predecir = ctk.CTkButton(
            btn_frame, 
            text="CALCULAR PREDICCIÓN", 
            command=self.predecir,
            font=ctk.CTkFont(weight="bold"),
            height=40
        )
        self.btn_predecir.pack(side="left", padx=10)
        
        self.btn_limpiar = ctk.CTkButton(
            btn_frame, 
            text="LIMPIAR CAMPOS", 
            command=self.limpiar_campos,
            fg_color="gray",
            hover_color="darkgray",
            height=40
        )
        self.btn_limpiar.pack(side="left", padx=10)
        
        # Insertar datos de ejemplo
        self.insertar_datos_ejemplo()
    
    def crear_seccion_resultados(self):
        """Crear sección para mostrar resultados"""
        self.resultados_frame = ctk.CTkFrame(self.main_frame)
        self.resultados_frame.pack(fill="x", padx=10, pady=10)
        
        titulo_resultados = ctk.CTkLabel(
            self.resultados_frame, 
            text="RESULTADOS DE LA PREDICCIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo_resultados.pack(pady=10)
        
        # Frame para resultados principales
        resultados_grid = ctk.CTkFrame(self.resultados_frame)
        resultados_grid.pack(padx=20, pady=10, fill="x")
        
        # Predicción principal
        self.lbl_prediccion = ctk.CTkLabel(
            resultados_grid, 
            text="KL Predicho: --",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_prediccion.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Margen de error
        self.lbl_margen = ctk.CTkLabel(
            resultados_grid, 
            text="Margen de error: ± --",
            font=ctk.CTkFont(size=14)
        )
        self.lbl_margen.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Rango probable
        self.lbl_rango = ctk.CTkLabel(
            resultados_grid, 
            text="Rango probable: -- - --",
            font=ctk.CTkFont(size=12)
        )
        self.lbl_rango.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Interpretación
        self.lbl_interpretacion = ctk.CTkLabel(
            resultados_grid, 
            text="Interpretación: --",
            font=ctk.CTkFont(size=12),
            wraplength=400
        )
        self.lbl_interpretacion.grid(row=3, column=0, columnspan=2, pady=10)
        
    def crear_seccion_informacion(self):
        """Crear sección de información del modelo"""
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        titulo_info = ctk.CTkLabel(
            info_frame, 
            text="INFORMACIÓN DEL MODELO",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_info.pack(pady=5)
        
        if self.modelo_cargado:
            info_text = f" Modelo cargado - Error medio: {self.error_medio:.4f}"
        else:
            info_text = " Modelo no disponible"
            
        self.lbl_info_modelo = ctk.CTkLabel(
            info_frame, 
            text=info_text,
            font=ctk.CTkFont(size=12)
        )
        self.lbl_info_modelo.pack(pady=5)
    
    def insertar_datos_ejemplo(self):
        """Insertar datos de ejemplo en los campos"""
        self.ent_hora.insert(0, "10")
        self.ent_altura.insert(0, "250")
        self.ent_temp.insert(0, "28")
        self.ent_presion.insert(0, "745")
        self.ent_humedad.insert(0, "14")
        self.ent_gradiente.insert(0, "0.11")
    
    def limpiar_campos(self):
        """Limpiar todos los campos de entrada"""
        self.ent_hora.delete(0, 'end')
        self.ent_altura.delete(0, 'end')
        self.ent_temp.delete(0, 'end')
        self.ent_presion.delete(0, 'end')
        self.ent_humedad.delete(0, 'end')
        self.ent_gradiente.delete(0, 'end')
        
        # Restaurar ejemplo
        self.insertar_datos_ejemplo()
        
        # Limpiar resultados
        self.limpiar_resultados()
    
    def limpiar_resultados(self):
        """Limpiar los resultados mostrados"""
        self.lbl_prediccion.configure(text="KL Predicho: --")
        self.lbl_margen.configure(text="Margen de error: ± --")
        self.lbl_rango.configure(text="Rango probable: -- - --")
        self.lbl_interpretacion.configure(text="Interpretación: --")
    
    def validar_datos(self):
        """Validar que todos los datos de entrada sean correctos"""
        try:
            hora = float(self.ent_hora.get())
            altura = float(self.ent_altura.get())
            temperatura = float(self.ent_temp.get())
            presion = float(self.ent_presion.get())
            humedad = float(self.ent_humedad.get())
            gradiente = float(self.ent_gradiente.get())
            
            # Validaciones básicas
            if not (6 <= hora <= 18):
                messagebox.showwarning("Advertencia", "La hora debe estar entre 6 y 18")
                return None
                
            if altura <= 0:
                messagebox.showwarning("Advertencia", "La altura debe ser positiva")
                return None
                
            if gradiente <= 0:
                messagebox.showwarning("Advertencia", "El gradiente debe ser positivo")
                return None
                
            return hora, altura, temperatura, presion, humedad, gradiente
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en todos los campos")
            return None
    
    def predecir(self):
        """Realizar la predicción con los datos ingresados"""
        if not self.modelo_cargado:
            messagebox.showerror("Error", "El modelo no está disponible")
            return
        
        datos = self.validar_datos()
        if datos is None:
            return
        
        hora, altura, temperatura, presion, humedad, gradiente = datos
        
        try:
            # Crear array de entrada
            entrada = np.array([[hora, altura, temperatura, presion, humedad, gradiente]])
            entrada_df = pd.DataFrame(entrada, columns=self.columnas)
            
            # Escalar y predecir
            entrada_escalada = self.scaler.transform(entrada_df)
            prediccion = self.modelo.predict(entrada_escalada)[0]
            
            # Calcular márgenes
            margen_inferior = max(0, prediccion - self.error_medio)
            margen_superior = prediccion + self.error_medio
            
            # Mostrar resultados
            self.mostrar_resultados(prediccion, margen_inferior, margen_superior)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la predicción: {str(e)}")
    
    def mostrar_resultados(self, prediccion, margen_inf, margen_sup):
        """Mostrar los resultados en la interfaz"""
        # Formatear valores
        kl_formateado = f"{prediccion:.4f}"
        margen_formateado = f"{self.error_medio:.4f}"
        rango_formateado = f"{margen_inf:.4f} - {margen_sup:.4f}"
        
        # Actualizar labels
        self.lbl_prediccion.configure(text=f"KL Predicho: {kl_formateado}")
        self.lbl_margen.configure(text=f"Margen de error: ± {margen_formateado}")
        self.lbl_rango.configure(text=f"Rango probable: {rango_formateado}")
        
        # Interpretación
        interpretacion = self.interpretar_kl(prediccion)
        self.lbl_interpretacion.configure(text=f"Interpretación: {interpretacion}")
    
    def interpretar_kl(self, kl):
        """Proporcionar interpretación del valor KL"""
        if kl < 0.1:
            return "Valor muy bajo - Condiciones atmosféricas excepcionales"
        elif kl < 0.14:
            return "Valor bajo - Condiciones favorables"
        elif kl < 0.17:
            return "Valor normal - Condiciones estándar"
        elif kl < 0.2:
            return "Valor moderado - Influencia moderada de refracción"
        elif kl < 0.25:
            return "Valor alto - Refracción significativa"
        else:
            return "Valor muy alto - Condiciones de refracción extrema"

if __name__ == "__main__":
    app = InterfazRefraccion()
    app.mainloop()