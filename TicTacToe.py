import tkinter
import random

color_background = "#7F8F79"      
color_grid = "#696A69"            
color_hover = "#AEAFAE"           
color_x = "#947409"               
color_o = "#694D2C"              
color_button = "#204227"         
color_winning = "#3B683E"       
color_win_bg = "#749E7A"         

#  المتغيرات
playerX = "X"
playerO = "O"
curr_player = playerX
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

turns = 0
game_over = False

# عداد الفوز
score_x = 0
score_o = 0

# وضعي اللعب
mode = "PvP"  # الوضع الافتراضي

# المؤقت
timer_seconds = 7
timer_remaining = timer_seconds
timer_running = False
timer_id = None


def stop_timer():
    global timer_id, timer_running
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    timer_running = False

def update_timer_label():
    
    if game_over:
        return
    if timer_running and not game_over:
        label.config(text=f"{curr_player}'s turn ({timer_remaining}s)")
    else:
        label.config(text=f"{curr_player}'s turn")

def start_timer():
    global timer_remaining, timer_id, timer_running
    stop_timer()
    if game_over:
        return
    # شغل المؤقت فقط اذا كان الدور للاعب بشري
    if mode == "PvP" or (mode == "PvE" and curr_player == playerX):
        timer_remaining = timer_seconds
        timer_running = True
        update_timer_label()
        timer_tick()
    else:
        #دور الكمبيوتر لا مؤقت 
        timer_running = False
        update_timer_label()

def timer_tick():
    global timer_remaining, timer_id, timer_running
    if not timer_running or game_over:
        return
    timer_remaining -= 1
    update_timer_label()
    if timer_remaining <= 0:
        stop_timer()
        timeout_switch()
    else:
        timer_id = window.after(1000, timer_tick)

def timeout_switch():
    
    global curr_player
    if game_over:
        return
    # تبديل اللاعب
    if curr_player == playerX:
        curr_player = playerO
    else:
        curr_player = playerX


    if mode == "PvE" and curr_player == playerO:
        stop_timer()
        update_timer_label()
        window.after(100, ai_move) 
    else:
    
        start_timer()


def set_tile(row, column):
    global curr_player

    if game_over:
        return
    if board[row][column]["text"] != "":
        return

    # تعيين الخانة بلون اللاعب المناسب
    if curr_player == playerX:
        board[row][column].config(text=curr_player, foreground=color_x)
    else:
        board[row][column].config(text=curr_player, foreground=color_o)

    # تبديل اللاعب
    if curr_player == playerO:
        curr_player = playerX
    else:
        curr_player = playerO

    # التحقق من الفوز
    check_winner()

    # اذا اللعبة لم تنته اعد ضبط المؤقت للاعب الجديد
    if not game_over:
        start_timer()
    else:
        stop_timer()

    
    if not game_over and mode == "PvE" and curr_player == playerO:
        window.after(200, ai_move) 

def check_winner():
    global turns, game_over, score_x, score_o
    turns += 1

    # افقيا
    for row in range(3):
        if (board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"]
                and board[row][0]["text"] != ""):
            winner = board[row][0]["text"]
            label.config(text=f"{winner} is the winner!", foreground=color_winning)
            for col in range(3):
                board[row][col].config(foreground=color_winning, background=color_win_bg)
            game_over = True
            update_score(winner)
            stop_timer()
            return

    # عموديا
    for col in range(3):
        if (board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"]
                and board[0][col]["text"] != ""):
            winner = board[0][col]["text"]
            label.config(text=f"{winner} is the winner!", foreground=color_winning)
            for row in range(3):
                board[row][col].config(foreground=color_winning, background=color_win_bg)
            game_over = True
            update_score(winner)
            stop_timer()
            return

    # قطر رئيسي
    if (board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"]
            and board[0][0]["text"] != ""):
        winner = board[0][0]["text"]
        label.config(text=f"{winner} is the winner!", foreground=color_winning)
        for i in range(3):
            board[i][i].config(foreground=color_winning, background=color_win_bg)
        game_over = True
        update_score(winner)
        stop_timer()
        return

    # قطر ثانوي
    if (board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"]
            and board[0][2]["text"] != ""):
        winner = board[0][2]["text"]
        label.config(text=f"{winner} is the winner!", foreground=color_winning)
        board[0][2].config(foreground=color_winning, background=color_win_bg)
        board[1][1].config(foreground=color_winning, background=color_win_bg)
        board[2][0].config(foreground=color_winning, background=color_win_bg)
        game_over = True
        update_score(winner)
        stop_timer()
        return

    # تعادل
    if turns == 9:
        game_over = True
        label.config(text="Tie!", foreground=color_winning)
        stop_timer()

