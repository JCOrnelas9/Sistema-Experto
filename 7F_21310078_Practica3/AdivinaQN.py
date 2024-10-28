import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Archivo JSON donde se guardan las verduras
JSON_FILE = 'verduras.json'

def load_vegetables():
    """Carga las verduras desde el archivo JSON, o retorna una lista vacía si no existe."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    else:
        return []  # Retorna una lista vacía si el archivo no existe

def save_vegetables(vegetables):
    """Guarda las verduras en el archivo JSON."""
    with open(JSON_FILE, 'w') as file:
        json.dump(vegetables, file, indent=4)

class GuessVegetableApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Adivina la Verdura")
        self.vegetables = load_vegetables()  # Cargar verduras del archivo JSON
        self.remaining_vegetables = self.vegetables[:]
        self.already_asked = set()
        self.questions = []
        self.current_question = None

        # Elementos de la interfaz
        self.question_label = tk.Label(master, text="¿Es una verdura?")
        self.question_label.pack()

        self.yes_button = tk.Button(master, text="Sí", command=lambda: self.answer_question("sí"))
        self.yes_button.pack()

        self.no_button = tk.Button(master, text="No", command=lambda: self.answer_question("no"))
        self.no_button.pack()

        self.reset_button = tk.Button(master, text="Reiniciar Juego", command=self.reset_game)
        self.reset_button.pack()

        self.start_game()

    def start_game(self):
        """Inicia el juego mostrando la primera pregunta."""
        if not self.vegetables:
            messagebox.showinfo("Sin verduras", "No hay verduras en la base de datos. Por favor, agrega nuevas verduras.")
            self.add_vegetable()  # Invitar a agregar verduras si no hay
            return

        self.remaining_vegetables = self.vegetables[:]
        self.already_asked.clear()
        self.questions = self.generate_questions()
        self.next_question()

    def generate_questions(self):
        """Genera preguntas basadas en las características de las verduras restantes."""
        questions = []
        colors = set(v["color"].lower() for v in self.remaining_vegetables)
        types = set(v["type"].lower() for v in self.remaining_vegetables)
        flavors = set(v["flavor"].lower() for v in self.remaining_vegetables)

        # Generar preguntas basadas en colores
        for color in colors:
            if f"¿Es {color}?" not in self.already_asked:
                questions.append({"question": f"¿Es {color}?", "attribute": "color", "value": color})

        # Generar preguntas basadas en tipos
        for veg_type in types:
            if f"¿Es un tipo {veg_type}?" not in self.already_asked:
                questions.append({"question": f"¿Es un tipo {veg_type}?", "attribute": "type", "value": veg_type})

        # Generar preguntas basadas en sabores
        for flavor in flavors:
            if f"¿Es {flavor}?" not in self.already_asked:
                questions.append({"question": f"¿Es {flavor}?", "attribute": "flavor", "value": flavor})

        return questions

    def next_question(self):
        """Realiza la siguiente pregunta al jugador."""
        if self.remaining_vegetables and self.questions:
            question_data = self.questions.pop(0)
            self.question_label.config(text=question_data["question"])
            self.current_question = question_data
            self.already_asked.add(question_data["question"])  # Marcar pregunta como hecha
        elif len(self.remaining_vegetables) == 1:
            # Si solo queda una verdura, preguntar al usuario si es la correcta
            self.confirm_guess()  # Confirma si la adivinanza es correcta
        else:
            # Si no hay preguntas disponibles y no se ha adivinado una verdura
            messagebox.showinfo("Fin del juego", "¡El juego ha terminado!")
            self.reset_game()  # Reinicia el juego si no hay preguntas

    def confirm_guess(self):
        """Confirma la adivinanza del programa con el usuario."""
        guessed_vegetable = self.remaining_vegetables[0]['name']
        if messagebox.askyesno("Confirmación", f"¿Es {guessed_vegetable} la verdura que estás pensando?"):
            messagebox.showinfo("¡Correcto!", f"¡Era {guessed_vegetable}!")
        else:
            messagebox.showinfo("¡Incorrecto!", "Parece que he fallado. ¿Quieres agregar una nueva verdura?")
            self.add_vegetable()  # Opción para agregar una nueva verdura
        self.reset_game()  # Reinicia el juego después de adivinar correctamente

    def answer_question(self, answer):
        """Procesa la respuesta de la pregunta actual."""
        if answer == "sí":
            # Filtrar las verduras que cumplen con la respuesta afirmativa
            self.remaining_vegetables = [v for v in self.remaining_vegetables if v[self.current_question["attribute"]].lower() == self.current_question["value"]]
        else:
            # Filtrar las verduras que no cumplen con la respuesta negativa
            self.remaining_vegetables = [v for v in self.remaining_vegetables if v[self.current_question["attribute"]].lower() != self.current_question["value"]]

        # Verificar cuántas verduras quedan después de la respuesta
        if len(self.remaining_vegetables) == 0:
            # Si no quedan verduras, ofrecer la opción de agregar una nueva
            messagebox.showinfo("¡Sin opciones!", "No quedan más verduras que coincidan. Puedes agregar una nueva.")
            self.add_vegetable()
            self.reset_game()  # Reinicia el juego después de agregar
        else:
            # Generar preguntas actualizadas después de cada respuesta
            self.questions = self.generate_questions()
            self.next_question()  # Haz la siguiente pregunta
    def add_vegetable(self):
        name = simpledialog.askstring("Nombre de la verdura", "Ingrese el nombre de la verdura:").strip()
        color = simpledialog.askstring("Color de la verdura", "Ingrese el color de la verdura:").strip()
        veg_type = simpledialog.askstring("Tipo de la verdura", "Ingrese el tipo de la verdura:").strip()
        flavor = simpledialog.askstring("Sabor de la verdura", "Ingrese el sabor de la verdura:").strip()

        new_vegetable = {
            "name": name,
            "color": color,
            "type": veg_type,
            "flavor": flavor
        }

        # Verificar si la verdura ya existe para evitar duplicados
        if any(v["name"].lower() == new_vegetable["name"].lower() for v in self.vegetables):
            messagebox.showwarning("Verdura duplicada", f"La verdura '{name}' ya existe en la base de datos.")
            return

        # Agregar la nueva verdura y guardar en el archivo
        self.vegetables.append(new_vegetable)
        save_vegetables(self.vegetables)

        messagebox.showinfo("Verdura agregada", f"Se ha agregado {name} a la base de datos.")

    def reset_game(self):
        """Reinicia el juego."""    
        self.question_label.config(text="¿Es una verdura?")
        self.yes_button.config(command=lambda: self.answer_question("sí"))
        self.no_button.config(command=lambda: self.answer_question("no"))
        self.start_game()

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessVegetableApp(root)
    root.mainloop()
