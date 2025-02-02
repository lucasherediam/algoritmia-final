# Modulos estandar de Python
import sys
import io
import operator
import webbrowser
import numpy as np
# Modulos para la interfaz grafica
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# Modulos para Prolog
from pyswip import Prolog
# Modulos para manejo de imagenes
from PIL import Image, ImageTk
# Modulos para graficos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


# ===============================
# Funciones de consulta a Prolog
# ===============================

def list_unique_index(relation):
    """Obtiene una lista única de índices (X) desde una consulta Prolog de una relación unaria."""
    result = list(pl.query(relation + '(X)'))
    return [item['X'] for item in result]


def item_x_prolog(relation):
    """Obtiene los elementos X desde una consulta Prolog para una relación binaria."""
    result = list(pl.query(f'{relation}(X,Y)'))
    return [item['X'] for item in result]


def item_y_prolog(relation):
    """Obtiene los elementos Y desde una consulta Prolog para una relación binaria."""
    result = list(pl.query(f'{relation}(X,Y)'))
    return [item['Y'] for item in result]


def team_name(team):
    """Obtiene el nombre de un equipo dado su identificador desde la base de datos Prolog."""
    result = list(pl.query(f"teams({team},Y)"))
    return [item['Y'] for item in result][0]


def get_options(tipo):
    """Obtiene las opciones únicas para un tipo dado desde Prolog."""
    results = item_y_prolog(tipo)
    unique_options = []
    already_used = set()
    for result in results:
        if result not in already_used:
            unique_options.append(result)
            already_used.add(result)
    return unique_options


def questions(types_list):
    """Genera un diccionario con las preguntas, asignándolas según el orden de 'types_list'."""
    i = 0
    option = {}
    result = item_y_prolog('question')
    while i < len(result):
        option[types_list[i]] = result[i]
        i += 1
    return option


# ===============================
# Funciones de la interfaz gráfica
# ===============================

def styles():
    """Configura los estilos de los widgets en la interfaz gráfica."""
    st = ttk.Style()
    st.configure("TLabel", font=('Elephant', 16), foreground="black", padding=15)
    st.configure("TRadiobutton", font=('Arial', 12),
                 foreground="black", background="#C0C0C0", padding=5)
    st.map("TRadiobutton", foreground=[("active", "red"), ("!active", "black")])
    st.configure("TButton", font=('Arial', 12),
                 foreground="black", background="black", padding=5, width=20)


def on_closing():
    """Maneja el evento de cierre de la ventana, pidiendo confirmación antes de salir."""
    if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
        main_window.destroy()
        sys.exit()


def show_questions(index):
    """Muestra la pregunta actual y sus opciones, actualizando la interfaz."""
    if index < len(types):
        current_type = types[index]
        print("aspect:", current_type)
        options = type_option[current_type]
        q = question[current_type]

        # Limpiar el frame de la pregunta anterior
        for widget in frame.winfo_children():
            widget.destroy()
        radio_buttons.clear()

        # Título de la pregunta
        title = ttk.Label(frame, text=q, font=('Segoe UI', 17), background="#DC0000")
        title.pack(pady=10)

        # Si la pregunta es de "character" se muestran imágenes; de lo contrario, texto
        if current_type == "character":
            columns = len(options) // 2 + (len(options) % 2)
            grid_frame = tk.Frame(frame, bg="#C0C0C0")
            grid_frame.pack(pady=10)
            for i, option in enumerate(options):
                row = i // columns
                col = i % columns
                img = load_image(option)
                radio_button = ttk.Radiobutton(grid_frame, image=img, variable=answer, value=option)
                radio_button.image = img  # se guarda la referencia para que no se borre la imagen
                radio_button.grid(row=row, column=col, padx=20, pady=10)
                radio_buttons.append(radio_button)
        else:
            for option in options:
                radio_button = ttk.Radiobutton(frame, text=option, variable=answer, value=option)
                radio_button.pack(anchor=tk.W, padx=70)
                radio_buttons.append(radio_button)

        # Botón para enviar la respuesta
        def send():
            if answer.get() == "":
                messagebox.showerror("Error", "Debes seleccionar una opción.")
            else:
                options_type[current_type] = answer.get()
                answer.set("")
                title.pack_forget()
                for rb in radio_buttons:
                    rb.pack_forget()
                send_button.forget()
                show_questions(index + 1)

        send_button = tk.Button(main_window, text="Enviar respuesta", command=send,
                                font=('Segoe UI', 14), foreground="white",
                                padx=10, pady=5, border=2, background="#DC0000")
        send_button.pack(pady=5)
        send_button.place(x=300, y=385)
    else:
        main_window.destroy()


