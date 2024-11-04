import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from lyrics_extractor import SongLyrics
import mysql.connector
from datetime import datetime

# Creating connection object
mydb = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL password
    database="music_lyrics"
)

# Function to insert song name and timestamp into the database
def insert_song_request(song_name):
    cursor = mydb.cursor()
    query = "INSERT INTO song_requests (song_name) VALUES (%s)"
    cursor.execute(query, (song_name,))
    mydb.commit()
    cursor.close()

# Create the main window
window = Tk()
window.geometry('600x700')
window.title('Sandeep Music Lyrics Extractor')
window.configure(bg="#222831")

# Frame for header
header_frame = Frame(window, bg="#393E46")
header_frame.pack(pady=20, padx=20, fill="x")

# Header label
head = Label(header_frame, text="Enter the Song You Want Lyrics For", font=('Helvetica', 18, 'bold'), bg="#00ADB5", fg="white")
head.pack(pady=10)

# Variables to store song name and result
song = tk.StringVar()

# Function to fetch and display lyrics
def get_lyrics():
    song_name = song.get()  # Get the song name entered by the user
    api_key = "AIzaSyAcZ6KgA7pCIa_uf8-bYdWR85vx6-dWqDg"
    engine_id = "aa2313d6c88d1bf22"
    extract_lyrics = SongLyrics(api_key, engine_id)  # Initialize the lyrics extractor
    song_lyrics = extract_lyrics.get_lyrics(song_name)  # Fetch lyrics

    # Display lyrics in the text box
    lyrics_box.config(state=NORMAL)  # Enable editing of the text box
    lyrics_box.delete(1.0, END)  # Clear previous content
    lyrics_box.insert(INSERT, song_lyrics['lyrics'])  # Insert new lyrics
    lyrics_box.config(state=DISABLED)  # Disable editing of the text box

    # Insert song request into the database
    insert_song_request(song_name)

# Entry frame
entry_frame = Frame(window, bg="#393E46")
entry_frame.pack(pady=10, padx=20, fill="x")

# Entry for song name
song_entry = Entry(entry_frame, textvariable=song, font=('Helvetica', 14), width=40, bd=2, relief=GROOVE)
song_entry.pack(pady=10)

# Scrollable text widget to display the lyrics
lyrics_frame = Frame(window, bg="#393E46")
lyrics_frame.pack(pady=10, padx=20, fill="both", expand=True)

lyrics_box = scrolledtext.ScrolledText(
    lyrics_frame, wrap=WORD, width=60, height=20, bg="#EEEEEE", fg="#222831", font=('Calibri', 12), bd=0, relief=GROOVE
)
lyrics_box.pack(pady=10, padx=10, fill="both", expand=True)
lyrics_box.config(state=DISABLED)  # Initially, make the text box read-only

# Button frame for better layout
button_frame = Frame(window, bg="#393E46")
button_frame.pack(pady=10)

# Create GO button to trigger the lyrics fetch
go_button = Button(button_frame, text="Get Lyrics", command=get_lyrics, width=20, font=('Helvetica', 14), bg="#00ADB5", fg="white", bd=0, relief=GROOVE)
go_button.pack(pady=10)

# Start the Tkinter main loop
window.mainloop()
