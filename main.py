import random
import os
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect
from argparse import ArgumentParser
from instaloader import ConnectionException, Instaloader, Post
import instaloader
import subprocess
import time
import sys
import json
import random
import requests
from io import BytesIO



# CREATE WINDOW
def create_window():
    
    global root 
    root = tk.Tk()
    root.title("Random Comment(s)")
    root.geometry("1000x800")
    root.configure(bg="#f0f0f0")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.grid(row=0, column=0, sticky="nsew")

    global canvas
    canvas = tk.Canvas(frame, bg="#f0f0f0", bd=0, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    global content_frame
    content_frame = tk.Frame(canvas, bg="#ffffff", relief="raised", bd=2)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def update_width(event):
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    root.bind("<Configure>", update_width)

    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scroll)

    label_font = ("Helvetica", 16, "bold")
    entry_font = ("Helvetica", 12)
    button_font = ("Helvetica", 12, "bold")
    btn_color = "#4CAF50"
    btn_text_color = "#ffffff"

    label = tk.Label(content_frame, text="Draw Random Comment(s)", font=("Helvetica", 24, "bold"), 
                     fg="#333333", bg="#ffffff")
    label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="n")

    t3 = tk.Label(content_frame, text="Instagram Post Link", font=label_font, fg="#555555", bg="#ffffff")
    t3.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    link = tk.Entry(content_frame, font=entry_font, width=40, bd=2, relief="groove")
    link.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    t4 = tk.Label(content_frame, text="Number of Winners", font=label_font, fg="#555555", bg="#ffffff")
    t4.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    number_comments = tk.Entry(content_frame, font=entry_font, width=20, bd=2, relief="groove")
    number_comments.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    button = tk.Button(content_frame, text="Select Comment(s)", font=button_font, bg=btn_color, fg=btn_text_color,
                       bd=0, relief="raised", padx=10, pady=5, 
                       activebackground="#45a049", activeforeground=btn_text_color,
                       command=lambda: on_click(link, number_comments, result))
    button.grid(row=3, column=0, columnspan=2, pady=20)


    banner = tk.Label(content_frame, text="WINNER(S)", font=("Helvetica", 24, "bold"), fg="#000000", bg="#ffffff")
    banner.grid(row=4, column=0, columnspan=2, pady=20)

    global result
    result = tk.Label(content_frame, text=" ", font=("Helvetica", 18), fg="#333333", bg="#ffffff")
    result.grid(row=5, column=0, columnspan=2, pady=20)

    global winner_frame
    winner_frame = tk.Frame(content_frame, bg="#ffffff")
    winner_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()


def on_click(link, number_comments, result):
    global  _LINK 
    _LINK = link.get()

    global _NUMBER_COMMENTS 
    _NUMBER_COMMENTS = number_comments.get()

    generate_output(result)


# GET COOKIES FOR LOGIN
def get_cookiefile():
    default_cookiefile = {
        "Windows": "~//AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite"
        }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No firefox cookies.sqlite file found")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print('Using cookies from {}'.format(cookiefile))
    conn = connect(f'file:{cookiefile}?immutable=1', uri=True)

    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )

    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()

    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)

    return instaloader, username


# Get Comments
def get_comments(shortcode, _NUMBER_COMMENTS):

    for widget in winner_frame.winfo_children():
        widget.destroy()

    target_dir = shortcode
    number_of_winners = int(_NUMBER_COMMENTS)

    abs_path = os.path.join(os.getcwd(), target_dir)

    # issue
    if os.path.isdir(abs_path):
        for file in os.listdir(abs_path):
            base = os.path.basename(file)
            name, ext = os.path.splitext(base)

            if ext == '.json':
                os.replace(os.path.join(target_dir,base),os.path.join(target_dir,'comments.json'))
                break
    else:
        print('No comments file found.')
        exit(1)

    comments_file = os.path.join(target_dir,'comments.json')

    with open(comments_file, 'r') as file:
        data = json.load(file)


    winners = []
    winner_IDs = []

    if(number_of_winners > len(data)):
        number_of_winners = len(data)

    while len(winners) != number_of_winners:
        index = random.randint(0,len(data)-1)
        candidate = data[index]

        if candidate['owner']['id'] not in winner_IDs:
            winners.append(candidate)
            winner_IDs.append(candidate['owner']['id'])


    info_font = ("Helvetica", 12)
    label_font = ("Helvetica", 14, "bold")
    box_bg = "#ffffff"
    box_border = "#d3d3d3"

    current_row = content_frame.grid_size()[1]  

    for idx, winner in enumerate(winners):

        info_frame = tk.Frame(winner_frame, bg=box_bg, bd=2, relief="groove", padx=20, pady=10)
        info_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

        # Username Label
        username = tk.Label(info_frame, text=f"Username: {winner['owner']['username']}", font=label_font, fg="#333333", bg=box_bg)
        username.pack(anchor="w", pady=2)

        # Comment Label
        comment = tk.Label(info_frame, text=f"Comment: {winner['text']}", font=info_font, fg="#555555", bg=box_bg, wraplength=800, justify="left")
        comment.pack(anchor="w", pady=2)

        # Instagram ID Label
        user_id = tk.Label(info_frame, text=f"Instagram ID: {winner['owner']['id']}", font=info_font, fg="#777777", bg=box_bg)
        user_id.pack(anchor="w", pady=2)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


# Main logic
def generate_output(result_box):

    session_file = open('session_file','w')

    temp = import_session(get_cookiefile(), 'session_file')
    loader = temp[0]
    username = temp[1]

    temp = _LINK.split('/')
    shortcode = temp[len(temp)-2]

    # Establish session, get cookie data
    # Command needs: username, shortcode
    command = f'python -m instaloader --comments -l {username} --sessionfile=session_file -- -{shortcode}'
    result = subprocess.run(command, shell=True,capture_output=True, text=True)

    with open('test.txt','w') as file:
        file.write(result.stderr)

    temp = ''
    with open('test.txt','r') as file:
        for i in file.readlines():
            time.sleep(1)
            result_box.config(text=i.strip())
            root.update()

    result_box.config(text=" ")
    # Get comments
    # Needs: shortcode, number_comments
    get_comments(f'-{shortcode}', _NUMBER_COMMENTS)

    root.update()



if __name__ == "__main__":

    create_window()




