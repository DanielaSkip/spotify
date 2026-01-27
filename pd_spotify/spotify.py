import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

conn = sqlite3.connect("spotifi.db")
cursor = conn.cursor()

window = tk.Tk()
window.title("Spotify Playlist App")
window.geometry("520x520")
window.configure(bg="#121212")

style = ttk.Style()
style.theme_use("default")

style.configure("TLabel",
    background="#121212",
    foreground="white",
    font=("Segoe UI", 10)
)

style.configure("Title.TLabel",
    font=("Segoe UI", 18, "bold"),
    foreground="#1DB954"
)

style.configure("TEntry",
    font=("Segoe UI", 10),
    padding=6
)

style.configure("TButton",
    font=("Segoe UI", 10, "bold"),
    padding=8,
    background="#1DB954"
)

style.map("TButton",
    background=[("active", "#1ed760")]
)


ttk.Label(window, text="🎧 Spotify Atskaņošanas Saraksts ", style="Title.TLabel").pack(pady=15)

card = tk.Frame(window, bg="#181818", bd=0)
card.pack(padx=20, pady=10, fill="both", expand=True)

def label(text):
    ttk.Label(card, text=text).pack(anchor="w", padx=20, pady=(12, 4))

def entry(var):
    ttk.Entry(card, textvariable=var, width=40).pack(anchor="w", padx=20)


label("Lietotāja vārds")
user_var = tk.StringVar()
entry(user_var)


label("Žanrs")
genre_var = tk.StringVar()

genre_frame = tk.Frame(card, bg="#181818")
genre_frame.pack(anchor="w", padx=20)

for g in ["pop", "roks", "hip-hops", "jazz"]:
    ttk.Radiobutton(
        genre_frame,
        text=g.capitalize(),
        variable=genre_var,
        value=g
    ).pack(side="left", padx=5)


label("Mākslinieks")
artist_var = tk.StringVar()
entry(artist_var)


label("Dziesma")
song_var = tk.StringVar()
entry(song_var)


label("Atskaņošanas saraksta nosaukums")
playlist_var = tk.StringVar()
entry(playlist_var)


def save_all():
    if not all([user_var.get(), genre_var.get(), artist_var.get(), song_var.get(), playlist_var.get()]):
        messagebox.showerror("Kļūda", "Aizpildiet visus laukus")
        return

    cursor.execute(
        "INSERT INTO lietotaji (lietotaja_vards, email, parole) VALUES (?, '', '')",
        (user_var.get(),)
    )
    user_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO makslinieki (makslinieka_vards, biografija, valsts) VALUES (?, '', '')",
        (artist_var.get(),)
    )
    artist_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO albumi (nosaukums, zanrs, izveidosanas_datums, makslinieks_id) VALUES (?, ?, '', ?)",
        ("Single", genre_var.get(), artist_id)
    )
    album_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO dziesmas (nosaukums, garums_min, albums_id) VALUES (?, 0, ?)",
        (song_var.get(), album_id)
    )
    song_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO playlisti (nosaukums, dziesma_id, lietotajs_id) VALUES (?, ?, ?)",
        (playlist_var.get(), song_id, user_id)
    )

    conn.commit()
    messagebox.showinfo("Veiksmīgi", "🎉 Dziesma pievienota atskaņošanas sarakstam!")


def show_playlist():
    name = simpledialog.askstring("Atskaņošanas saraksts", "Ievadiet atskaņošanas saraksta nosakumu:")
    if not name:
        return

    cursor.execute("""
        SELECT lietotaji.lietotaja_vards, makslinieki.makslinieka_vards, dziesmas.nosaukums
        FROM playlisti
        JOIN lietotaji ON playlisti.lietotajs_id = lietotaji.lietotajs_id
        JOIN dziesmas ON playlisti.dziesma_id = dziesmas.dziesma_id
        JOIN albumi ON dziesmas.albums_id = albumi.albums_id
        JOIN makslinieki ON albumi.makslinieks_id = makslinieki.makslinieks_id
        WHERE playlisti.nosaukums = ?
    """, (name,))

    rows = cursor.fetchall()
    text = ""
    for r in rows:
        text += f"👤 {r[0]}\n🎤 {r[1]}\n🎵 {r[2]}\n\n"

    messagebox.showinfo("Atskaņošanas saraksts", text or "Atskaņošanas saraksts nav atrasts")


btn_frame = tk.Frame(window, bg="#121212")
btn_frame.pack(pady=20)

ttk.Button(btn_frame, text="➕ SAGLABĀT ATSKAŅOŠANAS SARAKSTĀ", command=save_all).pack(side="left", padx=10)
ttk.Button(btn_frame, text="📂 RĀDĪT ATSKAŅOŠANAS SARAKSTU", command=show_playlist).pack(side="left", padx=10)

window.mainloop()
conn.close()
