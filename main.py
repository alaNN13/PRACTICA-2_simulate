import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import time

def main():
    root = tk.Tk()
    root.title("Simulador Avanzado AFD - Proyecto TC")
    root.geometry("950x700")
    root.eval('tk::PlaceWindow . center')
    root.configure(bg="#f0f2f5") # Color de fondo moderno

    # ==========================================
    # ESTILOS MODERNOS (El "Lavado de Cara")
    # ==========================================
    style = ttk.Style()
    # Usamos 'clam' que es mucho más limpio que el estilo por defecto de Windows
    style.theme_use('clam') 
    
    style.configure("TFrame", background="#f0f2f5")
    style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1a365d")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#2b6cb0", foreground="white")
    style.map("TButton", background=[("active", "#2c5282")]) # Efecto Hover
    style.configure("TLabelframe", background="#ffffff", borderwidth=2)
    style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground="#2d3748", background="#ffffff")
    
    # Estilo de la tabla interactiva
    style.configure("Treeview", font=("Consolas", 10), rowheight=30, borderwidth=0)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e2e8f0", foreground="#1a202c")
    style.map("Treeview", background=[("selected", "#bee3f8")], foreground=[("selected", "#2b6cb0")])

    # ==========================================
    # FUNCIÓN DE CARGA E INTERACTIVIDAD
    # ==========================================
    def escribir_consola(mensaje):
        """Escribe en la consola interactiva con efecto de máquina de escribir"""
        consola.config(state=tk.NORMAL)
        consola.insert(tk.END, f"> {mensaje}\n")
        consola.see(tk.END)
        consola.config(state=tk.DISABLED)
        root.update()
        time.sleep(0.1) # Pequeña pausa para dar efecto de "procesamiento"

    def cargar_archivo():
        ruta = filedialog.askopenfilename(
            title="Descubre tu Autómata",
            filetypes=[("Archivos JSON", "*.json")]
        )
        
        if not ruta:
            return
            
        try:
            consola.config(state=tk.NORMAL)
            consola.delete(1.0, tk.END)
            consola.config(state=tk.DISABLED)
            
            escribir_consola(f"Iniciando análisis del archivo...")
            
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            escribir_consola("JSON descifrado correctamente.")
            
            # Interactividad visual de los datos
            alfabeto = datos.get('alfabeto', [])
            escribir_consola(f"Extrayendo alfabeto Σ = {{ {', '.join(alfabeto)} }}")
            lbl_alfabeto.config(text=f"Σ = {{ {', '.join(alfabeto)} }}")
            
            nombres_estados = [e['nombre'] for e in datos.get('estados', [])]
            escribir_consola(f"Identificando conjunto de estados Q... ({len(nombres_estados)} encontrados)")
            lbl_estados.config(text=f"Q = {{ {', '.join(nombres_estados)} }}")
            
            lbl_inicial.config(text=f"q0 = {datos.get('inicial', '')}")
            lbl_finales.config(text=f"F = {{ {', '.join(datos.get('finales', []))} }}")
            
            # Limpiar y rellenar tabla
            for item in tabla_transiciones.get_children():
                tabla_transiciones.delete(item)
                
            escribir_consola("Mapeando función de transición δ...")
            for i, t in enumerate(datos.get("transiciones", [])):
                # Alternar colores en las filas para mejor lectura
                tag = 'par' if i % 2 == 0 else 'impar'
                tabla_transiciones.insert("", tk.END, values=(f"δ({t['de']}, {t['lee']})", "→", t["a"]), tags=(tag,))
            
            tabla_transiciones.tag_configure('par', background='#f7fafc')
            tabla_transiciones.tag_configure('impar', background='#ffffff')
            
            escribir_consola("¡Autómata ensamblado y listo para simulación!")
            messagebox.showinfo("Éxito", "El autómata ha sido cargado y analizado por completo.")
            
        except Exception as e:
            escribir_consola(f"[ERROR CRÍTICO] {str(e)}")
            messagebox.showerror("Error", "El archivo está corrupto o no es válido.")

    # ==========================================
    # INTERFAZ GRÁFICA (GUI)
    # ==========================================
    # Encabezado
    header_frame = ttk.Frame(root, padding=15)
    header_frame.pack(fill='x')
    ttk.Label(header_frame, text="Simulador de Autómatas Finitos Deterministas", style="Header.TLabel").pack()
    ttk.Label(header_frame, text="Motor de Análisis y Validación de Cadenas").pack()

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    # --- PESTAÑA 1: IMPORTACIÓN MAGISTRAL ---
    tab1 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab1, text=" ⚙️ Definición y Carga ")

    # Panel Izquierdo: Controles e Información
    panel_izq = ttk.Frame(tab1)
    panel_izq.pack(side=tk.LEFT, fill='y', padx=15, pady=15)

    ttk.Button(panel_izq, text="🔍 Explorar Archivo .JSON", command=cargar_archivo).pack(fill='x', pady=(0, 15), ipady=5)

    frame_info = ttk.LabelFrame(panel_izq, text=" 5 Tuplas del Autómata ")
    frame_info.pack(fill='both', expand=True)
    
    # Textos con formato matemático
    ttk.Label(frame_info, text="Alfabeto:", font=("Segoe UI", 9, "italic")).pack(anchor='w', padx=10, pady=(10,0))
    lbl_alfabeto = ttk.Label(frame_info, text="Σ = { }", font=("Consolas", 12, "bold"), foreground="#2b6cb0")
    lbl_alfabeto.pack(anchor='w', padx=10)

    ttk.Label(frame_info, text="Estados:", font=("Segoe UI", 9, "italic")).pack(anchor='w', padx=10, pady=(10,0))
    lbl_estados = ttk.Label(frame_info, text="Q = { }", font=("Consolas", 11, "bold"), foreground="#2b6cb0")
    lbl_estados.pack(anchor='w', padx=10)

    ttk.Label(frame_info, text="Estado Inicial:", font=("Segoe UI", 9, "italic")).pack(anchor='w', padx=10, pady=(10,0))
    lbl_inicial = ttk.Label(frame_info, text="q0 = ", font=("Consolas", 12, "bold"), foreground="#38a169")
    lbl_inicial.pack(anchor='w', padx=10)

    ttk.Label(frame_info, text="Estados de Aceptación:", font=("Segoe UI", 9, "italic")).pack(anchor='w', padx=10, pady=(10,0))
    lbl_finales = ttk.Label(frame_info, text="F = { }", font=("Consolas", 12, "bold"), foreground="#e53e3e")
    lbl_finales.pack(anchor='w', padx=10, pady=(0, 10))

    # Panel Derecho: Tabla y Consola
    panel_der = ttk.Frame(tab1)
    panel_der.pack(side=tk.RIGHT, fill='both', expand=True, padx=15, pady=15)

    frame_tabla = ttk.LabelFrame(panel_der, text=" Función de Transición Interactiva ")
    frame_tabla.pack(fill='both', expand=True, pady=(0, 10))

    tabla_transiciones = ttk.Treeview(frame_tabla, columns=("origen", "flecha", "destino"), show="headings")
    tabla_transiciones.heading("origen", text="Estado Actual + Lectura")
    tabla_transiciones.heading("flecha", text="")
    tabla_transiciones.heading("destino", text="Estado Siguiente")
    tabla_transiciones.column("origen", anchor='center', width=200)
    tabla_transiciones.column("flecha", anchor='center', width=50)
    tabla_transiciones.column("destino", anchor='center', width=150)
    
    scroll_tabla = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_transiciones.yview)
    tabla_transiciones.configure(yscroll=scroll_tabla.set)
    scroll_tabla.pack(side=tk.RIGHT, fill=tk.Y)
    tabla_transiciones.pack(fill='both', expand=True, padx=2, pady=2)

    # Consola tipo "Hacker"
    frame_consola = ttk.LabelFrame(panel_der, text=" Consola de Eventos ")
    frame_consola.pack(fill='x')
    consola = tk.Text(frame_consola, height=6, bg="#1a202c", fg="#48bb78", font=("Consolas", 10), state=tk.DISABLED)
    consola.pack(fill='both', expand=True, padx=2, pady=2)

    # --- PESTAÑA 2 y 3 (Estructuras listas para mañana) ---
    tab2 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab2, text=" 🎯 Simulación Paso a Paso ")
    ttk.Label(tab2, text="Aquí programaremos la lógica de la validación mañana...", font=("Segoe UI", 12, "italic")).pack(pady=50)

    tab3 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab3, text=" 🛠️ Herramientas Kleene & Subcadenas ")
    ttk.Label(tab3, text="Aquí programaremos la lógica de las herramientas extra...", font=("Segoe UI", 12, "italic")).pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()