# 宣告 棋盤 陣列
checkerboard = [[[0 for _ in range(2)] for _ in range(9)] for _ in range(9)]
# 9x9x2 陣列，第一層為棋盤，第二層紀錄陣營

game_over = False

RED = 1
GREEN = -1
VOID = 0

current_player = GREEN   # 初回合的玩家




def initialization(): # 遊戲初始化
    chess = (["R", "N", "B", "Q", "K", "B", "N", "R"], "P") # 棋子擺放順序
    x_axis = " ABCDEFGH" # x軸的對應字母

    for row in range(9):
        for column in range(9):
            if row == 8:  # x 坐標軸
                checkerboard[row][column][0] = x_axis[column]
                checkerboard[row][column][1] = VOID  # 座標無陣營
            
            elif column == 0:  # y 坐標軸
                checkerboard[row][column][0] = 8 - row
                checkerboard[row][column][1] = VOID  # 座標無陣營
            
            elif column > 0:
                if row == 0:
                    checkerboard[row][column][0] = chess[0][column - 1]
                    checkerboard[row][column][1] = RED

                elif row == 1:
                    checkerboard[row][column][0] = chess[1]
                    checkerboard[row][column][1] = RED

                elif row == 6:
                    checkerboard[row][column][0] = chess[1]
                    checkerboard[row][column][1] = GREEN

                elif row == 7:
                    checkerboard[row][column][0] = chess[0][column - 1]
                    checkerboard[row][column][1] = GREEN

                else:
                    checkerboard[row][column][0] = " "
                    checkerboard[row][column][1] = VOID
    return 0
        

          

def refresh_display(error_msg=""):
    def get_current_player():
        if current_player == GREEN: 
            return "G"
        else: 
            return "R"
        
    print("\033[H\033[J", end=" ")  # 清除之前的畫面
    print(f"Chess, Current Player：{get_current_player()} ")

    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]

            if camp == RED:   # 陣營為紅方
                print(f"\033[41m {piece}", end=" \033[0m")  # 红色背景

            elif camp == GREEN:# 陣營為綠方
                print(f"\033[42m {piece}", end=" \033[0m")  # 綠色背景

            else:           # 無陣營 (空)
                if column%2 == row%2 and column > 0 and row < 8:
                    print(f"\033[40m {piece}", end=" \033[0m") # 黑色背景
                elif column > 0 and row < 8:
                    print(f"\033[47m {piece}", end=" \033[0m") # 白色背景
                else:  # 坐標軸
                    print(f" {piece}", end=" ")
        print()

    print(error_msg)
    return 0




def convert_position(x, y):
    """Convert chess position from algebraic notation to board indices."""
    table = {
        "A": 1, "B": 2, "C": 3, "D": 4,
        "E": 5, "F": 6, "G": 7, "H": 8,
    }
    try:
        x = table.get(str.upper(x))
        y = 8 - int(y)
        return x, y
    except:
        raise ValueError("輸入格式錯誤，請重試")
    

def cover(x1, y1, x2, y2):
    """Check if there is any piece between (x1, y1) and (x2, y2)."""
    if x1 > x2:
        dirx = -1
    elif x1 < x2:
        dirx = 1
    else:
        dirx = 0

    if y1 > y2:
        diry = -1
    elif y1 < y2:
        diry = 1
    else:
        diry = 0

    movepoint_x = x1
    movepoint_y = y1
    while movepoint_x != x2 or movepoint_y != y2:
        movepoint_x += dirx
        movepoint_y += diry
        if checkerboard[movepoint_y][movepoint_x][1] == VOID:
            continue
        elif movepoint_x == x2 and movepoint_y == y2:
            continue
        else:
            return -1
    return 0


