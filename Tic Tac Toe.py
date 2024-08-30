import tkinter as tk
def game_started():
    print('button pushed')
    button.destroy()






root = tk.Tk()
root.title('Tic Tac Toe vs AI')
root.geometry("900x700")
button = tk.Button(root, text="Play", command=game_started, font=("Times_New_Roman", 18, "bold"))
button.pack(side="top",pady=300)
root.mainloop()