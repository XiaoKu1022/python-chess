x1 = 1
y1 = 1

x2 = 4
y2 = 4




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
        print(movepoint_x,movepoint_y)

    return 0

cover()