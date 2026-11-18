import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from markitdown import MarkItDown

# Inicializa el motor de MarkItDown
md = MarkItDown()
texto_convertido_actual = ""
nombre_archivo_actual = "resultado.md"

def seleccionar_archivo():
    global texto_convertido_actual, nombre_archivo_actual
    
    ruta = filedialog.askopenfilename(
        title="Selecciona un documento para convertir",
        filetypes=[
            ("Todos los soportados", "*.pdf *.docx *.xlsx *.pptx *.html *.txt *.csv *.json *.xml *.jpg *.png"),
            ("Todos los archivos", "*.*")
        ]
    )
    if not ruta:
        return

    etiqueta_estado.config(text="⏳ Convirtiendo archivo...", fg="#f39c12")
    ventana.update()

    try:
        resultado = md.convert(ruta)
        texto_convertido_actual = resultado.text_content
        nombre_base = os.path.splitext(os.path.basename(ruta))[0]
        nombre_archivo_actual = f"{nombre_base}.md"

        # Mostrar vista previa en el cuadro de texto
        caja_texto.delete("1.0", tk.END)
        caja_texto.insert(tk.END, texto_convertido_actual)

        etiqueta_estado.config(text=f"✅ Convertido: {os.path.basename(ruta)}", fg="#2ecc71")
        boton_guardar.config(state=tk.NORMAL)
    except Exception as e:
        etiqueta_estado.config(text="❌ Error al convertir", fg="#e74c3c")
        messagebox.showerror("Error de conversión", f"No se pudo procesar el archivo:\n{e}")

def guardar_markdown():
    if not texto_convertido_actual:
        return

    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".md",
        initialfile=nombre_archivo_actual,
        filetypes=[("Archivo Markdown", "*.md"), ("Texto plano", "*.txt")],
        title="Guardar archivo Markdown como..."
    )
    if ruta_guardado:
        with open(ruta_guardado, "w", encoding="utf-8") as f:
            f.write(texto_convertido_actual)
        messagebox.showinfo("Guardado", "¡Archivo Markdown guardado correctamente!")

# Configuración de la ventana principal de Windows
ventana = tk.Tk()
ventana.title("MarkItDown - Conversor Desktop")
ventana.geometry("680x500")
ventana.configure(bg="#1e1e1e")

# Encabezado y botones superiores
marco_superior = tk.Frame(ventana, bg="#1e1e1e", pady=12)
marco_superior.pack(fill=tk.X, padx=15)

boton_abrir = tk.Button(
    marco_superior, text="📂 Seleccionar Archivo", command=seleccionar_archivo,
    bg="#0078d4", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6, relief=tk.FLAT, cursor="hand2"
)
boton_abrir.pack(side=tk.LEFT)

boton_guardar = tk.Button(
    marco_superior, text="💾 Guardar .md", command=guardar_markdown,
    bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=6, relief=tk.FLAT, cursor="hand2", state=tk.DISABLED
)
boton_guardar.pack(side=tk.LEFT, padx=10)

etiqueta_estado = tk.Label(marco_superior, text="Listo para convertir", bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 9))
etiqueta_estado.pack(side=tk.RIGHT)

# Área de vista previa del Markdown generado
caja_texto = scrolledtext.ScrolledText(
    ventana, wrap=tk.WORD, bg="#252526", fg="#d4d4d4",
    font=("Consolas", 10), insertbackground="white", relief=tk.FLAT, padx=10, pady=10
)
caja_texto.pack(expand=True, fill=tk.BOTH, padx=15, pady=(0, 15))

ventana.mainloop()
