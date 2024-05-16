import tkinter as tk

root = tk.Tk()
root.attributes('-fullscreen', True)

quit = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit.place(x=10,y=10)

root.mainloop()
