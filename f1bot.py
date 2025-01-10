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


def list_unique_index(relation):
    result = list(pl.query(relation + '(X)'))
    return [item['X'] for item in result]


# Obtener los item X en una consulta --> relacion(X,Y)
# Este código realiza una consulta Prolog para la relación relacion con dos variables (X e Y)
# y luego extrae y devuelve los valores de X como una lista en Python.
def itemX_prolog(relation):
    result = list(pl.query(f'{relation}(X,Y)'))
    return [item['X'] for item in result]


# Obtener los item Y en una consulta --> relacion(X,Y)
def itemY_prolog(relation):
    result = list(pl.query(f'{relation}(X,Y)'))
    return [item['Y'] for item in result]


def teamName(team):
    result = list(pl.query(f'teams({team},Y)'))
    return [item['Y'] for item in result][0]


# Crear una instancia de Pytholog y cargar las asociaciones
pl = Prolog()
pl.consult("f1.pl")

# Obtener los roles y aspectos desde Prolog
teams = itemX_prolog('teams')
# ['mclaren', 'ferrari', 'redbull', 'mercedes', 'astonmartin', 'alpine', 'rb', 'haas', 'rb', 'williams', 'kick']
types = list_unique_index('type')
# ['time', 'color', 'character', 'football', 'music', 'crash', 'number']


def get_options(type):
    results = itemY_prolog(type)
    unique_options = []
    already_used = set() # Usamos un conjunto para la eficiencia en la comprobación de duplicados
    for result in results:
        if result not in already_used:
            unique_options.append(result)
            already_used.add(result)
    return unique_options

type_option = {}
for type in types:
    result = get_options(type)
    type_option[type] = result
# poner lo que sale del type_option

# Obtener diccionario de preguntas segun el aspecto
def questions(type):
    i = 0
    option = {}
    result = itemY_prolog('question')
    while i < len(result):
        option[type[i]] = result[i]
        i += 1
    return option


def styles():
    styles = ttk.Style()
    styles.configure("TLabel", font=('Elephant', 16),
                     foreground="black", padding=15)
    styles.configure("TRadiobutton", font=('Arial', 12),
                     foreground="black", background="#8ecae6", padding=5)
    styles.map("TRadiobutton", foreground=[
        ("active", "red"), ("!active", "black")])
    styles.configure("TButton", font=('Arial', 12),
                     foreground="black", background="black", padding=5, width=20)


question = questions(types)
type_index = 0
options_type = {}
radio_buttons = []

# Ejecucion para iniciar cuestionario
main_window = tk.Tk()
main_window.title("¿Que escuderia de formula 1 apoyar?")
option = tk.StringVar()
main_window.geometry('800x450')
frame = tk.Frame(main_window)
frame.configure(bg="#8ecae6")
frame.pack(fill=tk.BOTH, expand=True)


def on_closing():
    if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
        main_window.destroy()
        sys.exit(0)


# on_closing() se ejecuta cuando quiere cerrar
main_window.protocol("WM_DELETE_WINDOW", on_closing)


def show_questions(index):
    if (index < len(types)):
        type = types[index]
        print("aspect: ", type)
        options = type_option[type]
        q = question[type]

        # Elimina los widgets existentes
        for widget in frame.winfo_children():
            widget.destroy()
        radio_buttons.clear()  # Limpia la lista de botones de radio

        # titulo
        title = ttk.Label(frame, text=q, font=('Segoe UI', 17), background="#8ecae6")
        title.pack(pady=10)

        # Opciones de respuesta
        if type == "character":
            columns = len(options) // 2 + len(options) % 2  # Dividir en dos filas máximo
            grid_frame = tk.Frame(frame, bg="#8ecae6")  # Marco para organizar en grilla
            grid_frame.pack(pady=10)

            for i, option in enumerate(options):
                row = i // columns  # Calcular fila (dos filas máximo)
                col = i % columns  # Columna dentro de la fila
                image = load_image(option)
                radio_button = ttk.Radiobutton(
                    grid_frame, image=image, variable=option, value=option
                )
                radio_button.image = image
                radio_button.grid(row=row, column=col, padx=20, pady=10)
                radio_buttons.append(radio_button)
        else:
            for option in options:
                radio_button = ttk.Radiobutton(frame, text=option, variable=option, value=option)
                radio_button.pack(anchor=tk.W, padx=70)
                radio_buttons.append(radio_button)

        # enviar respuesta
        def send():
            if option.get() == "":
                messagebox.showerror("Error", "Debes seleccionar una opción.")
            else:
                # {'debilidad': 'Antisocial', 'futbol': 'Juego de defensor','pelea': 'Me meto a pelear','protagonismo':'No quiero ser protagonista','ayudar': 'Nunca me piden ayuda','insultos': 'Nunca me insultan'}
                options_type[type] = option.get()
                # Reiniciar la variable respuesta para la siguiente pregunta
                option.set("")
                title.pack_forget()
                for radio_button in radio_buttons:
                    radio_button.pack_forget()
                send_button.forget()
                show_questions(index + 1)

        send_button = tk.Button(main_window, text="Enviar respuesta", command=send, font=('Segoe UI', 14),
                                 foreground="white", padx=10, pady=5, border=2, background="#023047")
        send_button.pack(pady=5)
        send_button.place(x=300, y=400)

    else:
        main_window.destroy()

def load_image(route):
    img = Image.open(route)
    img = img.resize((100, 100))
    return ImageTk.PhotoImage(img)

styles()
show_questions(0)
main_window.mainloop()

