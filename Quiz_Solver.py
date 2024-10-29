import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageGrab
import re
import requests
import json
import pyautogui
import time
import os
import pyperclip
import pytesseract
from coordinate import AreaSelezionata
from tkinter import messagebox
import csv


# Imposta il percorso di Tesseract-OCR (se necessario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specifica la cartella di salvataggio
save_path = "screenshot/"  # Cambia il percorso se necessario

# Crea la cartella se non esiste
if not os.path.exists(save_path):
    os.makedirs(save_path)


save_path_domande = "domande/"  # Cambia il percorso se necessario
if not os.path.exists(save_path_domande):
    os.makedirs(save_path_domande)



# Variabili globali per memorizzare i valori
x_selezione = 1
y_selezione = 1
larghezza_selezione = 1
altezza_selezione = 1

def coordinate_selezione(x, y, larghezza, altezza):
    global x_selezione, y_selezione, larghezza_selezione, altezza_selezione


    # Assegna i valori alle variabili globali
    x_selezione = x
    y_selezione = y
    larghezza_selezione = larghezza
    altezza_selezione = altezza
    #print(f"Coordinate X: {x}, Y: {y}")
    #print(f"Larghezza: {larghezza}, Altezza: {altezza}")


    #Label(tool_bar, text=f"Coord_x : {x}").grid(row=4, column=0, padx=5, pady=5, sticky="W")
    #Label(tool_bar, text=f"Coord_y : {y}").grid(row=5, column=0, padx=5, pady=5, sticky="W")
    #Label(tool_bar, text=f"Altezza : {altezza}").grid(row=6, column=0, padx=5, pady=5, sticky="W")
    #Label(tool_bar, text=f"Largezza: {larghezza}").grid(row=7, column=0, padx=5, pady=5, sticky="W")

    Label(tool_bar, text=f"Coord_x: {x} - Coord_y: {y}").grid(row=4, column=0, padx=5, pady=5)
    Label(tool_bar, text=f"Altezza: {altezza} - Larghezza: {larghezza}").grid(row=5, column=0, padx=5, pady=5)

    Button(tool_bar,text="Disegna Cornice", bg="white",
           command=lambda: disegna_cornice(x_selezione, y_selezione,larghezza_selezione,altezza_selezione)).grid(row=8, column=0, padx=5, pady=5)



def launch():
        global second
        second = Toplevel()
        second.geometry("200x200")

def disegna_cornice(x, y, larghezza, altezza):
    #print(f"Coordinate X: {x}, Y: {y}, Larghezza: {larghezza}, Altezza: {altezza}")
    global frame_cornice

    # Crea una finestra esterna
    frame_cornice = Toplevel()
    frame_cornice.geometry(f"{larghezza}x{altezza}+{x-8}+{y-32}") # Imposta dimensioni (width, height) e coordinate (x, y)

    frame_cornice.title("Finestra Esterna")
    frame_cornice.configure(background="white")

    #frame_cornice.attributes('-alpha', 0.5)
    frame_cornice.wm_attributes("-transparentcolor", "white")

    frame_cornice.mainloop()



def take_screenshot(x, y, width, height):
    # Cattura la porzione specificata dello schermo
    #screenshot = pyautogui.screenshot(region=(x, y, width, height))

    if x == 1 and y == 1 and width == 1 and height == 1:
        messagebox.showwarning("Seleziona un Area", f"Devi prima selezionare un'area!\n Usa il tasto \"Seleziona Area\"")
    else:

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Genera un nome unico per il file
        timestamp = time.strftime("%d%m%Y-%H%M%S")
        file_path = os.path.join(save_path, f"screenshot_{timestamp}.png")
        # Salva lo screenshot
        screenshot.save(file_path)
        print(f"Screenshot salvato in: {file_path}")
        Label(tool_bar, text=f"screenshot_{timestamp}.png").grid(row=12, column=0, padx=5, pady=5)



def soluzione(x, y, width, height):

    if x == 1 and y == 1 and width == 1 and height == 1:
        messagebox.showwarning("Seleziona un Area", f"Devi prima selezionare un'area!\n Usa il tasto \"Seleziona Area\"")
    else:

        # Cattura la porzione specificata dello schermo
        #screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Genera un nome unico per il file
        timestamp = time.strftime("%d%m%Y-%H%M%S")
        file_path = os.path.join(save_path, f"screenshot_{timestamp}.png")
        # Salva lo screenshot
        screenshot.save(file_path)
        print(f"Screenshot salvato in: {file_path}")
        Label(tool_bar, text=f"screenshot_{timestamp}.png").grid(row=12, column=0, padx=5, pady=5)

        testo_ocr = ocr(file_path)
        domanda = converti_testo(testo_ocr)
        response = richiesta_curl(domanda)

        if response.status_code == 200:
            # Converte la risposta in formato JSON
            data = response.json()

            # Estrae il contenuto dalla chiave 'answer' e dalla chiave 'content'
            content = data['answer']['content']

            # Stampa il contenuto
            print(f"Risposta corretta: {content}")

            #Label(tool_bar, text=f"").grid(row=15, column=0, padx=5, pady=5)
            Label(tool_bar, text=f"Risposta: {content}").grid(row=15, column=0, padx=5, pady=5)

            messagebox.showinfo("Risposta", f"Risposta corretta: {content}")

            timestamp = time.strftime("%d%m%Y")
            file_path_domande = os.path.join(save_path_domande, f"domande_risposte_{timestamp}.csv")

            domande = purifica_testo(testo_ocr)
            salva_domande_risposte(domande, content, file_path_domande)

        else:
            print(f"Errore nella richiesta: {response.status_code}")
            messagebox.showerror("Errore", f"Purtroppo qualcosa è andato storto!!! \n {response.status_code}")




