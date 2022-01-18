import time
from turtle import *

from maze import MazeGen

# ENTER = 2
# EXIT = 5
PART_OF_PATH = 0
OBSTACLE = 1
TRIED = 3
DEAD_END = 4

class Maze:
    def __init__(self, mazedata, enter, exit) -> None:
        rowsInMaze = len(mazedata)
        columnsInMaze = len(mazedata[0])
        self.enter = enter
        self.exit = exit
        self.startRow = enter[0]
        self.startCol = enter[1]
        self.mazelist = mazedata
        
        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = Turtle(shape='turtle')
        setup(width=800, height=650)
        setworldcoordinates(-(columnsInMaze-1)/2 - 0.5, -(rowsInMaze-1)/2 - 0.5, 
                            (columnsInMaze-1)/2 + 0.5, (rowsInMaze-1)/2 + 0.5)
        pass

    def drawMaze(self):
        tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x + self.xTranslate, -y + self.yTranslate, 'tan')
        
        self.t.color('black', 'blue')
        self.updatePosition(self.startRow, self.startCol)
        tracer(1)
    
    def drawCenteredBox(self, x, y, color):
        self.t.up()
        self.t.goto(x - 0.5,    y - 0.5)
        self.t.color('black', color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()
        update()
        
    
    def moveTurtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate, -y+self.yTranslate))
        self.t.goto(x+self.xTranslate, -y+self.yTranslate)

    def dropBreadcrumb(self, color):
        self.t.dot(color)
    
    def updatePosition(self, row, col, val=None):
        if val:
            self.mazelist[row][col] = val
        self.moveTurtle(col, row)

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)
    
    def isExit(self, row, col):
        return (row, col) == self.exit
        # return (row == 0 or row == self.rowsInMaze-1 or 
        #         col == 0 or col == self.columnsInMaze-1)

    def __getitem__(self, idx):
        try:
            return self.mazelist[idx]
        except:
            return [int(i) for i in '1'*self.columnsInMaze]
        
def find(maze, startRow, startColumn, searchType):
    if searchType == 'es' or searchType == 'e':
        return east(maze, startRow, startColumn, searchType) or south(maze, startRow, startColumn, searchType) or \
               west(maze, startRow, startColumn, searchType) or north(maze, startRow, startColumn, searchType)
    elif searchType == 'en':
        return east(maze, startRow, startColumn, searchType) or north(maze, startRow, startColumn, searchType) or \
               west(maze, startRow, startColumn, searchType) or south(maze, startRow, startColumn, searchType)
    elif searchType == 'wn' or searchType == 'w':
        return west(maze, startRow, startColumn, searchType) or north(maze, startRow, startColumn, searchType) or \
               east(maze, startRow, startColumn, searchType) or south(maze, startRow, startColumn, searchType)
    elif searchType == 'ws':
        return west(maze, startRow, startColumn, searchType) or south(maze, startRow, startColumn, searchType) or \
               east(maze, startRow, startColumn, searchType) or north(maze, startRow, startColumn, searchType)
    elif searchType == 'n':
        return north(maze, startRow, startColumn, searchType) or east(maze, startRow, startColumn, searchType) or \
               west(maze, startRow, startColumn, searchType) or south(maze, startRow, startColumn, searchType)
    elif searchType == 's':
        return south(maze, startRow, startColumn, searchType) or east(maze, startRow, startColumn, searchType) or \
               west(maze, startRow, startColumn, searchType) or north(maze, startRow, startColumn, searchType)
    pass

def east(maze, startRow, startColumn, searchType):
    return search(maze, startRow, startColumn+1, searchType)

def south(maze, startRow, startColumn, searchType):
    return search(maze, startRow+1, startColumn, searchType)

def west(maze, startRow, startColumn, searchType):
    return search(maze, startRow, startColumn-1, searchType)

def north(maze, startRow, startColumn, searchType):
    return search(maze, startRow-1, startColumn, searchType)


def search(maze, startRow, startColumn, searchType):  # 从指定的点开始搜索
    if maze[startRow][startColumn] == OBSTACLE:
        return False
    if maze[startRow][startColumn] == TRIED:
        return False
    if maze.isExit(startRow, startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        return True

    maze.updatePosition(startRow, startColumn, TRIED)

    found = find(maze, startRow, startColumn, searchType)
    # found = search(maze, startRow, startColumn+1) or \
    #         search(maze, startRow+1, startColumn) or \
    #         search(maze, startRow-1, startColumn) or \
    #         search(maze, startRow, startColumn-1)
            
            
    if found:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    else:
        maze.updatePosition(startRow, startColumn, DEAD_END)
    
    return found


if __name__ == '__main__':
    mg = MazeGen(31, 21)
    mg.generate()
    mazedata = mg.map
    m = Maze(mg.map, mg.entrance, mg.exit)
    myWin = m.t.getscreen()
    m.drawMaze()

    # 计算最近探索方向
    searchType = 'es'
    if mg.entrance[0]<mg.exit[0] and mg.entrance[1] < mg.exit[1]:
        searchType = 'es'
    elif mg.entrance[0]<mg.exit[0] and mg.entrance[1] > mg.exit[1]:
        searchType = 'ws'
    elif mg.entrance[0]>mg.exit[0] and mg.entrance[1] > mg.exit[1]:
        searchType = 'wn'
    elif mg.entrance[0]>mg.exit[0] and mg.entrance[1] < mg.exit[1]:
        searchType = 'en'
    elif mg.entrance[0] == mg.exit[0]:
        searchType = 'n'
    elif  mg.entrance[1] == mg.exit[1]:
        searchType = 's'

    search(m, m.startRow, m.startCol, searchType)

    myWin.exitonclick()
