#Librerias
from tkinter import *
from tkinter import ttk
import tkinter.filedialog

def main():
    # Crear la ventana principal
    root = Tk()
    # Crear un marco dentro de la ventana principal
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    # Título de la ventana principal
    root.title("Act07")
    # Crear una etiqueta de bienvenida 
    ttk.Label(frm, text="Bienvenido a mi compresor de archivo!").grid(column=0, row=0)

    # Estilo para los botones
    style = ttk.Style()
    style.configure("TButton", padding=9, relief="flat", background="#add8e6", foreground="#333333", font=("Arial", 10))

    # Crear botones para abrir, comprimir, descomprimir y salir
    ttk.Button(frm, text="Abrir archivo", command=abrirArchivo, style="BotonAzul.TButton").grid(column=0, row=1, pady=5)
    ttk.Button(frm, text="Comprimir archivo", command=descomprimirArchivo, style="BotonAzul.TButton").grid(column=0, row=2, pady=5)
    ttk.Button(frm, text="Descomprimir archivo", command=comprimirArchivo, style="BotonAzul.TButton").grid(column=0, row=3, pady=5)        
    ttk.Button(frm, text="Salir", command=root.destroy, style="BotonAzul.TButton").grid(column=0, row=4, pady=5)    

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()

# Función para comprimir un archivo (a implementar)
def comprimirArchivo():
    pass

# Función para descomprimir un archivo (a implementar)
def descomprimirArchivo():
    pass

# Función para abrir un archivo
def abrirArchivo():
    # Abrir un cuadro de diálogo para seleccionar un archivo
    ruta_archivo = tkinter.filedialog.askopenfilename(defaultextension='.txt')
    # Verificar si se seleccionó un archivo
    if ruta_archivo:
        # Abrir el archivo seleccionado en modo lectura
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            # Leer el contenido del archivo
            content = archivo.read()

        # Contar la frecuencia de cada carácter en el contenido del archivo
        frequency = {}
        for char in content:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

        # Crear una segunda ventana para mostrar la frecuencia de caracteres
        ventana = Tk()
        # Título de la segunda ventana
        ventana.title("Caracteres")
        frame = ttk.Frame(ventana, padding=10)
        frame.grid()

        # Crear un subtitulo para la lista de frecuencia de caracteres
        ttk.Label(ventana, text="Lista de frecuencia con la que se repite cada caracter").grid(column=0, row=0)

        # Crear un área de texto para mostrar la frecuencia de caracteres
        text_area = Text(ventana, width=40, height=20)
        text_area.grid(column=0, row=1, padx=10, pady=10)

        # Ordenar el diccionario de frecuencia alfabéticamente antes de mostrarlo
        sorted_frequency = sorted(frequency.items(), key=lambda item: item[0])

        # Mostrar cada carácter y su frecuencia en el área de texto
        for char, freq in sorted_frequency:
            # Hacer que la ñ y Ñ se muestren correctamente
            if char == 'ñ':
                char_display = "ñ"
            elif char == 'Ñ':
                char_display = "Ñ"
            else:
                char_display = char
            
            # Reemplazar el espacio con "space"
            if char == ' ':
                char_display = "space"
            
            # Insertar el carácter y su frecuencia en el área de texto
            text_area.insert(END, f"{char_display}: {freq}\n")
        
        # Crear un botón para cerrar la ventana secundaria
        ttk.Button(ventana, text="Salir", command=ventana.destroy).grid(column=0, row=2, pady=10)

        # Iniciar el bucle de la ventana secundaria
        ventana.mainloop()

if __name__ == "__main__":
    main()
