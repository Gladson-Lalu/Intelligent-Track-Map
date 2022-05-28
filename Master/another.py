


x = path[0].x
        y = path[0].y
        v = []
        focal = 5
        step = 5
        print((e.x, e.y))
while True:
    print(v)

    if objectCheck(img3, x, y - step, focal) and (x, y) not in v:
        v.append((x, y))
        y = y - step
        img[y][x] = [255, 0, 0]
    elif objectCheck(img3, x - step, y, focal) and (x, y) not in v:
        v.append((x, y))
        x = x - step

        img[y][x] = [255, 0, 0]
    elif objectCheck(img3, x + step, y, focal) and (x, y) not in v:
        v.append((x, y))
        x = x + step
        img[y][x] = [255, 0, 0]
    elif objectCheck(img3, x, y + step, focal) and (x, y) not in v:
        v.append((x, y))
        y = y + step
        img[y][x] = [255, 0, 0]

    print((x, y));