def pawn_rule(x1, y1, x2, y2, current_player):
    """Check the movement rules for pawns."""
    if current_player == RED:  # Red player
        dy = y2 - y1
    else:  # Green player
        dy = y1 - y2

    if (current_player == RED and y2 == 7) or (current_player == GREEN and y2 == 0):
        checkerboard[y1][x1][0] = "Q"

    if checkerboard[y2][x2][1] == -current_player:  # Capture move
        if abs(x1 - x2) == 1 and dy == 1:
            return 0
        else:
            return "違反吃過路兵規則，請重試"

    elif (current_player == RED and y1 == 1) or (current_player == GREEN and y1 == 6):  # First move can advance 1 or 2 squares
        if x1 == x2 and 0 < dy <= 2:
            if cover(x1, y1, x2, y2) != 0:
                return "Err -1 路徑有棋子"
            return 0
        else:
            return "違反兵規則，請重試"

    else:
        if x1 == x2 and dy > 1: #### TEST
            return 0
        else:
            return "違反兵規則，請重試"



def rook_rule(x1, y1, x2, y2):
    """Check the movement rules for rooks."""
    if x1 == x2 or y1 == y2:
        if cover(x1, y1, x2, y2) != 0:
            return "Err 0 路徑有棋子"
        return 0
    else:
        return "違反城堡規則，請重試"


def knight_rule(x1, y1, x2, y2):
    """Check the movement rules for knights."""
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
        return 0
    else:
        return "違反騎士規則，請重試"


def bishop_rule(x1, y1, x2, y2):
    """Check the movement rules for bishops."""
    if abs(x1 - x2) == abs(y1 - y2):
        if cover(x1, y1, x2, y2) != 0:
            return "Err 1 路徑有棋子"
        return 0
    else:
        return "違反主教規則，請重試"


def queen_rule(x1, y1, x2, y2):
    """Check the movement rules for queens."""
    if (abs(x1 - x2) == abs(y1 - y2)) or (x1 == x2) or (y1 == y2):
        if cover(x1, y1, x2, y2) != 0:
            return "Err 2 路徑有棋子"
        return 0
    else:
        return "違反后規則，請重試"


def king_rule(x1, y1, x2, y2):
    """Check the movement rules for kings."""
    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        return 0
    else:
        return "違反王規則，請重試"


def rules(x1, y1, x2, y2):
    global current_player

    try:
        x1, y1 = convert_position(x1, y1)
        x2, y2 = convert_position(x2, y2)
    except ValueError as e:
        return str(e)

    if y1 == 8 or y1 < 0 or y2 == 8 or y2 < 0 or x1 is None or x2 is None:
        return "輸入範圍錯誤，請重試"

    if checkerboard[y1][x1][1] != current_player:
        return "非己方，請重試"

    if checkerboard[y2][x2][1] == current_player:
        return "不能吃己方的棋，請重試"

    piece = checkerboard[y1][x1][0]
    if piece == "P":
        result = pawn_rule(x1, y1, x2, y2, current_player)
    elif piece == "R":
        result = rook_rule(x1, y1, x2, y2)
    elif piece == "N":
        result = knight_rule(x1, y1, x2, y2)
    elif piece == "B":
        result = bishop_rule(x1, y1, x2, y2)
    elif piece == "Q":
        result = queen_rule(x1, y1, x2, y2)
    elif piece == "K":
        result = king_rule(x1, y1, x2, y2)
    else:
        return "未知的棋子類型"

    if result != 0:
        return result

    # 移動棋子
    checkerboard[y2][x2][0] = piece
    checkerboard[y2][x2][1] = checkerboard[y1][x1][1]
    checkerboard[y1][x1][0] = " "
    checkerboard[y1][x1][1] = 0

    current_player = -current_player  # 回合乘負一
    return 0




initialization()    # 初始化遊戲

checkerboard[1][1][0] = "P"
checkerboard[1][1][1] = GREEN
refresh_display()   # 刷新畫面





def check():
    king_coordinate = []
    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]
            if piece == "K":
                king_coordinate.append((row,column,camp))

    
    return king_coordinate


while not(game_over):
    print(check())
    select = input("Select > ")
    moveto = input("MoveTo > ")
    if len(select + moveto) == 4:
        return_val = rules(select[0],select[1],moveto[0],moveto[1])
        if  return_val == 0: # 若回傳為0，代表成功
            refresh_display()
        else:
            refresh_display(return_val)
        
    else:
        refresh_display("輸入錯誤，請重試")