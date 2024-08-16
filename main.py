import os
from tkinter import *
from tkinter import ttk
from os import startfile

# Check to see if movie list file exists
if os.path.exists("movielist.txt"):
    os.remove("movielist.txt")
else:
    print("Making a new file!")
    f = open("movielist.txt", "x")
    f.close()

# Initialize our window and table
screen = Tk()
screen.title("Movie List: Massive Swag!")
screen.geometry("1000x1200")

table = ttk.Treeview(screen, columns=('index', 'movies', 'filename'), show='headings')
style = ttk.Style()
upDownBar = ttk.Scrollbar(screen, orient="vertical", command=table.yview)
table.configure(yscrollcommand=upDownBar.set)
style.configure("Treeview", background="#EBEFE9")
style.configure("Treeview.Heading", font=("Comic Sans MS", 20))
style.configure("Treeview.columns", font=("Comic Sans MS", 10))
table.heading('index', text="#")
table.heading('movies', text="Video Title:")
table.heading('filename', text="Video Link: ")
table.column("index", width=20)
table.column('movies', width=200)
style.map('Treeview', background=[('selected', 'green')])
upDownBar.pack(side="right", fill="y")
table.tag_configure("odd", background='#F2BC69')
table.tag_configure("even", background='white')


def character_removal(text):
    for ch in ["[", "]", ".", "-", "_", ".mkv", ".mp4", "AnimeRG ", "CBM ", f"\n"]:
        if ch in text:
            text1 = text.replace(ch, "")
            return str(text1)


# Initialize our list
movieList = []
movieTypes = (".mkv", ".avi", ".mp4")
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
            swag5 = swag4.replace(" mkv", "")
            swag6 = swag5.replace("CBM ", "")
            swag7 = swag6.replace("AnimeRG ", "")
            swag8 = swag7.replace("\n", "")
            f.write(swag8 + "@" + root + "\\" + file + "\n")

# find the movie list text file, and read it.
if os.path.exists("movielist.txt"):
    g = open("movielist.txt", "r")
    data = g.readlines()
    data.sort()
    # creating an index that will follow each insert
    dex = 1
    # insert each index + movie combination
    color_dex = 0
    for i in data:
        idx = i.index("@")
        if color_dex % 2 == 0:
            table.insert(parent='', index=dex, values=(dex, i[:idx], i[idx:]), tags='even')
        else:
            table.insert(parent='', index=dex, values=(dex, i[:idx], i[idx:]), tags='odd')
        dex += 1
        color_dex += 1
        g.close()

    table.pack(fill='both', expand=True)


    def item_select(_):
        print(table.selection())
        for x in table.selection():
            z = table.item(x)['values']
            if len(z) == 3:
                movie = z[2]
                print("Now Playing: " + z[1])
                startfile(movie.replace(f'\n', "").replace("@", ""))


    table.bind('<<TreeviewSelect>>', item_select)
    screen.mainloop()