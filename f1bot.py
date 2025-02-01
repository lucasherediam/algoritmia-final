import sys

import PySimpleGUI as sg
import io
import tkinter as tk
from tkinter import messagebox
from pyswip import Prolog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import operator
import numpy as np
import seaborn as sns
import webbrowser


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
    result = list(pl.query(f'teams({team},Y)'))
    return [item['Y'] for item in result][0]


def get_options(type):
    """Obtiene las opciones únicas para un tipo dado desde Prolog."""
    results = item_y_prolog(type)
    unique_options = []
    already_used = set()
    for result in results:
        if result not in already_used:
            unique_options.append(result)
            already_used.add(result)
    return unique_options


# Obtener diccionario de preguntas segun el aspecto
def questions(type):
    """Crea un diccionario de preguntas para cada tipo desde Prolog."""
    i = 0
    option = {}
    result = item_y_prolog('question')
    while i < len(result):
        option[type[i]] = result[i]
        i += 1
    return option


def styles():
    styles = ttk.Style()
    styles.configure("TLabel", font=('Elephant', 16),
                     foreground="black", padding=15)
    styles.configure("TRadiobutton", font=('Arial', 12),
                     foreground="black", background="#C0C0C0", padding=5)
    styles.map("TRadiobutton", foreground=[
        ("active", "red"), ("!active", "black")])
    styles.configure("TButton", font=('Arial', 12),
                     foreground="black", background="black", padding=5, width=20)


def on_closing():
    if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
        main_window.destroy()
        sys.destroy()


def show_questions(index):
    """Muestra las preguntas y opciones correspondientes en la interfaz según el índice actual."""
    if index < len(types):
        type = types[index]
        print("aspect: ", type)
        options = type_option[type]
        q = question[type]

        # Limpia lo que puede haber quedado de la pregunta anterior
        for widget in frame.winfo_children():
            widget.destroy()
        radio_buttons.clear()

        # Titulo
        title = ttk.Label(frame, text=q, font=('Segoe UI', 17), background="#DC0000")
        title.pack(pady=10)

        # Opciones de respuesta
        if type == "character":
            columns = len(options) // 2 + len(options) % 2  # Dividir en dos filas máximo
            grid_frame = tk.Frame(frame, bg="#C0C0C0")  # Marco para organizar en grilla
            grid_frame.pack(pady=10)

            for i, option in enumerate(options):
                row = i // columns  # Calcular fila
                col = i % columns  # Columna dentro de la fila
                image = load_image(option)
                radio_button = ttk.Radiobutton(
                    grid_frame, image=image, variable=answer, value=option
                )
                radio_button.image = image
                radio_button.grid(row=row, column=col, padx=20, pady=10)
                radio_buttons.append(radio_button)
        else:
            for option in options:
                radio_button = ttk.Radiobutton(frame, text=option, variable=answer, value=option)
                radio_button.pack(anchor=tk.W, padx=70)
                radio_buttons.append(radio_button)

        # Enviar la respuesta elegida
        def send():
            if answer.get() == "":
                messagebox.showerror("Error", "Debes seleccionar una opción.")
            else:
                options_type[type] = answer.get()
                # Reiniciar la variable respuesta para la siguiente pregunta
                answer.set("")
                title.pack_forget()
                for radio_button in radio_buttons:
                    radio_button.pack_forget()
                send_button.forget()
                show_questions(index + 1)

        send_button = tk.Button(main_window, text="Enviar respuesta", command=send, font=('Segoe UI', 14),
                                foreground="white", padx=10, pady=5, border=2, background="#DC0000")
        send_button.pack(pady=5)
        send_button.place(x=300, y=375)

    else:
        main_window.destroy()


def load_image(route):
    img = Image.open(route)
    img = img.resize((100, 100))
    return ImageTk.PhotoImage(img)


# Mostrar las descripciones y las imagenes de los roles
def images_descriptions(teams):
    """Muestra descripciones, imágenes y enlaces para los equipos recomendados."""
    descriptions = []
    images = []
    links = []  # Lista para almacenar los enlaces de cada equipo

    for team in teams:
        result = list(pl.query(f"description({team}, Y)"))
        image = list(pl.query(f"image({team}, Y)"))
        link = list(pl.query(f"link({team}, Y)"))

        images.append([item['Y'] for item in image])
        descriptions.append([item['Y'] for item in result])
        links.append([item['Y'] for item in link][0])  # Guardar el primer enlace

    columns = []
    layout = []

    for i, team in enumerate(teams):
        description = "\n".join([f"- {desc}" for desc in descriptions[i]])

        # Crear columnas para descripción e imagen
        col_description = [
            [sg.Text(team.upper(), font=('Segoe UI', 25), background_color="#C0C0C0", text_color="black")],
            [sg.Text(description, auto_size_text=True, font=('Arial', 14), background_color="#C0C0C0",
                     text_color="black")],
            [sg.Button('Go to website', key=f'website_{i}', button_color=("white", "#DC0000"), border_width=2)]
        ]
        col_image = [
            [sg.Image(data=get_img_data(images[i][0], maxsize=(220, 400), first=True), background_color="#C0C0C0")]
        ]

        # Agregar a las columnas
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

        # Abrir el enlace correspondiente al botón presionado
        for i, link in enumerate(links):
            if event2 == f'website_{i}':  # Botón específico para cada equipo
                webbrowser.open(link)  # Abre el enlace en el navegador

    window2.close()


def show_descriptions():
    """Determina los equipos recomendados y muestra sus descripciones y enlaces."""
    sorted_value = sorted(result.items(), key=operator.itemgetter(1))
    first_two_teams = sorted_value[-2:]
    max = []
    for team in first_two_teams:
        if team[1] != 0:
            max.append(team[0])
    images_descriptions(max)


