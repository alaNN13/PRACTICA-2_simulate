import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import time
import itertools

# Variable global para guardar el autómata en memoria
automata_actual = None 

# ==========================================
# LÓGICA MATEMÁTICA (El Cerebro)
# ==========================================
def simular_afd(datos_json, cadena):
    estado_actual = datos_json.get("inicial")
    transiciones = datos_json.get("transiciones", [])
    estados_finales = datos_json.get("finales", [])
    traza = []

    traza.append(f"Inicio en q0: {estado_actual}")

    for simbolo in cadena:
        encontrada = False
        for t in transiciones:
            if t["de"] == estado_actual and t["lee"] == simbolo:
                estado_anterior = estado_actual
                estado_actual = t["a"]
                traza.append(f"δ({estado_anterior}, '{simbolo}') ➔ {estado_actual}")
                encontrada = True
                break
        
        if not encontrada:
            traza.append(f" Error: El estado {estado_actual} no sabe qué hacer con '{simbolo}'")
            return False, traza

    es_aceptada = estado_actual in estados_finales
    return es_aceptada, traza

# ==========================================
# INTERFAZ GRÁFICA Y EVENTOS
# ==========================================
def main():
    root = tk.Tk()
    root.title("Simulador Avanzado AFD - Proyecto TC")
    root.geometry("950x700")
    root.eval('tk::PlaceWindow . center')
    root.configure(bg="#f0f2f5")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TFrame", background="#f0f2f5")
    style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1a365d")
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#2b6cb0", foreground="white")
    style.map("TButton", background=[("active", "#2c5282")])
    style.configure("TLabelframe", background="#ffffff", borderwidth=2)
    style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground="#2d3748", background="#ffffff")
    style.configure("Treeview", font=("Consolas", 10), rowheight=30)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e2e8f0")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=20, pady=(15, 20))

    # ------------------------------------------
    # PESTAÑA 1: CARGA DE AUTÓMATA
    # ------------------------------------------
    tab1 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab1, text=" ⚙️ 1. Carga de Autómata ")

    def escribir_consola(mensaje):
        consola.config(state=tk.NORMAL)
        consola.insert(tk.END, f"> {mensaje}\n")
        consola.see(tk.END)
        consola.config(state=tk.DISABLED)
        root.update()
        time.sleep(0.05)

    def cargar_archivo():
        global automata_actual
        ruta = filedialog.askopenfilename(title="Carga tu JSON", filetypes=[("Archivos JSON", "*.json")])
        if not ruta: return
            
        try:
            consola.config(state=tk.NORMAL)
            consola.delete(1.0, tk.END)
            consola.config(state=tk.DISABLED)
            
            with open(ruta, 'r', encoding='utf-8') as f:
                automata_actual = json.load(f)
            
            alfabeto = automata_actual.get('alfabeto', [])
            nombres_estados = [e['nombre'] for e in automata_actual.get('estados', [])]
            
            lbl_alfabeto.config(text=f"Σ = {{ {', '.join(alfabeto)} }}")
            lbl_estados.config(text=f"Q = {{ {', '.join(nombres_estados)} }}")
            lbl_inicial.config(text=f"q0 = {automata_actual.get('inicial', '')}")
            lbl_finales.config(text=f"F = {{ {', '.join(automata_actual.get('finales', []))} }}")
            
            for item in tabla_transiciones.get_children():
                tabla_transiciones.delete(item)
                
            for i, t in enumerate(automata_actual.get("transiciones", [])):
                tag = 'par' if i % 2 == 0 else 'impar'
                tabla_transiciones.insert("", tk.END, values=(f"δ({t['de']}, {t['lee']})", "→", t["a"]), tags=(tag,))
            
            tabla_transiciones.tag_configure('par', background='#f7fafc')
            tabla_transiciones.tag_configure('impar', background='#ffffff')
            
            escribir_consola("¡Autómata cargado exitosamente! Listo para Pestaña 2.")
            messagebox.showinfo("Éxito", "Autómata listo en memoria.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Archivo inválido: {e}")

    panel_izq = ttk.Frame(tab1)
    panel_izq.pack(side=tk.LEFT, fill='y', padx=15, pady=15)
    ttk.Button(panel_izq, text="🔍 Explorar Archivo .JSON", command=cargar_archivo).pack(fill='x', pady=(0, 15), ipady=5)

    frame_info = ttk.LabelFrame(panel_izq, text=" 5 Tuplas del Autómata ")
    frame_info.pack(fill='both', expand=True)
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

    panel_der = ttk.Frame(tab1)
    panel_der.pack(side=tk.RIGHT, fill='both', expand=True, padx=15, pady=15)
    frame_tabla = ttk.LabelFrame(panel_der, text=" Función de Transición Interactiva ")
    frame_tabla.pack(fill='both', expand=True, pady=(0, 10))
    tabla_transiciones = ttk.Treeview(frame_tabla, columns=("origen", "flecha", "destino"), show="headings")
    tabla_transiciones.heading("origen", text="Estado Actual + Lectura")
    tabla_transiciones.heading("flecha", text="")
    tabla_transiciones.heading("destino", text="Estado Siguiente")
    tabla_transiciones.column("flecha", width=50, anchor='center')
    scroll_tabla = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla_transiciones.yview)
    tabla_transiciones.configure(yscroll=scroll_tabla.set)
    scroll_tabla.pack(side=tk.RIGHT, fill=tk.Y)
    tabla_transiciones.pack(fill='both', expand=True, padx=2, pady=2)
    frame_consola = ttk.LabelFrame(panel_der, text=" Consola de Eventos ")
    frame_consola.pack(fill='x')
    consola = tk.Text(frame_consola, height=5, bg="#1a202c", fg="#48bb78", font=("Consolas", 10), state=tk.DISABLED)
    consola.pack(fill='both', expand=True, padx=2, pady=2)

    # ------------------------------------------
    # PESTAÑA 2: SIMULACIÓN DE CADENAS
    # ------------------------------------------
    tab2 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab2, text="  2. Simulación y Validación ")

    def ejecutar_validacion():
        if not automata_actual:
            messagebox.showwarning("Aviso", "Primero debes cargar un autómata en la Pestaña 1.")
            return
            
        cadena = txt_cadena.get().strip()
        lista_traza.delete(0, tk.END)
        
        es_aceptada, traza = simular_afd(automata_actual, cadena)
        
        for paso in traza:
            lista_traza.insert(tk.END, paso)
            
        if es_aceptada:
            lbl_resultado.config(text="¡CADENA ACEPTADA! ", foreground="#38a169", font=("Segoe UI", 16, "bold"))
            lista_traza.config(bg="#f0fff4") # Fondo verdecito
        else:
            lbl_resultado.config(text="CADENA RECHAZADA ", foreground="#e53e3e", font=("Segoe UI", 16, "bold"))
            lista_traza.config(bg="#fff5f5") # Fondo rojito

    ttk.Label(tab2, text="Ingresa la cadena a evaluar:", font=("Segoe UI", 12)).pack(pady=(30, 5))
    txt_cadena = ttk.Entry(tab2, width=40, font=("Consolas", 14))
    txt_cadena.pack(pady=5)
    ttk.Button(tab2, text=" Validar Cadena", command=ejecutar_validacion).pack(pady=10)
    
    lbl_resultado = ttk.Label(tab2, text="Esperando cadena...", font=("Segoe UI", 14))
    lbl_resultado.pack(pady=10)

    frame_traza = ttk.LabelFrame(tab2, text=" Traza de Recorrido Paso a Paso ")
    frame_traza.pack(fill='both', expand=True, padx=50, pady=20)
    lista_traza = tk.Listbox(frame_traza, font=("Consolas", 12), height=10)
    lista_traza.pack(fill='both', expand=True, padx=10, pady=10)

    # ------------------------------------------
    # PESTAÑA 3: HERRAMIENTAS EXTRA
    # ------------------------------------------
    tab3 = tk.Frame(notebook, bg="#f0f2f5")
    notebook.add(tab3, text="  3. Herramientas Extra ")

    def calcular_extras():
        cad = txt_cadena_extra.get().strip()
        prefijos = [cad[:i] if cad[:i] != "" else "λ" for i in range(len(cad) + 1)]
        sufijos = [cad[i:] if cad[i:] != "" else "λ" for i in range(len(cad) + 1)]
        
        txt_resultados.config(state=tk.NORMAL)
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, f"Prefijos: {', '.join(prefijos)}\n\n")
        txt_resultados.insert(tk.END, f"Sufijos: {', '.join(sufijos)}\n")
        txt_resultados.config(state=tk.DISABLED)

    def calcular_kleene():
        alfabeto = txt_alfabeto_kleene.get().replace(" ", "").split(",")
        try:
            limite = int(txt_limite_kleene.get())
            resultados = []
            for i in range(limite + 1):
                combinaciones = [''.join(p) for p in itertools.product(alfabeto, repeat=i)]
                resultados.extend(combinaciones if i > 0 else ["λ"])
                
            txt_resultados.config(state=tk.NORMAL)
            txt_resultados.delete(1.0, tk.END)
            txt_resultados.insert(tk.END, f"Cerradura Σ* (hasta longitud {limite}):\n\n")
            txt_resultados.insert(tk.END, f"{{ {', '.join(resultados)} }}")
            txt_resultados.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Error", "El límite debe ser un número entero.")

    # Frame Superior (Prefijos/Sufijos)
    f_cadenas = ttk.LabelFrame(tab3, text=" Req 2.4.2: Prefijos y Sufijos ")
    f_cadenas.pack(fill='x', padx=20, pady=15)
    ttk.Label(f_cadenas, text="Cadena:").pack(side=tk.LEFT, padx=10, pady=15)
    txt_cadena_extra = ttk.Entry(f_cadenas, width=30)
    txt_cadena_extra.pack(side=tk.LEFT, padx=5)
    ttk.Button(f_cadenas, text="Calcular", command=calcular_extras).pack(side=tk.LEFT, padx=10)

    # Frame Medio (Kleene)
    f_kleene = ttk.LabelFrame(tab3, text=" Req 2.4.3: Cerradura de Kleene ")
    f_kleene.pack(fill='x', padx=20, pady=5)
    ttk.Label(f_kleene, text="Alfabeto (ej. a,b):").pack(side=tk.LEFT, padx=10, pady=15)
    txt_alfabeto_kleene = ttk.Entry(f_kleene, width=15)
    txt_alfabeto_kleene.pack(side=tk.LEFT, padx=5)
    ttk.Label(f_kleene, text="Longitud:").pack(side=tk.LEFT, padx=10)
    txt_limite_kleene = ttk.Entry(f_kleene, width=10)
    txt_limite_kleene.pack(side=tk.LEFT, padx=5)
    ttk.Button(f_kleene, text="Generar Kleene", command=calcular_kleene).pack(side=tk.LEFT, padx=10)

    # Caja de resultados compartida
    f_resultados = ttk.LabelFrame(tab3, text=" Resultados Generados ")
    f_resultados.pack(fill='both', expand=True, padx=20, pady=15)
    txt_resultados = tk.Text(f_resultados, height=10, font=("Consolas", 11), state=tk.DISABLED)
    txt_resultados.pack(fill='both', expand=True, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()