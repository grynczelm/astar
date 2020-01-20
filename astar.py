#!/usr/bin/python
import sys
import time
import os


animate = False

openList = []
closedList = []

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Field():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.f = 0 # odległość od startu + heurystyka
        self.g = 0 # odległość od startu
        self.h = 0 # heurystyka


def calculatePath(maze, startPoint, endPoint):
    startField = Field(None, startPoint)
    
    openList.append(startField)

    while len(openList) > 0:
        currentField = smallestF(openList)
        openList.remove(currentField)
        closedList.append(currentField)

        if (currentField.position.x == endPoint.x) and (currentField.position.y == endPoint.y):
            positions = []
            tracedPath = tracePath([currentField], currentField)
            for element in tracedPath:
                positions.append((element.position.x, element.position.y))
            
            return positions[::-1]
        
        neighbours = [
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
            Position(1, 1),
            Position(-1, -1),
            Position(-1, 1),
            Position(1, -1)
        ] # można zakomentować cztery ostatnie, aby algorytm chodził tylko w kierunkach NSWE
        # North, South, West, East - północ, południe, zachód, wschód

        children = []

        for neighbour in neighbours:
            nextX = currentField.position.x + neighbour.x
            nextY = currentField.position.y + neighbour.y
            
            if nextX >= 0 and nextY >= 0 and nextY < len(maze) and nextX < len(maze[0]):
                if maze[nextY][nextX] == 0:
                    childPosition = Position(nextX, nextY)
                    children.append(Field(currentField, childPosition))
        
        closedPositions = []

        for closed in closedList:
            closedPositions.append(closed.position)
        
        if animate:
            os.system('clear')
            printMaze(maze, startPoint, endPoint, closedPositions)
            time.sleep(0.25)
        
        for child in children:
            already = False
            
            for closed in closedPositions:
                if closed.x == child.position.x and closed.y == child.position.y:
                    already = True
            
            if already:
                continue

            child.g = currentField.g + 1
            child.h = calculateHeuristic(child, endPoint)
            child.f = child.g + child.h

            for element in openList:
                if child == element and child.g > element.g:
                    already = True
            
            if not already:
                openList.append(child)
    
    return []


def calculateHeuristic(child, endPoint):
    heuristicValue = ((child.position.x - endPoint.x)**2) + ((child.position.y - endPoint.y)**2)
    return heuristicValue


def tracePath(path, field):
    if field.parent != None:
        path.append(field.parent)
        return tracePath(path, field.parent)
    else:
        return path


def smallestF(fieldList):
    smallest = None
    for el in fieldList:
        if smallest == None:
            smallest = el
        else:
            if smallest.f > el.f:
                smallest = el
    
    return smallest


def stdwrite(element, foreground="white", background="black"):
    if foreground == "red":
        foreground = "0;31"
    elif foreground == "green":
        foreground = "0;32"
    else:
        foreground = "1;37"
    
    foreground = "\033[" + foreground + "m"

    if background == "green":
        background = "42"
    elif background == "light_gray":
        background = "47"
    elif background == "yellow":
        background = "43"
    elif background == "red":
        background = "41"
    else:
        background = "40"
    
    background = "\033[" + background + "m"
    
    element = foreground+background+element
    sys.stdout.flush()
    sys.stdout.write("\033[1;37m\033[40m " + element + "\033[1;37m\033[40m")


def printMaze(maze, startpoint, endpoint, highlighted=[]):
    c = -1
    r = -1

    print("\n\033[1;37m\033[40m\t\033[1;37m\033[42m0\033[1;37m\033[40m - element startowy")
    print("\t\033[1;37m\033[41m0\033[1;37m\033[40m - element końcowy\n")

    for row in maze:
        r = r+1
        c = -1
        
        sys.stdout.write("\t")

        for column in row:
            c = c+1

            isStartPoint = (c == startpoint.x and r == startpoint.y)
            isEndPoint = (c == endpoint.x and r == endpoint.y)

            color = "black"

            for element in highlighted:
                if element.x == c and element.y == r:
                    color = "yellow"

            if isStartPoint:
                color = "green"
            if isEndPoint:
                color = "red"

            if column == 0:
                stdwrite("O", "white", color)
            else:
                if isStartPoint or isEndPoint:
                    print("\n\n\tNieprawidłowe współrzędne "+("startowe" if isStartPoint else "docelowe"))
                    exit()
                
                stdwrite("X", "green", color)
        
        print("")


def main():
    print("")

    maze = [[1,1,0,0,0,1,1,0,1,1,0,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0,0,1,1],
            [1,0,1,1,1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,0,1,0,0,1,1,0,1,0,1,1],
            [1,1,1,1,1,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,0,1,1,1,0,0,1,0],
            [1,1,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,1,0,0,1,1,0,0,0,1,0,0,1,1],
            [1,1,0,1,1,1,0,1,0,1,1,0,1,1,0,0,1,1,1,1,1,1,1,0,1,0,0,0,1,1],
            [1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0,1,1],
            [0,0,1,0,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,1,0,1,1],
            [0,0,0,1,0,0,0,1,1,1,0,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
            [0,1,1,0,0,1,1,0,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,0,1,0,1,1,0],
            [0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,1,0,1,0,0,1,1,1,0,0,0,1,0],
            [0,0,1,0,0,1,0,1,1,0,1,0,1,0,0,1,1,1,1,0,1,1,0,0,0,1,0,0,1,1],
            [1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,1,1,1],
            [1,1,0,1,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,0,1,0,1,0,1,1,0],
            [0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,1],
            [1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,1,0,1,0,0],
            [0,1,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,1,1,1,1,0,1,1,0,0,0],
            [1,1,0,1,1,0,1,1,0,0,0,1,0,1,0,1,0,1,0,1,1,1,0,0,0,0,1,1,1,0],
            [1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0],
            [1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,1,0,0,1,1,0,0,0,1,1,1],
            [0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,0,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0],
            [1,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0],
            [1,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,1,1,0,1,1,0,0,1,1,1,1,1,0],
            [1,0,0,1,1,0,0,0,0,1,1,0,1,0,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,0],
            [1,0,0,0,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0,1,0],
            [1,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,0,1,0,1],
            [0,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,1,1,1,0,0,1,1],
            [1,1,1,0,0,0,1,1,1,1,1,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0]]
    
    start = Position(17, 0)
    end = Position(3, 29)

    sys.stdout.write("\033[1;37m\033[40m\tTak wygląda labirynt bez wyznaczonej trasy:\n")
    printMaze(maze, start, end)

    calculatedPath = calculatePath(maze, start, end)
    converted = []

    for element in calculatedPath:
        converted.append(Position(element[0], element[1]))
    
    if animate:
        os.system('clear')
    
    print("\n\tGraficzne przedstawienie wyniku działania algorytmu:")
    printMaze(maze, start, end, converted)

    print("\n\tOto wyliczona trasa dla podanych danych:")
    print("\t" + str(calculatedPath))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--animate":
            animate = True
        else:
            print("Nieznany argument '" + str(sys.argv[1]) + "'. Czy miałeś na myśli '--animate'?")
            exit()
    
    main()
