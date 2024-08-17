import json
import os
import subprocess
import av

from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from os import startfile

# Check to see if movie list file exists
if os.path.exists("movielist.txt"):
    os.remove("movielist.txt")
    print("Movie List Exists!")
else:
    print("Movie List Is Being Created!")
    f = open("movielist.txt", "x")
    f.close()

# Initialize our window and table
screen = Tk()
screen.title("Movie List: Massive Swag!")
screen.geometry("1000x1200")

# Create our table and styling with a vertical scrollbar
table = ttk.Treeview(screen, columns=('index', 'movies', 'filename'), show='headings')
style = ttk.Style()
upDownBar = ttk.Scrollbar(screen, orient="vertical", command=table.yview)
table.configure(yscrollcommand=upDownBar.set)
style.configure("Treeview", rowheight=24, background="#EBEFE9")
style.configure("Treeview.Heading", font=("Comic Sans MS", 20))
style.configure("Treeview.columns", font=("Comic Sans MS", 10))
table.heading('index', text="#")
table.heading('movies', text="Video Title:")
table.heading('filename', text="Video Link: ")
table.column("index", width=35, stretch=0)
table.column('movies', width=200)
style.map('Treeview', background=[('selected', 'green')])
table.tag_configure("odd", background='#F2BC69')
table.tag_configure("even", background='white')
style.configure("Treeview.Rows", font=("Ariel", 10))
upDownBar.pack(side="right", fill="y")


def character_removal(text):
    for ch in ["[", "]", ".", "-", "_", " mkv", " mp4", "AnimeRG ", "CBM ", f"\n", " mp3", ""]:
        if ch in text:
            text1 = text.replace(ch, "")
            return str(text1)


# Initialize our list
movieTypes = (".mkv", ".avi", ".mp3", ".mp4", ".mov", ".webm")
# walk down the D:\\ drive (where movies are stored)
for root, dirs, files in os.walk(r'D:', topdown=False):
    path = root.split(os.sep)
    for file in files:
        # open the movielist text file
        f = open("movielist.txt", "a")
        # clean up the names of files that are movies, and write them to the list file
        if file.endswith(movieTypes):
            swag = file
            swag1 = swag.replace("[", "")
            swag2 = swag1.replace("]", "")
            swag3 = swag2.replace(".", " ")
            swag4 = swag3.replace("_", " ")
            swag5 = swag4.replace(" mkv", "").replace(" avi", "").replace(" mp3", "").replace("mp4", "").replace(" mov", "").replace(" webm", "")
            swag6 = swag5.replace("CBM ", "").replace(" MX", "").replace(" YIFY", "").replace(" 6ch 2ch", "").replace("Rapta", "")
            swag7 = swag6.replace("AnimeRG ", "").replace("H264", "").replace(" Shiv", "").replace("AAC", "").replace("[", "").replace("x264", "")
            swag8 = swag7.replace("\n", "").replace("x265", "").replace("Shiv", "")
            f.write(swag8 + "@" + root + "\\" + file + "\n")

# find the movie list text file, and read it.
if os.path.exists("movielist.txt"):
    g = open("movielist.txt", "r")
    data = g.readlines()
    data.sort()
    # creating an index that will follow each insert
    dex = 1
    # creating an index to determine row color
    color_dex = 0
    # insert each index and video name
    for i in data:
        # index the list around the character '@', which I used to split the data.
        idx = i.index("@")
        # check the color dex with a modulus
        left = character_removal(i[:idx])
        if color_dex % 2 == 0:
            table.insert(parent='', index=dex, values=(dex, left, i[idx:]), tags='even')
        else:
            table.insert(parent='', index=dex, values=(dex, left, i[idx:]), tags='odd')
        dex += 1
        color_dex += 1
        g.close()

    table.pack(fill='both', expand=True)

    # create video opening code onclick
    def item_select(_):
        print(table.selection())
        for x in table.selection():
            z = table.item(x)['values']
            if len(z) == 3:
                movie = z[2]
                container = av.open(movie.replace(f'\n', "").replace("@", ""))
                video_info = container.streams.video[0]
                codec = video_info.codec_context.codec.name
                print("Now Playing: " + character_removal(z[1]))
                print("Codec Information: " + codec)
                startfile(movie.replace(f'\n', "").replace("@", ""))


    table.bind('<<TreeviewSelect>>', item_select)
    screen.mainloop()
