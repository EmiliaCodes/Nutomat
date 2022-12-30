from tkinter.filedialog import askdirectory
import customtkinter
import engine
import os
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


def switch_mode_appearance():
    if App.is_on:
        customtkinter.set_appearance_mode("Light")
        App.is_on = False
    else:
        customtkinter.set_appearance_mode("Dark")
        App.is_on = True


class App(customtkinter.CTk):
    WIDTH = 700
    HEIGHT = 500
    is_on = True

    my_engine = engine.Engine()

    def __init__(self):
        super().__init__()

        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title("Nutomat")
        self.iconbitmap("note.ico")

        # Create the frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)

        self.frame_top = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frame_top.grid(row=0, column=0, columnspan=2, sticky="nswe", padx=20, pady=(20, 0))

        self.frame_left = customtkinter.CTkFrame(master=self, width=100, corner_radius=10)
        self.frame_left.grid(row=1, column=0, sticky="nswe", padx=(20, 10), pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=1, column=1, sticky="nswe", padx=(10, 20), pady=20)

        # # Frame top
        self.frame_top.grid_rowconfigure(0, weight=0)  # empty row with minsize as spacing
        self.frame_top.grid_rowconfigure(1, weight=1, minsize=10)  # button row
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_top,
                                                   text="NUTOMAT\nW celu wygenerowania nowego dyktanda "
                                                        "wybierz ścieżkę zapisu oraz ustaw parametry - tonację, "
                                                        "długość w taktach oraz tempo przy zapisanym pliku dźwiękowym. "
                                                        "Zaznacz czy chcesz wygenerować dodatkowy plik PDF, "
                                                        "który wypełnisz przy rozwiązywaniu dyktanda.",
                                                   corner_radius=6,
                                                   fg_color=("white", "gray38"),
                                                   height=100,
                                                   wraplength=750)
        self.label_info_1.grid(column=0, row=0, sticky="nswe", padx=10, pady=10)

        self.button_generate = customtkinter.CTkButton(master=self.frame_top, text="GENERUJ",
                                                       command=self.generate, height=40, width=400,
                                                       fg_color="#11B384",
                                                       hover_color="#92374d",
                                                       text_font=("TkDefaultFont", 10, 'bold')
                                                       )
        self.button_generate.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Frame left
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_columnconfigure(0, weight=1, minsize=200)
        self.frame_left.grid_columnconfigure(1, weight=2)

        self.label_time_sig = customtkinter.CTkLabel(master=self.frame_left, text="Metrum", width=100, anchor="w")
        self.label_time_sig.grid(row=1, column=0, pady=10, padx=(0, 0))

        self.option_time_sig = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                           values=["3/4", "4/4"])
        self.option_time_sig.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        self.label_key_signature = customtkinter.CTkLabel(master=self.frame_left, text="Tonacja dyktanda", width=100,
                                                          anchor="w")
        self.label_key_signature.grid(row=2, column=0, pady=10, padx=(0, 0))

        self.option_key_signature = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                values=["C-dur", "F-dur", "G-dur", "B-dur", "D-dur"])
        self.option_key_signature.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        self.label_number_of_bars = customtkinter.CTkLabel(master=self.frame_left,
                                                           width=100,
                                                           anchor="w",
                                                           text="Ilość taktów")
        self.label_number_of_bars.grid(row=3, column=0, pady=10, padx=(0, 0))

        self.option_number_of_bars = customtkinter.CTkOptionMenu(master=self.frame_left, values=["4", "8", "12", "16"])
        self.option_number_of_bars.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        self.label_tempo = customtkinter.CTkLabel(master=self.frame_left, text="Tempo dyktanda", width=100, anchor="w")
        self.label_tempo.grid(row=4, column=0, pady=10, padx=(0, 0))

        self.option_tempo = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["szybkie", "umiarkowane", "wolne"])
        self.option_tempo.grid(row=4, column=1, pady=10, padx=20, sticky="w")

        self.switch_appearance_mode = customtkinter.CTkSwitch(master=self.frame_left,
                                                              text="Tryb ciemny",
                                                              command=switch_mode_appearance)
        self.switch_appearance_mode.grid(row=6, column=0, columnspan=2, pady=10, padx=20, sticky="w")

        # Right column
        self.frame_right.grid_rowconfigure(0, minsize=10)  # empty - spacing
        self.frame_right.grid_rowconfigure(4, weight=10, minsize=5)  # empty - spacing
        self.frame_right.grid_columnconfigure(0, minsize=10)
        self.frame_right.grid_columnconfigure(1, weight=1)

        self.switch_if_midi = customtkinter.CTkSwitch(master=self.frame_right, text="Zapis midi")
        self.switch_if_midi.grid(row=1, column=1, pady=10, padx=20, sticky='w')

        self.switch_if_blank_staff = customtkinter.CTkSwitch(master=self.frame_right, text="Zapis pustych pięciolinii",
                                                             command=self.empty_staff_action)
        self.switch_if_blank_staff.grid(row=2, column=1, pady=10, padx=20, sticky='w')

        self.switch_hints = customtkinter.CTkSwitch(master=self.frame_right, text="Zapis podpowiedzi")
        self.switch_hints.grid(row=3, column=1, pady=10, padx=20, sticky='w')

        self.button_save_in = customtkinter.CTkButton(master=self.frame_right,
                                                      text="Zapisz w",
                                                      command=self.select_file)
        self.button_save_in.grid(row=5, column=1, padx=20, pady=(0, 10))

        self.label_path = customtkinter.CTkLabel(master=self.frame_right, text="", width=100, anchor="w",
                                                 wraplength=300)
        self.label_path.grid(row=6, column=1, pady=(0, 10), padx=(0, 0))

        # Start
        self.switch_appearance_mode.select()
        self.option_number_of_bars.set("4")
        self.switch_if_midi.select()  # turn on as default
        self.switch_if_blank_staff.select()  # turn on as default

    def select_file(self):
        path = askdirectory()
        self.label_path.configure(text=path)

    def empty_staff_action(self):
        if self.switch_if_blank_staff.get() == 0:
            self.switch_hints.configure(state="disabled")
        else:
            self.switch_hints.configure(state="normal")

    def generate(self):
        my_path = self.label_path.text
        number_of_bars = float(self.option_number_of_bars.current_value)
        key_signature = str(self.option_key_signature.current_value)
        tempo = str(self.option_tempo.current_value)
        write_midi = self.switch_if_midi.get()
        write_empty = self.switch_if_blank_staff.get()
        hints = engine.hints_count(self.switch_hints.get(), number_of_bars)
        time_signature = str(self.option_time_sig.current_value)

        temperature = 0.5

        if my_path == "":  # if path is not yet chosen
            current_path = os.path.abspath(os.getcwd())

            info = 'Nie wybrano ścieżki zapisu. Czy zapisać w ' + current_path + " ?"
            answer = messagebox.askquestion('Brak ścieżki', info)

            if answer == "yes":
                my_path = current_path
                self.title("Proszę czekać - trwa generowanie dyktanda...")
            else:
                return

        self.title("Proszę czekać - trwa generowanie dyktanda...")
        pitch_final_prediction, rhythm_final_prediction = App.my_engine.generate(temperature, number_of_bars,
                                                                                 time_signature)
        App.my_engine.save_file(pitch_final_prediction, rhythm_final_prediction, my_path, key_signature,
                                tempo, write_midi, write_empty, hints, time_signature)

        self.title("NUTOMAT")
        messagebox.showinfo(title="Informacja", message="Dyktando pomyślnie wygenerowane w {path}".format(path=my_path))
