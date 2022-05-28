import time

import cv2
import numpy as np
import threading
import sys

from DataClass.FrontFace import FrontFace
from DataClass.Link import Link
from DataClass.Point import Point

np.set_printoptions(threshold=sys.maxsize)

image = "pmaze.jpg"
blockSize = 24
frontFace = FrontFace.Up

p = 0
start = Point()
end = Point()
dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]

pathCommands = []
currentCommand = None


def createPathCommands(direction):
    global pathCommands, currentCommand
    if currentCommand != direction:
        pathCommands.append(direction)
        currentCommand = direction
        print(direction)


def getBlock(y, x):
    global blockSize
    return y - y % blockSize, x - x % blockSize


def draw_grid(img, color=(0, 10, 0), thickness=1):
    h, w, _ = img.shape

    # draw vertical lines
    for x in np.linspace(start=blockSize, stop=w - blockSize, num=w//blockSize - 1):
        x = int(round(x))
        cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=blockSize, stop=h - blockSize, num=h//blockSize - 1):
        y = int(round(y))
        cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img


def bfs(s, e):
    global img, h, w, blockSize, frontFace
    found = False
    q = []
    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    q.append(s)
    v[s.y][s.x] = 1
    nodes = []
    while q:
        element = q.pop(0)
        for d in dir4:
            cell = element + d
            if (0 <= cell.x < w and 0 <= cell.y < h and v[cell.y][cell.x] == 0 and
                    True != (img[cell.y][cell.x][0] == 255 and img[cell.y][cell.x][1] == 255 and img[cell.y][cell.x][
                        2] == 255)):
                block = getBlock(cell.y, cell.x)
                if block not in nodes:
                    nodes.append(getBlock(cell.y, cell.x))
                v[cell.y][cell.x] = v[element.y][element.x] + 1
                q.append(cell)
                parent[cell.y][cell.x] = (block, element)

                if cell == e:
                    found = True
                    q = []
                    break

    path = []
    img3 = 255 * np.ones((h, w, 3), np.uint8)
    if found:
        element = e
        while element != s:
            path.append((getBlock(element.y, element.x), element))
            block, element = parent[element.y][element.x]
        path.append((block, element))
        path.reverse()
        realPath = []
        vis = []
        prev = Link()
        diff = blockSize * 4
        for block, element in path:
            img[element.y][element.x] = [0, 255, 255]
            img3[element.y][element.x] = [0, 0, 0]
            l = False
            r = False
            u = False
            d = False

            coordinates = getBlock(element.y + diff, element.x)
            if coordinates in nodes and not prev.down:
                d = True
            coordinates = getBlock(element.y - diff, element.x)
            if coordinates in nodes and not prev.up:
                u = True
            coordinates = getBlock(element.y, element.x + diff)
            if coordinates in nodes and not prev.right:
                r = True
            coordinates = getBlock(element.y, element.x - diff)
            if coordinates in nodes and not prev.left:
                l = True
            prev = link = Link(block, u, l, r, d)
            if block not in vis:
                vis.append(block)
                print(block, u, l, r, d)
                realPath.append(link)
        currentBlock = realPath[0]
        leftCount = 0
        rightCount = 0

        for i in range(1, len(realPath)):
            img[currentBlock.coordinate[0]][currentBlock.coordinate[1]] = [0, 0, 255]
            if currentBlock.coordinate[1] == realPath[i].coordinate[1]:
                if currentBlock.coordinate[0] > realPath[i].coordinate[0]:
                    # North
                    if realPath[i].left:
                        leftCount += 1
                    if realPath[i].right:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        createPathCommands("f")
                    elif frontFace == FrontFace.Right:
                        createPathCommands(str(leftCount) + "l")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        createPathCommands(str(rightCount) + "r")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        createPathCommands("u")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Up
                elif currentBlock.coordinate[0] < realPath[i].coordinate[0]:
                    # South
                    if realPath[i].right:
                        leftCount += 1
                    if realPath[i].left:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        createPathCommands("u")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        createPathCommands(str(rightCount) + "r")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        createPathCommands(str(leftCount) + "l")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        createPathCommands("f")
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Down
                else:
                    print("error")
            elif currentBlock.coordinate[0] == realPath[i].coordinate[0]:
                if currentBlock.coordinate[1] > realPath[i].coordinate[1]:
                    # West
                    if realPath[i].down:
                        leftCount += 1
                    if realPath[i].up:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        createPathCommands(str(leftCount) + "l")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        createPathCommands("u")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        createPathCommands("f")
                    elif frontFace == FrontFace.Down:
                        createPathCommands(str(rightCount) + "r")
                        print(str(rightCount) + "right")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Left
                elif currentBlock.coordinate[1] < realPath[i].coordinate[1]:
                    # East
                    if realPath[i].up:
                        leftCount += 1
                    if realPath[i].down:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        createPathCommands(str(rightCount) + "r")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        createPathCommands("f")
                    elif frontFace == FrontFace.Left:
                        createPathCommands("u")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        createPathCommands(str(leftCount) + "l")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Right
                else:
                    print("error")
            currentBlock = realPath[i]
        print(str(pathCommands))

        print("Path Found")
        cv2.imshow("Path", img3)
        time.sleep(.0001)
    else:
        print("Path Not Found")


def mouse_event(event, pX, pY, flags, params):
    global img, start, end, p
    yo, x0 = getBlock(pY, pX)
    y1, x1 = getBlock(pY + blockSize, pX + blockSize)
    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (x0, yo), (x1, y1), (0, 0, 255), -1)
            start = Point(pX, pY)
            print("start = ", start.y, start.x)
            p += 1
        elif p == 1:
            cv2.rectangle(img, (x0, yo), (x1, y1), (0, 200, 50), -1)
            end = Point(pX, pY)
            print("end = ", end.y, end.x)
            p += 1


def display():
    global img ,img2
    cv2.imshow("Image", img)
    cv2.imshow("grid", img2)
    cv2.setMouseCallback('Image', mouse_event)
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)


img = cv2.imread(image)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img2 = img.copy()
h, w = img.shape[:2]
draw_grid(img2)
print("Select start and end points : ")

t = threading.Thread(target=display, args=())
t.daemon = True
t.start()

while p < 2:
    pass

bfs(start, end)

cv2.waitKey(0)