counter = []
for type in types:
    # ['debilidad', 'futbol', 'pelea', 'protagonismo', 'ayudar', 'insultos']
    # {'debilidad': 'Antisocial', 'futbol': 'Juego de defensor','pelea': 'Me meto a pelear','protagonismo':'No quiero ser protagonista','ayudar': 'Nunca me piden ayuda','insultos': 'Nunca me insultan'}
    # respuesta = 'Antisocial'
    option = options_type[type]
    consulta = list(pl.query(type + '(X,Y)'))
    # [{'X': 'top', 'Y': 'Antisocial'}, {'X': 'jgl', 'Y': 'Hiperactivo'}, {'X': 'mid', 'Y': 'Avaricia'}, {'X': 'adc', 'Y': 'Egocentrico'}, {'X': 'sup', 'Y': 'Sensible'}]
    for item in consulta:
        if item['Y'] == option:
            counter.append(item['X'])


# Mostrar las descripciones y las imagenes de los roles
def images_descriptions(teams):
    descriptions = []
    images = []
    for team in teams:
        result = list(pl.query(f"description({team}, Y)"))
        image = list(pl.query(f"image({team}, Y)"))
        images.append([item['Y'] for item in image])
        descriptions.append([item['Y'] for item in result])
    print("imagenes: ", images)
    columns = []
    columns_2 = []
    layout = []
    i = len(descriptions) - 1
    while i >= 0:
        description = ""
        for desc in descriptions[i]:
            description += '-' + desc + "\n"

        col = [[sg.Text(teams[i].upper(), font=('Segoe UI', 35), background_color="#8ecae6", text_color="black")],
               [sg.Text(description, auto_size_text=True, size=(35, 15), font=('Arial', 14), background_color="#8ecae6",
                        text_color="black")], ]
        col1 = [
            [sg.Image(data=get_img_data(images[i][0], maxsize=(220, 400), first=True), background_color="#8ecae6", pad=(0,0))]]

        if (len(descriptions) == 4 and i == 0):
            columns_2.append(sg.Column(col, element_justification='center', background_color="#8ecae6"))
            columns_2.append(sg.Column(col1, element_justification='center', background_color="black"))
        elif (len(descriptions) == 5 and i <= 1):
            columns_2.append(sg.Column(col, element_justification='center', background_color="#8ecae6"))
            columns_2.append(sg.Column(col1, element_justification='center', background_color="black"))
        else:
            columns.append(sg.Column(col, element_justification='center', background_color="#8ecae6"))
            columns.append(sg.Column(col1, element_justification='center', background_color="black"))
        i -= 1

    layout.append(columns)
    if columns_2 != []:
        layout.append(columns_2)
    layout.append(
        [sg.Button('X', key='Exit',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   pad=(0, 0))])
    window2 = sg.Window('Mi recomendación es:', layout, no_titlebar=True, grab_anywhere=True,
                        background_color="#8ecae6")
    while True:
        event2, values2 = window2.read()
        print(event2, values2)

        if event2 in (None, 'Exit'):
            break
        event2, values2 = None, None

    window2.close()
    return


def show_descriptions():
    sorted_value = sorted(result.items(), key=operator.itemgetter(1))
    first_two_teams = sorted_value[-2:]
    max = []
    for team in first_two_teams:
        if team[1] != 0:
            max.append(team[0])
    print("maximos: ", max)
    images_descriptions(max)


result = {}
for team in teams:
    result[team] = counter.count(team)
# {'top': 3, 'jgl': 1, 'mid':1, 'adc':1, 'supp':0}

total = len(counter)
percentage = {}
for key, value in result.items():
    percentage[teamName(key)] = round((value / total) * 100, 2)


# Mostrar resultados en una ventana
def final_results():
    if (len(options_type) == len(types)):

        labels = []
        values = []

        # Filtrar los valores iguales a 0.0
        for label, valor in percentage.items():
            if valor != 0.0:
                labels.append(label)
                values.append(valor)

        # Utilizar una paleta de colores para asignar un color a cada barra
        colors = sns.color_palette("husl", len(labels))

        # Ajustes para evitar la superposición de barras
        width = 0.4  # Ancho de las barras
        x = np.arange(len(labels))  # Posiciones en el eje x

        # Crear la figura y los subgráficos
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7.5))

        # Gráfico de barras
        ax1.bar(x, values, width, color=colors, alpha=0.7, edgecolor='black', linewidth=1.2)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=45, ha='right', fontdict={'fontsize': 12})
        ax1.set_ylabel('Porcentaje (%)')
        ax1.set_title('Gráfico de Barras')

        # Gráfico de pastel
        ax2.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Gráfico de Pastel')

        # Mostrar el gráfico de torespuesta en una nueva ventana
        results_window = tk.Tk()
        results_window.title("Resultados")
        results_window.geometry('1200x900')
        results_window.configure(bg="#8ecae6")

        def on_closing():
            if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir?"):
                results_window.destroy()
                sys.exit(0)
            return

        results_window.protocol("WM_DELETE_WINDOW", on_closing)

        results_label = ttk.Label(results_window, text="RESULTADOS", font=('Segoe UI', 25),
                                        background="#8ecae6")
        results_label.pack(pady=10)

        # Agregar el gráfico a la ventana de resultados
        canvas = FigureCanvasTkAgg(fig, master=results_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        descriptions_button = tk.Button(results_window, text="Mostrar descripciones", command=show_descriptions,
                                     font=('Segoe UI', 14), foreground="white", padx=10, pady=5, border=2,
                                     background="#023047")
        descriptions_button.pack(pady=5)

        descriptions_button.place(x=500, y=835)

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

final_results()