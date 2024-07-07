# 创建 9x9x2 的三维数组，初始化为 0
checkerboard = [[[0 for _ in range(2)] for _ in range(9)] for _ in range(9)]
x = "　ＡＢＣＤＥＦＧＨ"
y = "　１２３４５６７８"
chess = (["堡", "馬", "主", "后", "王", "主", "馬", "堡"], "兵")


def initialization():
    for row in range(9):
        for column in range(9):
            if column == 0:  # y 坐标轴
                checkerboard[row][column][0] = y[8 - row]
                checkerboard[row][column][1] = 0  # 坐标不属于任何阵营

            elif row == 8:  # x 坐标轴
                checkerboard[row][column][0] = x[column]
                checkerboard[row][column][1] = 0  # 坐标不属于任何阵营

            elif (row == 0 or row == 7) and column > 0:
                checkerboard[row][column][0] = chess[0][column - 1]
                checkerboard[row][column][1] = 1 if row == 0 else 2  # 阵营 1 或 2

            elif (row == 1 or row == 6) and column > 0:
                checkerboard[row][column][0] = chess[1]
                checkerboard[row][column][1] = 1 if row == 1 else 2  # 阵营 1 或 2

            else:
                checkerboard[row][column][0] = "　"
                checkerboard[row][column][1] = 0  # 空格子


def refresh_display():
    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]
            if camp == 1:
                print(f"\033[41m{piece}\033[0m", end=" ")  # 红色背景

            elif camp == 2:
                print(f"\033[42m{piece}\033[0m", end=" ")  # 绿色背景

            else:
                print(piece, end=" ")
        print()


def move(x1,y1,x2,y2):
    checkerboard[y2][x2][0] = checkerboard[y1][x1][0]
    checkerboard[y2][x2][1] = checkerboard[y1][x1][1]
    checkerboard[y1][x1][0] = "　"
    checkerboard[y1][x1][1] = 0


initialization()
refresh_display()



move(1,1,1,6)
move(1,6,1,2)
refresh_display()

while True:
    select = input("Select > ")
    moveto = input("MoveTo > ")