def load_image(route):
    """Carga y redimensiona una imagen desde una ruta especificada."""
    img = Image.open(route)
    img = img.resize((100, 100))
    return ImageTk.PhotoImage(img)


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Obtiene los datos de una imagen y la convierte en un formato adecuado para su uso en la interfaz gráfica."""
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


# ===============================
# Funciones para mostrar resultados y descripciones
# ===============================

def images_descriptions(teams_list):
    """Muestra descripciones, imágenes y enlaces para los equipos recomendados."""
    descriptions = []
    images_list = []
    links = []

    for team in teams_list:
        result = list(pl.query(f"description({team}, Y)"))
        image_query = list(pl.query(f"image({team}, Y)"))
        link_query = list(pl.query(f"link({team}, Y)"))

        images_list.append([item['Y'] for item in image_query])
        descriptions.append([item['Y'] for item in result])
        links.append([item['Y'] for item in link_query][0])

    columns = []
    layout = []

    for i, team in enumerate(teams_list):
        description_text = "\n".join([f"- {desc}" for desc in descriptions[i]])
        col_description = [
            [sg.Text(team.upper(), font=('Segoe UI', 25), background_color="#C0C0C0", text_color="black")],
            [sg.Text(description_text, auto_size_text=True, font=('Arial', 14),
                     background_color="#C0C0C0", text_color="black")],
            [sg.Button('Go to website', key=f'website_{i}', button_color=("white", "#DC0000"), border_width=2)]
        ]
        col_image = [
            [sg.Image(data=get_img_data(images_list[i][0], maxsize=(220, 400), first=True),
                      background_color="#C0C0C0")]
        ]
        columns.append(sg.Column(col_description, element_justification='center', background_color="#C0C0C0"))
        columns.append(sg.Column(col_image, element_justification='center', background_color="#C0C0C0"))

    layout.append(columns)
    layout.append([sg.Button('X', key='Exit', button_color=("white", "red"), border_width=2)])

    window2 = sg.Window('Mi recomendación es:', layout, no_titlebar=True, grab_anywhere=True,
                        background_color="#C0C0C0")

    while True:
        event2, values2 = window2.read()
        if event2 == 'Exit' or event2 is None:
            break
        for i, link in enumerate(links):
            if event2 == f'website_{i}':
                webbrowser.open(link)
    window2.close()


def show_descriptions():
    """
    Ordena el diccionario 'scores' (puntajes finales) para obtener las dos escuderías con mayor puntaje,
    y muestra sus descripciones.
    """
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    best_two = sorted_scores[-2:]
    max_teams = [team for team, score in best_two if score != 0]
    images_descriptions(max_teams)


def final_results():
    """Muestra los resultados finales en una ventana con gráfico de barras y lista de porcentajes."""
    if len(options_type) == len(types):
        sorted_data = sorted(percentage.items(), key=lambda item: item[1], reverse=True)
        labels = [label for label, value in sorted_data if value != 0.0]
        values = [value for label, value in sorted_data if value != 0.0]
        colors = sns.color_palette("husl", len(labels))
        width = 0.4
        x = np.arange(len(labels))

        fig, ax1 = plt.subplots(figsize=(8, 6))
        fig.subplots_adjust(bottom=0.2)
        ax1.bar(x, values, width, color=colors, alpha=0.7, edgecolor='black', linewidth=1.2)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=30, ha='right', fontdict={'fontsize': 12})
        ax1.set_ylabel('Porcentaje (%)')
        ax1.set_title('Gráfico de Barras')

        results_window = tk.Tk()
        results_window.title("Resultados")
        results_window.iconbitmap("assets/images/f1-logo.ico")
        results_window.geometry('1200x800')
        results_window.configure(bg="#C0C0C0")

        def on_closing_results():
            if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
                results_window.destroy()
                sys.exit(0)

        results_window.protocol("WM_DELETE_WINDOW", on_closing_results)
        results_label = ttk.Label(results_window, text="RESULTADOS", font=('Segoe UI', 25),
                                  background="#C0C0C0")
        results_label.pack(pady=10)

        main_frame = tk.Frame(results_window, bg="#C0C0C0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        graph_frame = tk.Frame(main_frame, bg="#C0C0C0")
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        list_frame = tk.Frame(main_frame, bg="#C0C0C0")
        list_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        list_label = ttk.Label(list_frame, text="Porcentajes por equipo:", font=('Segoe UI', 18),
                               background="#C0C0C0")
        list_label.pack(pady=5)
        for label, value in zip(labels, values):
            item_label = ttk.Label(list_frame, text=f"{label}: {value:.2f}%", font=('Arial', 14),
                                   background="#C0C0C0")
            item_label.pack(anchor=tk.W, pady=2)

        descriptions_button = tk.Button(results_window, text="Mostrar descripciones", command=show_descriptions,
                                        font=('Segoe UI', 14), foreground="white", padx=10, pady=5, border=2,
                                        background="#DC0000")
        descriptions_button.pack(pady=5)
        descriptions_button.place(x=500, y=735)

        results_window.mainloop()
    else:
        return


# ===============================
# Inicialización y ejecución principal
# ===============================

# Inicializar Prolog y consultar el archivo f1.pl
pl = Prolog()
pl.consult("f1.pl")

# Obtener equipos y tipos (preguntas) desde Prolog
teams = item_x_prolog('teams')
# teams: ['mclaren', 'ferrari', 'redbull', 'mercedes', 'astonmartin', 'alpine', 'haas', 'rb', 'williams', 'kick']
types = list_unique_index('type')
# types: ['time', 'color', 'character', 'football', 'music', 'crash', 'number']


# Construir opciones para cada tipo
type_option = {}
for t in types:
    result_options = get_options(t)
    type_option[t] = result_options
# type_option: {'time': ['2019 o antes', 'Arranque esta temporada', 'Empece en la pandemia', 'Nunca vi Formula 1',
# 'Desde que llego Colapinto'], 'color': ['naranja', 'rojo', 'verde agua', 'verde', 'azul', 'negro', 'otro'],
# 'character': ['assets/images/characters/mcqueen.png', 'assets/images/characters/mate.png',
# 'assets/images/characters/sally.png', 'assets/images/characters/dochudson.png', 'assets/images/characters/mack.png',
# 'assets/images/characters/guido.png', 'assets/images/characters/storm.png'], 'football': ['No miro futbol', 'Boca',
# 'River', 'Independiente', 'Racing', 'Otro'], 'music': ['Electronica', 'Rock', 'Rock nacional', 'Musica clasica',
# 'Baladas', 'Cachengue'], 'crash': ['3 o mas veces', '2 veces en menos de un aÃ±o', '2 veces', '1 vez', 'Nunca'],
# 'number': ['44', '33', '16', '14', '31', '43', '77', '10', '22', '4']}


# Obtener las preguntas asociadas a cada tipo
question = questions(types)
options_type = {}   # Se almacenarán las respuestas del usuario
radio_buttons = []

# Definir los pesos para cada pregunta (ajusta según la importancia deseada)
weights = {
    'time': 2.0,
    'color': 1.0,
    'character': 1.5,
    'football': 1.0,
    'music': 0.5,
    'crash': 1.0,
    'number': 1.0
}

# Configurar la ventana principal de Tkinter para el cuestionario
main_window = tk.Tk()
main_window.title("¿Qué escudería de Formula 1 apoyar?")
answer = tk.StringVar()
main_window.iconbitmap("assets/images/f1-logo.ico")
main_window.geometry('800x450')
frame = tk.Frame(main_window, bg="#C0C0C0")
frame.pack(fill=tk.BOTH, expand=True)
main_window.protocol("WM_DELETE_WINDOW", on_closing)
styles()
show_questions(0)
main_window.mainloop()


# ===============================
# Cálculo de puntajes y porcentajes
# ===============================

# Inicializar diccionario de puntajes para cada equipo
scores = {team: 0 for team in teams}

# Para cada pregunta, obtener la respuesta del usuario y asignar el puntaje ponderado
for t in types:
    user_answer = options_type[t]
    query_results = list(pl.query(f'{t}(X, Y)'))
    # Conjunto de equipos asociados a la respuesta seleccionada (sin duplicados)
    teams_for_answer = {item['X'] for item in query_results if item['Y'] == user_answer}
    if teams_for_answer:
        weight = weights.get(t, 1.0)
        # Cada equipo recibe (peso / número de equipos asociados)
        for team in teams_for_answer:
            scores[team] += weight / len(teams_for_answer)

# Calcular el total máximo de puntos posible (suma de los pesos)
total_max_points = sum(weights[t] for t in types)

# Calcular el porcentaje final para cada equipo
percentage = {}
for team in teams:
    percentage[team_name(team)] = round((scores[team] / total_max_points) * 100, 2)

print("Scores:", scores)
print("Percentage:", percentage)

# Mostrar los resultados finales
final_results()
