import tkinter as tk
from openai import OpenAI
import threading
import os


def creation_of_board():
    global UL, UM, UR, ML, M, MR, LL, LM, LR
    global buttons
    global game_frame
    buttons = {}
    button.destroy()
    frame.destroy()
    game_frame = tk.Frame(root)
    game_frame.pack(fill=tk.BOTH, expand=True)

    buttons['UL'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('UL', buttons['UL']))
    buttons['UM'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('UM', buttons['UM']))
    buttons['UR'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('UR', buttons['UR']))
    buttons['ML'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('ML', buttons['ML']))
    buttons['M'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                             command=lambda: on_click('M', buttons['M']))
    buttons['MR'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('MR', buttons['MR']))
    buttons['LL'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('LL', buttons['LL']))
    buttons['LM'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('LM', buttons['LM']))
    buttons['LR'] = tk.Button(game_frame, text='', font=("Times_New_Roman", 18, "bold"),
                              command=lambda: on_click('LR', buttons['LR']))

    # Placing buttons on the grid
    buttons['UL'].grid(row=0, column=0, sticky="nsew")
    buttons['UM'].grid(row=0, column=1, sticky="nsew")
    buttons['UR'].grid(row=0, column=2, sticky="nsew")
    buttons['ML'].grid(row=1, column=0, sticky="nsew")
    buttons['M'].grid(row=1, column=1, sticky="nsew")
    buttons['MR'].grid(row=1, column=2, sticky="nsew")
    buttons['LL'].grid(row=2, column=0, sticky="nsew")
    buttons['LM'].grid(row=2, column=1, sticky="nsew")
    buttons['LR'].grid(row=2, column=2, sticky="nsew")

    for i in range(3):
        game_frame.grid_rowconfigure(i, weight=1)
        game_frame.grid_columnconfigure(i, weight=1)


def on_click(square_name, button):
    global players_turn, total_moves, game_is_over
    if game_is_over:
        return
    if (players_turn and button['text'] == ''):
        button['text'] = 'X'
        players_turn = False
        total_moves += 1
        players_moves.append(square_name)
        button.config(state=tk.DISABLED)
    if total_moves >= 4:
        check_winner('X')
    elif total_moves == 9:
        print("game is a draw nobody wins")
        game_over()
    else:
        ai_turn()


def ai_turn():
    def make_ai_move():
        global total_moves, players_moves, ai_moves, game_is_over,players_turn
        prompt = (
            "You are playing Tic Tac Toe against an opponent. UR stands for upper right, UM stands for upper middle, "
            "UL stands for upper left, MR stands for middle right, M stands for middle, ML stands for middle left, "
            "LR stands for lower right, LM stands for lower middle, and LL stands for lower left. "
            f"The current moves of the opponent are: {players_moves}. Your moves are: {ai_moves}. "
            "Prioritize making a winning move. If no winning move is available, block the opponent from winning. "
            "Respond with only UR, UM, UL, MR, M, ML, LR, LM, or LL."
        )


        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4",
            max_tokens=1,
            temperature=0
        )

        ai_current_move = response.choices[0].message.content
        ai_moves.append(ai_current_move)

        ai_current_move_button = buttons[ai_current_move]
        ai_current_move_button['text'] = 'O'
        ai_current_move_button.config(state=tk.DISABLED)

        players_turn = True
        total_moves += 1
        if total_moves >= 6:
            check_winner('O')


    threading.Thread(target=make_ai_move).start()


def check_winner(player):
    winning_combinations = [
        ['UL', 'UM', 'UR'],
        ['ML', 'M', 'MR'],
        ['LL', 'LM', 'LR'],
        ['UL', 'ML', 'LL'],
        ['UM', 'M', 'LM'],
        ['UR', 'MR', 'LR'],
        ['UL', 'M', 'LR'],
        ['UR', 'M', 'LL']
    ]
    for three_in_a_row in winning_combinations:
        global game_is_over
        if all(buttons[pos]['text'] == player for pos in three_in_a_row):
            print(f"Player {player} wins!")
            for btn in buttons.values():
                btn.config(state=tk.DISABLED)
            game_is_over = True
            game_over()
            return


def game_over():
    game_frame.destroy()

    end_game_screen = tk.Frame(root)
    end_game_screen.pack(fill=tk.BOTH, expand=True)


    message = tk.Label(end_game_screen, text="Game Over! Play Again?", font=("Times_New_Roman", 24, "bold"))
    message.pack(pady=20)


    button_frame = tk.Frame(end_game_screen)
    button_frame.pack()

    yes_button = tk.Button(button_frame, text="YES", command=lambda: restart_game(end_game_screen), font=("Times_New_Roman", 18, "bold"))
    yes_button.pack(side=tk.LEFT, padx=20)

    no_button = tk.Button(button_frame, text="NO", command=root.destroy, font=("Times_New_Roman", 18, "bold"))
    no_button.pack(side=tk.RIGHT, padx=20)


def restart_game(end_game_screen):
    global game_is_over, players_turn, players_moves, ai_moves, total_moves
    end_game_screen.destroy()
    game_is_over = False
    players_turn = True
    players_moves = []
    ai_moves = []
    total_moves = 0
    creation_of_board()

root = tk.Tk()
root.title('Tic Tac Toe vs AI')
root.geometry("900x700")
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
game_is_over = False
players_turn = True
players_moves = []
ai_moves = []
total_moves = 0
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )
button = tk.Button(frame, text="Play", command=creation_of_board, font=("Times_New_Roman", 18, "bold"))
button.pack(expand=True)
root.mainloop()
