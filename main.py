"""
WHITE = 1
BLACK = -1 
EMPTY = 0 
"""

# [y,x][棋子/陣營]
checkerboard = [[[0 for _ in range(2)] for _ in range(9)] for _ in range(9)]

x = " ABCDEFGH"
y = " 12345678"

chess = (["R", "N", "B", "Q", "K", "B", "N", "R"], "P")
order = {
    "A" : 1,
    "B" : 2,
    "C" : 3,
    "D" : 4,
    "E" : 5,
    "F" : 6,
    "G" : 7,
    "H" : 8,
}

current_player = -1   # 初回合的玩家




def initialization():
    for row in range(9):
        for column in range(9):
            if column == 0:  # y 坐標軸
                checkerboard[row][column][0] = y[8 - row]
                checkerboard[row][column][1] = 0  # 座標無陣營

            elif row == 8:  # x 坐標軸
                checkerboard[row][column][0] = x[column]
                checkerboard[row][column][1] = 0  # 座標無陣營

            elif (row == 0 or row == 7) and column > 0:
                checkerboard[row][column][0] = chess[0][column - 1]
                checkerboard[row][column][1] = 1 if row == 0 else -1  # 陣營 1 或 -1

            elif (row == 1 or row == 6) and column > 0:
                checkerboard[row][column][0] = chess[1]
                checkerboard[row][column][1] = 1 if row == 1 else -1  # 陣營 1 或 -1

            else:
                checkerboard[row][column][0] = " "
                checkerboard[row][column][1] = 0  # 空格子




def refresh_display():
    print("\033[H\033[J", end="")  # 清除之前的画面

    def get_current_player():
        if current_player == -1: return "綠"
        else: return "紅"

    print(f"Chess, Current Player：{get_current_player()}\n")
    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]
            if camp == 1:
                print(f"\033[41m {piece}", end=" \033[0m")  # 红色背景

            elif camp == -1:
                print(f"\033[42m {piece}", end=" \033[0m")  # 綠色背景

            else:
                if column%2 == row%2 and column > 0 and row < 8:
                    print(f"\033[40m {piece}", end=" \033[0m") # 黑色背景
                elif column > 0 and row < 8:
                    print(f"\033[47m {piece}", end=" \033[0m") # 白色背景
                else:
                    print(f" {piece}", end=" ") # 白色背景
        print()




def move(x1, y1, x2, y2):
    global current_player
    # 翻譯指令

    x1 = order.get(x1)
    x2 = order.get(x2)
    try:
        y1 = 8 - int(y1)
        y2 = 8 - int(y2)
    except:
        return "輸入錯誤，請重試"

    # 確認是否違反規則
    if y1 == 8 or y1 < 0 and y2 == 8 or y2 < 0 and x1 == None or x2 == None:
        return "輸入錯誤，請重試"
    
    elif checkerboard[y1][x1][1] != current_player:   # 陣營偵測
        return "非己方，請重試"
    
    elif checkerboard[y2][x2][1] == current_player: # 友軍碰撞偵測
        return "不能吃己方的棋，請重試"
    
    else:   # 單獨棋子種類規則
        if checkerboard[y1][x1][0] == "P":  # 兵
            if checkerboard[y2][x2][1] == -current_player: # 要移動的位置有敵軍
                if (x1+1 == x2 or x1-1 == x2) and abs(y1-y2) == 1:
                    pass
                else:
                    return "違反規則，請重試"

            elif x1 == x2 and abs(y1-y2) == 1:
                pass
            else:
                return "違反規則，請重試"

        elif checkerboard[y1][x1][0] == "R":  # 城堡
            if x1 == x2 or y1 == y2:
                pass
            else: 
                return "違反規則，請重試"

        elif checkerboard[y1][x1][0] == "N":  # 騎士
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            if not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)):
                return "違反規則，請重試"

        elif checkerboard[y1][x1][0] == "B":  # 主教
            if abs(x1 - x2) != abs(y1 - y2):
                return "違反規則，請重試"

        elif checkerboard[y1][x1][0] == "Q":  # 后
            if (abs(x1 - x2) != abs(y1 - y2)) and (x1 != x2) and (y1 != y2):
                return "違反規則，請重試"

        elif checkerboard[y1][x1][0] == "K":  # 王
            if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
                return "違反規則，請重試"


    # 移動棋子
    checkerboard[y2][x2][0] = checkerboard[y1][x1][0]
    checkerboard[y2][x2][1] = checkerboard[y1][x1][1]
    checkerboard[y1][x1][0] = " "
    checkerboard[y1][x1][1] = 0

    current_player = -current_player  # 回合乘負一
    return 0




initialization()    # 初始化遊戲
refresh_display()   # 刷新畫面


while True:
    select = input("Select > ")
    moveto = input("MoveTo > ")
    if len(select + moveto) == 4:
        return_val = move(select[0],select[1],moveto[0],moveto[1])
        if  return_val == 0: # 若回傳為0，代表成功
            refresh_display()
        else:
            refresh_display()
            print(return_val)
        
    else:
        refresh_display()
        print("輸入錯誤，請重試")
    