from graphics import *
import time

def createGraph(lines):
    vertices = dict()
    for line in lines:
        words = line.split(',')
        if len(words) != 3:
            break
        if int(words[0]) == 0 and int(words[1]) == 0 and int(words[2]) == 0:
            break
        vertex = vertices.get(words[0])
        if vertex == None:
            vertices[words[0]] = [(words[1], 100 - int(words[2]))]
        else:
            vertices[words[0]].append((words[1], 100 - int(words[2])))
        
        vertex = vertices.get(words[1])
        if vertex == None:
            vertices[words[1]] = [(words[0], 100 - int(words[2]))]
        else:
            vertices[words[1]].append((words[0], 100 - int(words[2])))
    return vertices


def main():
    win = GraphWin('Dummy Player', 500, 500)

    win.setCoords(0.0, 0.0, 10.0, 10.0)
    win.setBackground("white")

    # draw grid
    for x in range(10):
        for y in range(10):
            win.plotPixel(x*50, y*50, "black")

    file = open('dummyGameBoard.out')
    lines = file.read().split('\n')
    file.close()
    for line in lines:
        words = line.split(',')
        if len(words) != 3:
            break
        else:
            square = Rectangle(Point(int(words[0]), int(words[1])), Point(int(words[0]) + 1, int(words[1]) + 1))
            square.draw(win)
            if words[2] == '#':
                square.setFill("red")
            elif words[2] == '%':            
                square.setFill("dark green")
            elif words[2] == '@':
                square.setFill("blue")
            elif words[2] == '*':
                square.setFill("cyan")
            elif words[2] == 'o':
                square.setFill("purple")

    time.sleep(5)
    file = open('dummyPlayerBoard.out')
    lines = file.read().split('\n')
    file.close()
    for line in lines:
        words = line.split(',')
        if len(words) != 2:
            break
        else:
            square = Rectangle(Point(int(words[0]) + 1, int(words[1]) + 1), Point(int(words[0]), int(words[1])))
            square.draw(win)
            square.setFill("black")
            time.sleep(1)


    win.getMouse()
    win.close()

main()