def final_results():
    """Genera y muestra los resultados finales en una ventana, con gráficos y porcentajes."""
    if len(options_type) == len(types):

        # Filtrar y ordenar los valores iguales a 0.0
        sorted_data = sorted(percentage.items(), key=lambda item: item[1], reverse=True)
        labels = [label for label, value in sorted_data if value != 0.0]
        values = [value for label, value in sorted_data if value != 0.0]

        # Utilizar una paleta de colores para asignar un color a cada barra
        colors = sns.color_palette("husl", len(labels))

        # Ajustes para evitar la superposición de barras
        width = 0.4  # Ancho de las barras
        x = np.arange(len(labels))  # Posiciones en el eje x

        # Crear la figura y los subgráficos
        fig, ax1 = plt.subplots(figsize=(8, 6))
        fig.subplots_adjust(bottom=0.2)

        # Gráfico de barras
        ax1.bar(x, values, width, color=colors, alpha=0.7, edgecolor='black', linewidth=1.2)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=30, ha='right', fontdict={'fontsize': 12})
        ax1.set_ylabel('Porcentaje (%)')
        ax1.set_title('Gráfico de Barras')

        # Mostrar el gráfico y la lista en una nueva ventana
        results_window = tk.Tk()
        results_window.title("Resultados")
        results_window.geometry('1200x800')
        results_window.configure(bg="#C0C0C0")

        def on_closing():
            if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
                results_window.destroy()
                sys.exit(0)
            return

        results_window.protocol("WM_DELETE_WINDOW", on_closing)

        results_label = ttk.Label(results_window, text="RESULTADOS", font=('Segoe UI', 25),
                                  background="#C0C0C0")
        results_label.pack(pady=10)

        # Crear un frame para dividir en dos columnas
        main_frame = tk.Frame(results_window, bg="#C0C0C0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Frame para el gráfico
        graph_frame = tk.Frame(main_frame, bg="#C0C0C0")
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Frame para la lista
        list_frame = tk.Frame(main_frame, bg="#C0C0C0")
        list_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        list_label = ttk.Label(list_frame, text="Porcentajes por equipo:", font=('Segoe UI', 18),
                               background="#C0C0C0")
        list_label.pack(pady=5)

        for label, value in zip(labels, values):
            item_label = ttk.Label(list_frame, text=f"{label}: {value:.2f}%", font=('Arial', 14), background="#C0C0C0")
            item_label.pack(anchor=tk.W, pady=2)

        descriptions_button = tk.Button(results_window, text="Mostrar descripciones", command=show_descriptions,
                                        font=('Segoe UI', 14), foreground="white", padx=10, pady=5, border=2,
                                        background="#DC0000")
        descriptions_button.pack(pady=5)

        descriptions_button.place(x=500, y=735)

        results_window.mainloop()
    else:
        return


def get_img_data(f, maxsize=(1200, 850), first=False):
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


# final_results()


# Crear una instancia de Pytholog y cargar las asociaciones
pl = Prolog()
pl.consult("f1.pl")

# Obtener los roles y aspectos desde Prolog
teams = item_x_prolog('teams')
# teams: ['mclaren', 'ferrari', 'redbull', 'mercedes', 'astonmartin', 'alpine', 'haas', 'rb', 'williams', 'kick']
types = list_unique_index('type')
# types: ['time', 'color', 'character', 'football', 'music', 'crash', 'number']

type_option = {}
for type in types:
    result = get_options(type)
    type_option[type] = result
# type_option: {'time': ['2019 o antes', 'Arranque esta temporada', 'Empece en la pandemia', 'Nunca vi Formula 1',
# 'Desde que llego Colapinto'], 'color': ['naranja', 'rojo', 'verde agua', 'verde', 'azul', 'negro', 'otro'],
# 'character': ['assets/images/characters/mcqueen.png', 'assets/images/characters/mate.png',
# 'assets/images/characters/sally.png', 'assets/images/characters/dochudson.png', 'assets/images/characters/mack.png',
# 'assets/images/characters/guido.png', 'assets/images/characters/storm.png'], 'football': ['No miro futbol', 'Boca',
# 'River', 'Independiente', 'Racing', 'Otro'], 'music': ['Electronica', 'Rock', 'Rock nacional', 'Musica clasica',
# 'Baladas', 'Cachengue'], 'crash': ['3 o mas veces', '2 veces en menos de un aÃ±o', '2 veces', '1 vez', 'Nunca'],
# 'number': ['44', '33', '16', '14', '31', '43', '77', '10', '22', '4']}

question = questions(types)
type_index = 0
options_type = {}
radio_buttons = []

# Ejecucion para iniciar cuestionario
main_window = tk.Tk()
main_window.title("¿Que escuderia de formula 1 apoyar?")
answer = tk.StringVar()
main_window.iconbitmap("assets/images/f1-logo.ico")
main_window.geometry('800x450')
frame = tk.Frame(main_window)
frame.configure(bg="#C0C0C0")
frame.pack(fill=tk.BOTH, expand=True)

# on_closing() se ejecuta cuando quiere cerrar
main_window.protocol("WM_DELETE_WINDOW", on_closing)

styles()
show_questions(0)
main_window.mainloop()

counter = []
for type in types:
    answer = options_type[type]
    consulta = list(pl.query(type + '(X,Y)'))
    for item in consulta:
        if item['Y'] == answer:
            counter.append(item['X'])

result = {}
for team in teams:
    result[team] = counter.count(team)

total = len(counter)
percentage = {}
for key, value in result.items():
    percentage[team_name(key)] = round((value / total) * 100, 2)

final_results()