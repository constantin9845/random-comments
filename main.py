import instaloader
import os
import random
import tkinter as tk
from PIL import Image, ImageTk

loader = instaloader.Instaloader()



root = tk.Tk()
root.title("Random Comment")
root.geometry("800x800")

label = tk.Label(root, text="Draw Random Comment", font=("Arial", 14))
label.pack(pady=20)

t1 = tk.Label(root, text="Username", font=("Arial", 8))
t1.pack()
username = tk.Entry(root, font=("Arial", 14))
username.pack(pady=5)

t2 = tk.Label(root, text="Password", font=("Arial", 8))
t2.pack()
password = tk.Entry(root, font=("Arial", 14))
password.pack(pady=5)

t3 = tk.Label(root, text="Instagram Post Link", font=("Arial", 8))
t3.pack()
link = tk.Entry(root, font=("Arial", 14))
link.pack(pady=5)

t4 = tk.Label(root, text='Number of Comments', font=("Arial", 8))
t4.pack()
number_comments = tk.Entry(root, font=("Arial", 14))
number_comments.pack()


banner = tk.Label(root, text='WINNER(S)', font=("Arial", 20))
banner.pack(pady=20)

img_path = 'arsenal/Unknown_person.jpg'
img = Image.open(img_path).resize((300,300))

photo = ImageTk.PhotoImage(img)

res = tk.Label(root, image=photo)
res.pack(pady=5)

result = tk.Label(root, text='________________________________', font=("Arial", 16))
result.pack(pady=20)

def on_click(number):
    # Get all comments
    # select random comment
    # display result

    '''
    loader = instaloader.Instaloader()

    username = t1.get()
    password = t2.get()
    link = t3.get()
    temp = link.split('/')
    shortcode = temp[len(temp)-2]

    loader.login(username, password)

    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    comments = post.get_comments()

    winners = []

    while len(winners) != number:
        winner = comments[random.randint(0,len(comments)-1)]
        if winner not in winners:
            winners.append(winner)
            
    winnerString = ""
    for i in winners:
        winnerString += f'Username: {i.owner.username}\n Comment: {i.text} \n Date: {i.created_at_utc} \n ID: {i.owner_id} \n '


    result.config(text=winnerString)

    # POSSIBLY RETURN OTHER INFO OF USER LIKE IG ID (easier to contact)
    '''

    img_path2 = 'arsenal/test.jpg'
    img2 = Image.open(img_path2).resize((300,300))

    photo2 = ImageTk.PhotoImage(img2)

    res.config(image=photo2)
    res.image = photo2

    result.config(text=f"Marron: I need this price!!! {number}")

button = tk.Button(root, text="Select Comment(s)", command=lambda: on_click(number_comments.get()))
button.pack(pady=10)


root.mainloop()


## WILL NEED SCROLLBAR -> SEE CANVAS