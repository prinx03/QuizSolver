import tkinter as tk


class AreaSelezionata(tk.Tk):
    def __init__(self, callback=None):
        super().__init__()

        self.geometry("800x600")  # Dimensione della finestra principale
        self.attributes('-fullscreen', True)  # Finestra a schermo intero

        self.overrideredirect(True)  # Rimuove la barra del titolo

        self.canvas = tk.Canvas(self, bg='white', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.attributes('-alpha', 0.5)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.callback = callback  # Memorizza il callback passato come argomento

        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='blue', fill='blue', stipple='gray50'
        )

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.rect:
            end_x, end_y = event.x, event.y
            width = end_x - self.start_x
            height = end_y - self.start_y
            x, y = self.start_x, self.start_y

            # Chiamata al callback con i valori di selezione
            if self.callback:
                self.callback(x, y, width, height)

            # Chiude l'applicazione dopo la selezione
            self.destroy()



#if __name__ == "__main__":
#    app = AreaSelezionata()
#    app.mainloop()