def update_score(winner):
    global score_x, score_o
    if winner == playerX:
        score_x += 1
    elif winner == playerO:
        score_o += 1
    update_score_display()

def update_score_display():
    score_label.config(text=f"X: {score_x}   O: {score_o}")

def new_game():
    global turns, game_over, curr_player
    turns = 0
    game_over = False
    curr_player = playerX  # X يبدا دائما

    
    for row in range(3):
        for col in range(3):
            board[row][col].config(text="", foreground=color_x, background=color_grid)

    
    stop_timer()
    start_timer()  
    update_score_display()


def ai_move():
    if game_over:
        return

    # البحث عن خانات فارغة
    empty_cells = []
    for row in range(3):
        for col in range(3):
            if board[row][col]["text"] == "":
                empty_cells.append((row, col))

    if not empty_cells:
        return

    # اختيار عشوائي
    row, col = random.choice(empty_cells)

    # تاكد ان الخانة ما زالت فارغة تجنب التكرار
    if board[row][col]["text"] != "":
        return

    
    board[row][col].config(text=playerO, foreground=color_o)

    
    check_winner()


    if not game_over:
        global curr_player
        curr_player = playerX
        start_timer()
    else:
        stop_timer()


def on_enter(event):
    if game_over:
        return
    button = event.widget
    if button["text"] == "":  # خانة فارغة
        button.config(background=color_hover)

def on_leave(event):
    if game_over:
        return
    button = event.widget
    if button["text"] == "":  # فقط للخانات الفارغة نعيد اللون
        button.config(background=color_grid)


def toggle_mode():
    global mode
    if mode == "PvP":
        mode = "PvE"
        mode_button.config(text="Mode: PvE")
    else:
        mode = "PvP"
        mode_button.config(text="Mode: PvP")

    
    if not game_over:
        if mode == "PvE" and curr_player == playerO:
        
            stop_timer()
            window.after(100, ai_move)
        else:
            
            start_timer()

# اعداد النافدة
window = tkinter.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)
window.configure(background=color_background)

frame = tkinter.Frame(window, background=color_background)
frame.pack()

# تسمية الدور والمؤقت
label = tkinter.Label(frame, text=curr_player + "'s turn", font=("Consolas", 20),
                      background=color_background, foreground="white")
label.grid(row=0, column=0, columnspan=3, sticky="we", pady=(10, 5))


for row in range(3):
    for col in range(3):
        btn = tkinter.Button(frame, text="", font=("Consolas", 50, "bold"),
                             background=color_grid, foreground=color_x,
                             width=4, height=1,
                             command=lambda r=row, c=col: set_tile(r, c))
        btn.grid(row=row+1, column=col, padx=2, pady=2)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        board[row][col] = btn

# عداد الفوز
score_label = tkinter.Label(frame, text="X: 0   O: 0", font=("Consolas", 16),
                            background=color_background, foreground="white")
score_label.grid(row=4, column=0, columnspan=3, pady=(10, 5))

# اطار الازرار السفلية
buttons_frame = tkinter.Frame(frame, background=color_background)
buttons_frame.grid(row=5, column=0, columnspan=3, pady=(5, 10))

# زر اعادة اللعبة
restart_button = tkinter.Button(buttons_frame, text="Restart", font=("Consolas", 16),
                                background=color_button, foreground="white",
                                command=new_game)
restart_button.pack(side=tkinter.LEFT, padx=(0, 20))

# زر تبديل الوضع
mode_button = tkinter.Button(buttons_frame, text="Mode: PvP", font=("Consolas", 16),
                             background=color_button, foreground="white",
                             command=toggle_mode)
mode_button.pack(side=tkinter.LEFT)

# توسيط النافذة
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# بدءالمؤقت لاول مرة
start_timer()

window.mainloop()