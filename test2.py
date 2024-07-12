def check():
    king_coordinate = []
    for row in range(9):
        for column in range(9):
            piece = checkerboard[row][column][0]
            camp = checkerboard[row][column][1]
            if piece == "K":
                king_coordinate.append((row,column,camp))
                find += 1

    

                