def ocr(image_path):

    image = Image.open(image_path)

    # Utilizza pytesseract per fare l'OCR
    text = pytesseract.image_to_string(image)

    # Stampa il testo riconosciuto
    print(f"Testo riconosciuto: {text}")

    return text


def converti_testo(testo):
    #testo = pyperclip.paste()

    # Rimuovi gli spazi
    # Ottieni il testo dagli appunti
    testo_modificato = testo.replace("\n\n", "\n")
    testo_modificato = re.sub(r'\n(?=[^?]*\?)', ' ', testo_modificato)

    domanda_inizio = "Data la domanda \""
    domanda_fine = "\" rispondi senza spiegazione"

    testo_modificato = domanda_inizio + testo_modificato + domanda_fine
    #print(f"text: {testo_modificato}")

    # Rimanda il testo modificato negli appunti
    pyperclip.copy(testo_modificato)
    print("Il testo modificato è stato copiato negli appunti.")

    return testo_modificato


def purifica_testo(testo):

    # Rimuovi gli spazi
    # Ottieni il testo dagli appunti
    testo_modificato = testo.replace("\n\n", "\n")
    testo_modificato = re.sub(r'\n(?=[^?]*\?)', ' ', testo_modificato)

    return testo_modificato



def richiesta_curl(domanda):
    # URL a cui inviare la richiesta
    url = 'https://pizzagpt.it/api/chatx-completion'

    # Dati da inviare (in formato dizionario)
    data = {
        'question': f"{domanda}"
    }

    # Headers da inviare
    headers = {

        'Host': 'pizzagpt.it',
        'X-Secret': 'Marinara',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://pizzagpt.it',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://pizzagpt.it/en'
    }

    # Effettua la richiesta POST
    response = requests.post(url, json=data, headers=headers)

    return response


def salva_domande_risposte(domanda, risposta, nome_file):
    # Controlla se il file esiste già
    file_existente = os.path.isfile(nome_file)

    # Apri il file in modalità append ('a')
    with open(nome_file, mode='a', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv, delimiter=';')

        # Scrivi l'intestazione solo se il file non esiste
        if not file_existente:
            writer.writerow(['domande', 'risposte'])

        # Scrivi la nuova riga con domanda e risposta
        writer.writerow([domanda, risposta])




def funzione_areaselezione():
    app = AreaSelezionata(callback=coordinate_selezione)
    app.mainloop()





root = Tk()  # create root window
root.title("Quiz Solver :)")  # title of the GUI window
#root.iconbitmap("myIcon.ico")
root.iconphoto(False, tk.PhotoImage(file='bacchetta_singola.png'))
#root.geometry("300x500+100+100")  # Imposta dimensioni (width, height) e coordinate (x, y)
#root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


# Create left and right frames
frame = Frame(root, width=200, height=400, bg='grey')
frame.grid(row=0, column=0, padx=10, pady=5)


# Create frames and labels in left_frame
Label(frame, text=" Quiz Solver ", bg='grey', fg="skyblue", font=("Helvetica", 16)).grid(row=0, column=0, padx=5, pady=5)


# Create tool bar frame
tool_bar = Frame(frame, width=280, height=285)
tool_bar.grid(row=2, column=0, padx=5, pady=5)

photo_selezione = tk.PhotoImage(file="selezione.png")
Button(tool_bar,  image=photo_selezione, bg="white", command=funzione_areaselezione).grid(row=1, column=0, padx=5, pady=5)

Label(tool_bar, text="_____________________", font="10", fg="skyblue").grid(row=9, column=0, padx=5, pady=5)

photo_screenshot = tk.PhotoImage(file="screenshot.png")
Button(tool_bar,  image=photo_screenshot, bg="white", command=lambda: take_screenshot(x_selezione, y_selezione, larghezza_selezione, altezza_selezione)).grid(row=11, column=0, padx=5, pady=5)

Label(tool_bar, text="_____________________", font="10", fg="skyblue").grid(row=13, column=0, padx=5, pady=5)

photo_solver = tk.PhotoImage(file="bacchetta.png")
Button(tool_bar,  image=photo_solver, bg="white", command=lambda: soluzione(x_selezione, y_selezione, larghezza_selezione, altezza_selezione)).grid(row=14, column=0, padx=5, pady=5)



root.mainloop()