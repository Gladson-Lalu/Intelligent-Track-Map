import time

import cv2
import numpy as np
import threading
import sys

from DataClass.FrontFace import FrontFace
from DataClass.Link import Link
from DataClass.Point import Point

np.set_printoptions(threshold=sys.maxsize)

image = "maze.png"
blockSize = 15
frontFace = FrontFace.Up

rw = blockSize // 2
p = 0
start = Point()
end = Point()
dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]


def getBlock(y, x):
    global blockSize
    return y - y % blockSize, x - x % blockSize


def bfs(s, e):
    global img, h, w, blockSize, frontFace
    found = False
    q = []
    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    q.append(s)
    v[s.y][s.x] = 1
    img2 = np.zeros((h, w, 3), np.uint8)
    nodes = []
    while q:
        element = q.pop(0)
        for d in dir4:
            cell = element + d
            if (0 <= cell.x < w and 0 <= cell.y < h and v[cell.y][cell.x] == 0 and
                    True != (img[cell.y][cell.x][0] == 255 and img[cell.y][cell.x][1] == 255 and img[cell.y][cell.x][
                        2] == 255)):
                img2[cell.y][cell.x] = [255, 255, 255]
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

        img2 = cv2.Canny(img2, 30, 255)
        cv2.imshow("image5", img2)
        element = e
        while element != s:
            path.append((getBlock(element.y, element.x), element))
            block, element = parent[element.y][element.x]
        path.append((block, element))
        path.reverse()
        realPath = []
        vis = []
        prev = Link()
        for block, element in path:
            img[element.y][element.x] = [0, 255, 255]
            img3[element.y][element.x] = [0, 0, 0]
            l = False
            r = False
            u = False
            d = False
            diff = blockSize
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
            print("front Face = " + str(frontFace), end=" , ")
            img[currentBlock.coordinate[0]][currentBlock.coordinate[1]] = [0, 0, 255]
            if currentBlock.coordinate[1] == realPath[i].coordinate[1]:
                if currentBlock.coordinate[0] > realPath[i].coordinate[0]:
                    print("North")
                    if realPath[i].left:
                        leftCount += 1
                    if realPath[i].right:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        print("forward")
                    elif frontFace == FrontFace.Right:
                        print(str(leftCount) + "left")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        print(str(rightCount) + "right")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        print("rotate")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Up
                elif currentBlock.coordinate[0] < realPath[i].coordinate[0]:
                    print("South")
                    if realPath[i].right:
                        leftCount += 1
                    if realPath[i].left:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        print("rotate")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        print(str(rightCount) + "right")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        print(str(leftCount) + "left")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        print("forward")
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Down
                else:
                    print("error")
            elif currentBlock.coordinate[0] == realPath[i].coordinate[0]:
                if currentBlock.coordinate[1] > realPath[i].coordinate[1]:
                    print("West")
                    if realPath[i].down:
                        leftCount += 1
                    if realPath[i].up:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        print(str(leftCount) + "left")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        print("rotate")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Left:
                        print("forward")
                    elif frontFace == FrontFace.Down:
                        print(str(rightCount) + "right")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Left
                elif currentBlock.coordinate[1] < realPath[i].coordinate[1]:
                    print("East")
                    if realPath[i].up:
                        leftCount += 1
                    if realPath[i].down:
                        rightCount += 1
                    if frontFace == FrontFace.Up:
                        print(str(rightCount) + "right")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Right:
                        print("forward")
                    elif frontFace == FrontFace.Left:
                        print("rotate")
                        leftCount = rightCount = 0
                    elif frontFace == FrontFace.Down:
                        print(str(leftCount) + "left")
                        leftCount = rightCount = 0
                    else:
                        print("set the frontFace")
                    frontFace = FrontFace.Right
                else:
                    print("error")
            currentBlock = realPath[i]

        print("Path Found")
        cv2.imshow("Path", img3)
        time.sleep(.0001)
    else:
        print("Path Not Found")


def mouse_event(event, pX, pY, flags, params):
    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 0, 255), -1)
            start = Point(pX, pY)
            print("start = ", start.y, start.x)
            p += 1
        elif p == 1:
            cv2.rectangle(img, (pX - rw, pY - rw),
                          (pX + rw, pY + rw), (0, 200, 50), -1)
            end = Point(pX, pY)
            print("end = ", end.y, end.x)
            p += 1


def display():
    global img
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouse_event)
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)


img = cv2.imread(image)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
h, w = img.shape[:2]

print("Select start and end points : ")

t = threading.Thread(target=display, args=())
t.daemon = True
t.start()

while p < 2:
    pass

bfs(start, end)

cv2.waitKey(0)
