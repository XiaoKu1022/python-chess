# 宣告 棋盤 陣列
checkerboard = [[[0 for _ in range(2)] for _ in range(9)] for _ in range(9)]
# 9x9x2 陣列，第一層為棋盤，第二層紀錄陣營

current_player = -1   # 初回合的玩家




def initialization(): # 遊戲初始化
    chess = (["R", "N", "B", "Q", "K", "B", "N", "R"], "P") # 棋子擺放順序
    x_axis = " ABCDEFGH" # x軸的對應字母

    for row in range(9):
        for column in range(9):
            if row == 8:  # x 坐標軸
                checkerboard[row][column][0] = x_axis[column]
                checkerboard[row][column][1] = 0  # 座標無陣營
            
            elif column == 0:  # y 坐標軸
                checkerboard[row][column][0] = 8 - row
                checkerboard[row][column][1] = 0  # 座標無陣營
            
            elif column > 0:
                if row == 0:
                    checkerboard[row][column][0] = chess[0][column - 1]
                    checkerboard[row][column][1] = 1

                elif row == 1:
                    checkerboard[row][column][0] = chess[1]
                    checkerboard[row][column][1] = 1

                elif row == 6:
                    checkerboard[row][column][0] = chess[1]
                    checkerboard[row][column][1] = -1

                elif row == 7:
                    checkerboard[row][column][0] = chess[0][column - 1]
                    checkerboard[row][column][1] = -1

                else:
                    checkerboard[row][column][0] = " "
                    checkerboard[row][column][1] = 0
    return 0
        

          

def refresh_display():
    def get_current_player():
        if current_player == -1: 
            return "G"
        else: 
            return "R"
        
    print("\033[H\033[J", end=f"Chess, Current Player：{get_current_player()}\n\n")  # 清除之前的畫面

    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]
            if camp == 1:   # 陣營為紅方
                print(f"\033[41m {piece}", end=" \033[0m")  # 红色背景

            elif camp == -1:# 陣營為綠方
                print(f"\033[42m {piece}", end=" \033[0m")  # 綠色背景

            else:           # 無陣營 (空)
                if column%2 == row%2 and column > 0 and row < 8:
                    print(f"\033[40m {piece}", end=" \033[0m") # 黑色背景
                elif column > 0 and row < 8:
                    print(f"\033[47m {piece}", end=" \033[0m") # 白色背景
                else:
                    print(f" {piece}", end=" ") # 白色背景
        print()
    return 0




def rules(x1,y1,x2,y2):
    global current_player

    def cover():
        if x1-x2 > 0:   dirx = -1
        elif x1-x2 < 0: dirx = 1
        else:           dirx = 0

        if y1-y2 > 0:   diry = -1
        elif y1-y2 < 0: diry = 1
        else:           diry = 0

        movepoint_x = x1
        movepoint_y = y1
        while movepoint_x != x2 or movepoint_y != y2:
            movepoint_x += dirx
            movepoint_y += diry
            if checkerboard[movepoint_y][movepoint_x][1] == 0:
                pass
            else:
                return "違反規則"
        return 0
        

    
    # 轉換格式 E.g. A1 -> (1,7)
    table = {
        "A" : 1,"B" : 2,"C" : 3,"D" : 4,
        "E" : 5,"F" : 6,"G" : 7,"H" : 8,
    }
    x1 = table.get(x1) # E.g. C -> 3
    x2 = table.get(x2)

    try:
        y1 = 8 - int(y1)
        y2 = 8 - int(y2)
    except:
        return "輸入格式錯誤，請重試"

    # 確認是否違反規則
    if y1 == 8 or y1 < 0 and y2 == 8 or y2 < 0 and x1 == None or x2 == None:
        return "輸入範圍錯誤，請重試"
    
    elif checkerboard[y1][x1][1] != current_player: # 陣營偵測
        return "非己方，請重試"
    
    elif checkerboard[y2][x2][1] == current_player: # 友軍碰撞偵測
        return "不能吃己方的棋，請重試"
    
    else:
        # 棋子種類規則
        if checkerboard[y1][x1][0] == "P":  # 兵
            if cover() != 0:
                return "E"
            
            if current_player == 1: # 紅方
                dy = y2-y1
            else:                   # 綠方
                dy = y1-y2

            if checkerboard[y2][x2][1] == -current_player: # 要移動的位置有敵軍
                if (x1+1 == x2 or x1-1 == x2) and dy == 1:
                    pass
                else:
                    return "違反規則，請重試"
                
            elif y1 == 1 or y1 == 6:  # 可前進兩格
                if x1 == x2 and dy <= 2 and dy > 0:
                    pass
                else:
                    return "違反規則，請重試"
                
            else:
                if x1 == x2 and dy == 1:
                    pass
                else:
                    return "違反規則，請重試"


        elif checkerboard[y1][x1][0] == "R":  # 城堡
            if cover() != 0:
                return "E"
            
            if x1 == x2 or y1 == y2:
                pass
            else: 
                return "違反規則，請重試"


        elif checkerboard[y1][x1][0] == "N":  # 騎士
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
                pass
            else:
                return "違反規則，請重試"


        elif checkerboard[y1][x1][0] == "B":  # 主教
            if cover() != 0:
                return "E"
            
            if abs(x1 - x2) == abs(y1 - y2):
                pass
            else:
                return "違反規則，請重試"


        elif checkerboard[y1][x1][0] == "Q":  # 后
            if cover() != 0:
                return "E"
            
            if (abs(x1 - x2) == abs(y1 - y2)) or (x1 == x2) or (y1 == y2):
                pass
            else:
                return "違反規則，請重試"


        elif checkerboard[y1][x1][0] == "K":  # 王
            if abs(x1 - x2) == 1 or abs(y1 - y2) == 1:
                pass
            else:
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
        return_val = rules(select[0],select[1],moveto[0],moveto[1])
        if  return_val == 0: # 若回傳為0，代表成功
            refresh_display()
        else:
            refresh_display()
            print(return_val)
        
    else:
        refresh_display()
        print("輸入錯誤，請重試")