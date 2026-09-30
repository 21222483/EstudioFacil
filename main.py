from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
import json
from pathlib import Path

DATA = Path("tareas.json")

def load_tasks():
    if DATA.exists():
        try:
            return json.loads(DATA.read_text(encoding="utf-8"))
        except:
            return []
    return []

def save_tasks(tasks):
    DATA.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(15))
        box.add_widget(Label(text="[b]📚 ESTUDIO FÁCIL[/b]", markup=True, font_size=30))
        box.add_widget(Label(text="Organiza tus tareas y mejora tus notas", font_size=16))
        self.user = TextInput(hint_text="Usuario", multiline=False, size_hint_y=None, height=dp(50))
        self.password = TextInput(hint_text="Contraseña", password=True, multiline=False, size_hint_y=None, height=dp(50))
        box.add_widget(self.user)
        box.add_widget(self.password)
        btn = Button(text="🚀 Iniciar sesión", size_hint_y=None, height=dp(55))
        btn.bind(on_press=self.login)
        box.add_widget(btn)
        box.add_widget(Label(text="Proyecto académico hecho con Python + Kivy"))
        self.add_widget(box)

    def login(self, *_):
        if self.user.text.strip() and self.password.text.strip():
            self.manager.current = "home"
        else:
            Popup(title="Faltan datos", content=Label(text="Escribe usuario y contraseña."), size_hint=(.8,.3)).open()

class HomeScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        box.add_widget(Label(text="[b]🏠 ESTUDIO FÁCIL[/b]", markup=True, font_size=28))
        box.add_widget(Label(text="Tu espacio para organizar el estudio.", font_size=16))

        for text, target in [
            ("📝 Mis tareas", "tasks"),
            ("📊 Mis notas", "grades"),
            ("💡 Consejos", "tips"),
            ("ℹ️ Sobre el proyecto", "about"),
        ]:
            b = Button(text=text, size_hint_y=None, height=dp(58))
            b.bind(on_press=lambda _, s=target: setattr(self.manager, "current", s))
            box.add_widget(b)

        self.add_widget(box)

class TasksScreen(Screen):
    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        box.add_widget(Label(text="[b]📝 MIS TAREAS[/b]", markup=True, font_size=25, size_hint_y=None, height=dp(45)))

        add = Button(text="➕ Agregar tarea", size_hint_y=None, height=dp(50))
        add.bind(on_press=self.add_task)
        box.add_widget(add)

        scroll = ScrollView()
        listbox = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        listbox.bind(minimum_height=listbox.setter("height"))

        tasks = load_tasks()
        if not tasks:
            listbox.add_widget(Label(text="No tienes tareas todavía.", size_hint_y=None, height=dp(50)))
        else:
            for i, t in enumerate(tasks):
                state = "✅" if t["done"] else "⏳"
                b = Button(
                    text=f"{state} {t['name']} — {t['subject']} — {t['priority']}",
                    size_hint_y=None, height=dp(55)
                )
                b.bind(on_press=lambda _, idx=i: self.toggle(idx))
                listbox.add_widget(b)

        scroll.add_widget(listbox)
        box.add_widget(scroll)

        back = Button(text="⬅️ Volver", size_hint_y=None, height=dp(50))
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        box.add_widget(back)
        self.add_widget(box)

    def add_task(self, *_):
        layout = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        name = TextInput(hint_text="Nombre de la tarea", multiline=False)
        subject = TextInput(hint_text="Materia", multiline=False)
        priority = TextInput(hint_text="Prioridad: Alta, Media o Baja", multiline=False)
        layout.add_widget(name); layout.add_widget(subject); layout.add_widget(priority)
        btn = Button(text="Guardar", size_hint_y=None, height=dp(50))
        layout.add_widget(btn)
        popup = Popup(title="Nueva tarea", content=layout, size_hint=(.9,.65))
        def save(*_):
            if not name.text.strip():
                return
            tasks = load_tasks()
            tasks.append({
                "name": name.text.strip(),
                "subject": subject.text.strip() or "General",
                "priority": priority.text.strip() or "Media",
                "done": False
            })
            save_tasks(tasks)
            popup.dismiss()
            self.refresh()
        btn.bind(on_press=save)
        popup.open()

    def toggle(self, idx):
        tasks = load_tasks()
        tasks[idx]["done"] = not tasks[idx]["done"]
        save_tasks(tasks)
        self.refresh()

class GradesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        box.add_widget(Label(text="[b]📊 CALCULADORA DE NOTAS[/b]", markup=True, font_size=25))
        self.inputs = []
        for i in range(3):
            row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
            grade = TextInput(hint_text=f"Nota {i+1} (0-5)", input_filter="float")
            weight = TextInput(hint_text=f"Peso {i+1} (%)", input_filter="float")
            row.add_widget(grade); row.add_widget(weight)
            self.inputs.append((grade, weight))
            box.add_widget(row)

        calc = Button(text="🧮 Calcular promedio", size_hint_y=None, height=dp(55))
        calc.bind(on_press=self.calculate)
        box.add_widget(calc)
        self.result = Label(text="Ingresa 3 notas cuyos porcentajes sumen 100%.", font_size=17)
        box.add_widget(self.result)

        back = Button(text="⬅️ Volver", size_hint_y=None, height=dp(50))
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        box.add_widget(back)
        self.add_widget(box)

    def calculate(self, *_):
        try:
            grades = [float(x[0].text) for x in self.inputs]
            weights = [float(x[1].text) for x in self.inputs]
            if any(g < 0 or g > 5 for g in grades):
                raise ValueError
            if sum(weights) != 100:
                self.result.text = "❌ Los porcentajes deben sumar 100%."
                return
            avg = sum(g*w/100 for g,w in zip(grades, weights))
            self.result.text = f"Promedio: {avg:.2f} / 5.00\n" + ("✅ Aprobado" if avg >= 3 else "📚 Necesitas mejorar")
        except:
            self.result.text = "❌ Revisa los datos ingresados."

class TipsScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        box.add_widget(Label(text="[b]💡 CONSEJOS[/b]", markup=True, font_size=25))
        for t in [
            "⏱️ Estudia en bloques y haz pausas.",
            "📱 Evita distracciones mientras estudias.",
            "📝 Prioriza las tareas más importantes.",
            "😴 Descansa y duerme bien.",
        ]:
            box.add_widget(Label(text=t, font_size=17))
        back = Button(text="⬅️ Volver", size_hint_y=None, height=dp(50))
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        box.add_widget(back)
        self.add_widget(box)

class AboutScreen(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        box.add_widget(Label(text="[b]ℹ️ SOBRE EL PROYECTO[/b]", markup=True, font_size=25))
        box.add_widget(Label(
            text="Estudio Fácil es una aplicación educativa.\n\n"
                 "Lenguaje: Python\n"
                 "Interfaz Android: Kivy\n\n"
                 "Permite iniciar sesión, administrar tareas,\n"
                 "calcular notas y consultar consejos de estudio.",
            font_size=17
        ))
        back = Button(text="⬅️ Volver", size_hint_y=None, height=dp(50))
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        box.add_widget(back)
        self.add_widget(box)

class EstudioFacilApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TasksScreen(name="tasks"))
        sm.add_widget(GradesScreen(name="grades"))
        sm.add_widget(TipsScreen(name="tips"))
        sm.add_widget(AboutScreen(name="about"))
        return sm

EstudioFacilApp().run()
