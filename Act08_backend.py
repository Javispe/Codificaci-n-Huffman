import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
import pickle

# Variable global para almacenar el árbol de codificación Huffman
arbol_huffman_global = None

def app():
    global lista_frecuencias
    archivo = tk.filedialog.askopenfilename()
    if archivo:
        resultado = contar_caracteres(archivo)
        if resultado:
            print("Caracteres ordenados por cantidad:")
            for caracter, cantidad in resultado:
                print(f"Caracter: {caracter}, Cantidad: {cantidad}")
            archivo_resultado = guardar_resultado(resultado)
            mostrar_archivo(archivo_resultado, root)
            # Almacenar la lista de frecuencias para su uso en el backend
            lista_frecuencias = resultado
            mensaje_label.config(text="Frecuencias calculadas correctamente.", foreground="green")

def contar_caracteres(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    cuenta_caracteres = {}
    for caracter in contenido:
        if caracter in cuenta_caracteres:
            cuenta_caracteres[caracter] += 1
        else:
            cuenta_caracteres[caracter] = 1

    caracteres_ordenados = sorted(cuenta_caracteres.items(), key=lambda x: x[1], reverse=True)
    return caracteres_ordenados

def guardar_resultado(resultado):
    ruta_programa = os.path.dirname(os.path.abspath(__file__))
    ruta_resultado = os.path.join(ruta_programa, 'resultado.txt')

    with open(ruta_resultado, 'w', encoding='utf-8') as f:
        f.write("Caracteres ordenados:\n")
        for caracter, cantidad in resultado:
            f.write(f"Caracter: {caracter}, Cantidad: {cantidad}\n")
    print("El resultado se ha guardado en 'resultado.txt'.")
    return ruta_resultado

def mostrar_archivo(archivo, root):
    # Crea una nueva ventana
    ventana_archivo = tk.Toplevel(root)
    ventana_archivo.title("Resultado")
    
    # Crea un widget Text para mostrar el contenido del archivo
    texto_archivo = tk.Text(ventana_archivo)
    texto_archivo.pack(expand=True, fill='both')
    
    # Abre el archivo y muestra su contenido en el widget Text
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        texto_archivo.insert('1.0', contenido)

# Funciones del backend

# Aqui esta la clase para representar el arbol de huffman 
class NodoHuffman:
    def __init__(self, caracter=None, frecuencia=None):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

# Funcion para construir arbol huffman
def construir_arbol_huffman(lista_frecuencias):
    # Crea nodos hoja para cada caracter y su frecuencia
    nodos = [NodoHuffman(caracter=caracter, frecuencia=frecuencia) for caracter, frecuencia in lista_frecuencias]
    while len(nodos) > 1:
        # Ordena los nodos por frecuencia ascendente
        nodos = sorted(nodos, key=lambda x: x.frecuencia)
        # Toma los dos nodos con menor frecuencia
        nodo_izq = nodos.pop(0)
        nodo_der = nodos.pop(0)
        # Crea un nuevo nodo con la suma de las frecuencias de los nodos tomados
        nuevo_nodo = NodoHuffman(frecuencia=nodo_izq.frecuencia + nodo_der.frecuencia)
        # Asigna los nodos tomados como hijos izquierdo y derecho del nuevo nodo
        nuevo_nodo.izquierda = nodo_izq
        nuevo_nodo.derecha = nodo_der
        # Agrega el nuevo nodo a la lista de nodos
        nodos.append(nuevo_nodo)
    # Al final, el último nodo restante en la lista es la raíz del árbol de codificación Huffman
    return nodos[0]

def generar_tabla_codigos(root, codigo='', tabla_codigos={}):
    # Verifica si el nodo actual no es nulo
    if root is not None:
        # Si el nodo actual es una hoja (tiene un caracter), agrega su código a la tabla de códigos
        if root.caracter is not None:
            tabla_codigos[root.caracter] = codigo
        # Recursivamente genera los códigos para los hijos izquierdo y derecho del nodo actual
        generar_tabla_codigos(root.izquierda, codigo + '0', tabla_codigos)
        generar_tabla_codigos(root.derecha, codigo + '1', tabla_codigos)
    # Devuelve la tabla de códigos actualizada
    return tabla_codigos

def comprimir_archivo(archivo_entrada, archivo_salida, tabla_codigos):
    with open(archivo_entrada, 'r', encoding='utf-8') as f_entrada, open(archivo_salida, 'wb') as f_salida:
        bits = ''  # Variable para almacenar los bits comprimidos
        while True:
            caracter = f_entrada.read(1)  # Lee un solo carácter
            if not caracter:  # Si no hay más caracteres, termina el bucle
                break
            bits += tabla_codigos[caracter]  # Agrega el código Huffman del carácter a la secuencia de bits
            while len(bits) >= 8:
                byte = bits[:8]  # Toma los primeros 8 bits
                bits = bits[8:]  # Elimina los primeros 8 bits de la secuencia
                # Escribe el byte en el archivo de salida como un byte binario
                f_salida.write(bytes([int(byte, 2)]))
        # Si aún quedan bits por escribir en el archivo de salida
        if bits:
            bits += '0' * (8 - len(bits) % 8)  # Rellena los bits faltantes con ceros
            f_salida.write(bytes([int(bits, 2)]))  # Escribe el último byte en el archivo de salida

# Abre el archivo en modo escritura binaria y utiliza pickle para serializar y guardar el árbol
def guardar_arbol_huffman(arbol, archivo):
    with open(archivo, 'wb') as f:
        pickle.dump(arbol, f)

# Abre el archivo en modo lectura binaria y utiliza pickle para deserializar y cargar el árbol
def cargar_arbol_huffman(archivo):
    with open(archivo, 'rb') as f:
        return pickle.load(f)

def descomprimir_archivo(archivo_comprimido, archivo_descomprimido):
     # Carga el árbol de codificación Huffman desde el archivo 'arbol_huffman.pkl'
    arbol_huffman = cargar_arbol_huffman('arbol_huffman.pkl')

    # Abre el archivo comprimido en modo lectura binaria y el archivo descomprimido en modo escritura de texto
    with open(archivo_comprimido, 'rb') as f_comprimido, open(archivo_descomprimido, 'w', encoding='utf-8') as f_descomprimido:
        nodo_actual = arbol_huffman  # Inicializa el nodo actual como la raíz del árbol

        bits = ''  # Variable para almacenar los bits leídos del archivo comprimido

        # Itera sobre cada byte en el archivo comprimido
        byte = f_comprimido.read(1)
        while byte:
            bits += f"{ord(byte):08b}"  # Convierte el byte en una secuencia de bits

            while bits:
                if bits[0] == '0':
                    nodo_actual = nodo_actual.izquierda
                else:
                    nodo_actual = nodo_actual.derecha
                
                bits = bits[1:]  # Elimina el primer bit de la secuencia

                if nodo_actual.caracter is not None:
                    f_descomprimido.write(nodo_actual.caracter)
                    nodo_actual = arbol_huffman  # Reinicia el nodo actual al inicio del árbol
                    
            # Lee el siguiente byte del archivo comprimido
            byte = f_comprimido.read(1)

        # Cierra el archivo descomprimido al finalizar
        f_descomprimido.close()

def comprimir():
    global lista_frecuencias  
    if lista_frecuencias is None:
        mensaje_label.config(text="Primero debes seleccionar un archivo.", foreground="red")
        return
    
    # Solicita al usuario que seleccione un archivo
    ruta_archivo = tk.filedialog.askopenfilename()
    
    if not ruta_archivo:
        mensaje_label.config(text="No se seleccionó ningún archivo.", foreground="red")
        return
    # Define la ruta para el archivo comprimido agregando la extensión '.huffman'
    ruta_archivo_comprimido = ruta_archivo + '.huffman'

    # Construye el árbol de codificación Huffman utilizando las frecuencias de caracteres previamente calculadas
    arbol_huffman = construir_arbol_huffman(lista_frecuencias)

    # Genera la tabla de códigos Huffman utilizando el árbol de codificación Huffman
    tabla_codigos = generar_tabla_codigos(arbol_huffman)

    # Comprime el archivo seleccionado utilizando la tabla de códigos Huffman y guarda el archivo comprimido
    comprimir_archivo(ruta_archivo, ruta_archivo_comprimido, tabla_codigos)

    # Guarda el árbol de codificación Huffman en un archivo binario para su uso posterior
    guardar_arbol_huffman(arbol_huffman, 'arbol_huffman.pkl')

    mensaje_label.config(text="Compresión correcta. Archivo comprimido guardado.", foreground="green")

def descomprimir():
    # Solicita al usuario que seleccione un archivo comprimido
    ruta_archivo_comprimido = tk.filedialog.askopenfilename()
    
    if not ruta_archivo_comprimido:
        mensaje_label.config(text="No se seleccionó ningún archivo.", foreground="red")
        return

    # Determina la ruta del archivo descomprimido reemplazando la extensión '.huffman' por '_descomprimido.txt'
    ruta_archivo_descomprimido = ruta_archivo_comprimido.replace('.huffman', '_descomprimido.txt')
    
    descomprimir_archivo(ruta_archivo_comprimido, ruta_archivo_descomprimido)
    
    mensaje_label.config(text="Descompresión correcta. Archivo descomprimido guardado.", foreground="green")

def main():
    global root
    root = tk.Tk()
    root.title("Árbol de Huffman / Comprimir y descomprimir")

    # Establecer el estilo de los widgets
    estilo = ttk.Style()
    estilo.configure('TLabel', font=('Helvetica', 12))
    estilo.configure('TButton', font=('Helvetica', 12))

    # Calcula el tamaño de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    # Calcula las dimensiones de la ventana a la mitad de la pantalla
    ancho_ventana = ancho_pantalla // 2
    alto_ventana = alto_pantalla // 2

    # Posiciona la ventana en el centro de la pantalla
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2

    # Establece la geometría de la ventana
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    frm = ttk.Frame(root, padding=10)
    frm.pack(expand=True, fill='both')

    ttk.Label(frm, text="Contador de caracteres").pack()

    btn_abrir = ttk.Button(frm, text="Examinar", command=app)
    btn_abrir.pack(side='top', padx=5, pady=5)

    btn_comprimir = ttk.Button(frm, text="Comprimir", command=comprimir)
    btn_comprimir.pack(side='top', padx=5, pady=5)

    btn_descomprimir = ttk.Button(frm, text="Descomprimir", command=descomprimir)
    btn_descomprimir.pack(side='top', padx=5, pady=5)

    # Crear la etiqueta para mostrar el mensaje
    global mensaje_label
    mensaje_label = ttk.Label(frm, text="", font=('Helvetica', 12))
    mensaje_label.pack(side='top', padx=5, pady=5)

    root.mainloop()

main()
