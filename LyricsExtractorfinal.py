import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
import re
from azapi import AZlyrics


logging.basicConfig(level=logging.DEBUG)

def preprocess_name(name):
    """
    Clean up the artist and song name for AZLyrics search.
    Convert spaces to empty strings, lowercase the name, and remove special characters.
    """
    return re.sub(r"[^a-zA-Z0-9]", "", name.lower())  

def try_fetch_lyrics(artist, song):
    az = AZlyrics()

    # Preprocess the artist and song names
    az.artist = preprocess_name(artist)
    az.title = preprocess_name(song)

    # First, try to fetch lyrics without suffixes
    try:
        lyrics = az.getLyrics()
        if lyrics:
            return lyrics
    except Exception as e:
        logging.warning(f"Base URL failed: {str(e)}")
    
    # If lyrics weren't found, attempt to try with numeric suffixes
    suffixes = ['112602', '1234', '5678', '91011']
    
    for suffix in suffixes:
        modified_url = f"https://www.azlyrics.com/lyrics/{az.artist}/{az.title}{suffix}.html"
        logging.debug(f"Trying URL with suffix: {modified_url}")
        
        try:
            lyrics = az.getLyrics()
            if lyrics:
                return lyrics
        except Exception as e:
            logging.warning(f"Failed with suffix {suffix}: {str(e)}")
            continue  # Try the next suffix if the current one fails
    
    # If no lyrics are found
    return "Lyrics not found on AZLyrics. Please check the artist or song name."

def fetch_lyrics(artist, song):
    """
    Fetch lyrics using azapi library with proper error handling.
    """
    try:
        lyrics = try_fetch_lyrics(artist, song)
        return lyrics
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def get_lyrics():
    """
    Fetch and display lyrics based on user input.
    """
    artist = artist_entry.get().strip()
    song = song_entry.get().strip()

    if not artist or not song:
        messagebox.showerror("Input Error", "Please enter both artist and song name.")
        return

    lyrics = fetch_lyrics(artist, song)
    lyrics_box.delete(1.0, tk.END)  # Clear previous content
    lyrics_box.insert(tk.END, f"Lyrics for {song.title()} by {artist.title()}:\n\n{lyrics}")

# GUI setup
root = tk.Tk()
root.title("GetUrLyrics")

# Input fields
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Artist Name:").grid(row=0, column=0, padx=5, pady=5)
artist_entry = tk.Entry(frame, width=30)
artist_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Song Name:").grid(row=1, column=0, padx=5, pady=5)
song_entry = tk.Entry(frame, width=30)
song_entry.grid(row=1, column=1, padx=5, pady=5)

search_button = tk.Button(frame, text="Get Lyrics", command=get_lyrics)
search_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

# Lyrics display
lyrics_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
lyrics_box.pack(pady=10)

# Run the app
root.mainloop()
