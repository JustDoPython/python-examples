import random
import pyxel


# Python 3.6.9+
#
# Win:
# pip install -U pyxel
# ************************
# Mac
# 1、brew install python3 sdl2 sdl2_image
# 2、restart the terminal
# 3、pip3 install -U pyxel
# ************************
# 「S」键开启游戏
# https://github.com/kitao/pyxel/blob/master/README.cn.md

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 if x % 2 == 1 and y % 2 == 1 else 1 for x in range(width)] for y in range(height)]
        self.map[1][0] = 0  # 入口
        self.map[height - 2][width - 1] = 0  # 出口
        self.visited = []
        # right up left down
        self.dx = [1, 0, -1, 0]
        self.dy = [0, -1, 0, 1]

    def set_value(self, point, value):
        self.map[point[1]][point[0]] = value

    def get_value(self, point):
        return self.map[point[1]][point[0]]

    # 获取坐标（x,y） 的邻居 返回数据结构为：二维数组
    def get_neighbor(self, x, y, value):
        res = []
        for i in range(4):
            if 0 < x + self.dx[i] < self.width - 1 and 0 < y + self.dy[i] < self.height - 1 and \
                    self.get_value([x + self.dx[i], y + self.dy[i]]) == value:
                res.append([x + self.dx[i], y + self.dy[i]])
        return res

    # 获取坐标（x,y） 的邻墙
    def get_neighbor_wall(self, point):
        return self.get_neighbor(point[0], point[1], 1)

    # 获取坐标（x,y） 的邻路
    def get_neighbor_road(self, point):
        return self.get_neighbor(point[0], point[1], 0)

    def deal_with_not_visited(self, point, wall_position, wall_list):
        if not [point[0], point[1]] in self.visited:
            self.set_value(wall_position, 0)
            self.visited.append(point)
            wall_list += self.get_neighbor_wall(point)

    # generate maze
    # https://en.wikipedia.org/wiki/Maze_generation_algorithm
    #
    # 1、迷宫行和列必须为奇数。
    # 2、奇数行和奇数列的交叉点为路，其余点为墙。迷宫四周全是墙。
    # 3、选定一个为路的单元格（本例选 [1,1]），然后把它的邻墙放入列表 wall。
    # 4、当列表 wall 里还有墙时：
    #     4.1、从列表里随机选一面墙，如果这面墙分隔的两个单元格只有一个单元格被访问过
    #         3.1.1、那就从列表里移除这面墙，同时把墙打通
    #         3.1.2、将单元格标记为已访问
    #         3.1.3、将未访问的单元格的的邻墙加入列表 wall
    #     4.2、如果这面墙两面的单元格都已经被访问过，那就从列表里移除这面墙
    def generate(self):
        start = [1, 1]
        self.visited.append(start)
        wall_list = self.get_neighbor_wall(start)
        while wall_list:
            wall_position = random.choice(wall_list)
            neighbor_road = self.get_neighbor_road(wall_position)
            wall_list.remove(wall_position)
            self.deal_with_not_visited(neighbor_road[0], wall_position, wall_list)
            self.deal_with_not_visited(neighbor_road[1], wall_position, wall_list)

    def is_out_of_index(self, x, y):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    # dfs
    def dfs(self, x, y, path, visited=[]):
        # 越界
        if self.is_out_of_index(x, y):
            return False

        # 访问过 or 撞墙
        if [x, y] in visited or self.get_value([x, y]) == 1:
            return False

        visited.append([x, y])
        path.append([x, y])

        # over
        if x == self.width - 2 and y == self.height - 2:
            return True

        # recursive
        for i in range(4):
            if 0 < x + self.dx[i] < self.width - 1 and 0 < y + self.dy[i] < self.height - 1 and \
                    self.get_value([x + self.dx[i], y + self.dy[i]]) == 0:
                if self.dfs(x + self.dx[i], y + self.dy[i], path, visited):
                    return True
                elif not self.is_out_of_index(x, y) and path[-1] != [x, y]:
                    path.append([x, y])

    # dfs
    def dfs_route(self):
        path = []
        self.dfs(1, 1, path)

        ans = [[0, 1]]
        for i in range(len(path)):
            ans.append(path[i])
            if 0 < i < len(path) - 1 and path[i - 1] == path[i + 1]:
                ans.append(path[i])
        ans.append([width - 1, height - 2])
        return ans

    # bfs
    def bfs_route(self):
        start = {'x': 0, 'y': 1, 'prev': None}
        now = start
        q = [start]
        visited = [[start['x'], start['y']]]
        # 1、从起点出发，获取起点周围所有连通的路
        # 2、如果该路没有走过，则加入队列 Q，否则跳过 同时记录其前驱节点
        while q:
            now = q.pop(0)
            # 结束
            if now['x'] == self.width - 2 and now['y'] == self.height - 2:
                break
            roads = my_maze.get_neighbor_road([now['x'], now['y']])
            for road in roads:
                if not road in visited:
                    visited.append(road)
                    q.append({'x': road[0], 'y': road[1], 'prev': now})

        ans = []
        while now:
            ans.insert(0, [now['x'], now['y']])
            now = now['prev']
        ans.append([width - 1, height - 2])
        return ans


pixel = 5
width, height = 37, 21
road_color, wall_color = 7, 13
start_point_color, end_point_color, = 11, 11
head_color, route_color, backtrack_color = 9, 11, 8

my_maze = Maze(width, height)
my_maze.generate()


class App:
    def __init__(self):
        #pyxel.init(width * pixel, height * pixel, caption='maze', border_width=10, border_color=0xFFFFFF)
        pyxel.init(width * pixel, height * pixel)
        self.death = True
        self.index = 0
        self.route = []
        self.step = 1  # 步长，数值越小速度越快，1：每次一格； 10：每次 1/10 格
        self.color = start_point_color
        self.bfs_route = my_maze.bfs_route()
        self.dfs_route = my_maze.dfs_route()
        self.dfs_model = True
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_S):
            self.death = False

        if not self.death:
            self.check_death()
            self.update_route()

    def draw(self):
        # draw maze
        for x in range(height):
            for y in range(width):
                color = road_color if my_maze.map[x][y] is 0 else wall_color
                pyxel.rect(y * pixel, x * pixel, pixel, pixel, color)
        pyxel.rect(0, pixel, pixel, pixel, start_point_color)
        pyxel.rect((width - 1) * pixel, (height - 2) * pixel, pixel, pixel, end_point_color)

        if self.index > 0:
            # draw route
            offset = pixel / 2
            for i in range(len(self.route) - 1):
                curr = self.route[i]
                next = self.route[i + 1]
                self.color = backtrack_color if curr in self.route[:i] and next in self.route[:i] else route_color
                pyxel.line(curr[0] + offset, (curr[1] + offset), next[0] + offset, next[1] + offset, self.color)
            pyxel.circ(self.route[-1][0] + 2, self.route[-1][1] + 2, 1, head_color)

    def check_death(self):
        if self.dfs_model and len(self.route) == len(self.dfs_route) - 1:
            self.death = True
        elif not self.dfs_model and len(self.route) == len(self.bfs_route) - 1:
            self.death = True

    def update_route(self):
        index = int(self.index / self.step)
        self.index += 1
        if index == len(self.route):  # move
            if self.dfs_model:
                self.route.append([pixel * self.dfs_route[index][0], pixel * self.dfs_route[index][1]])
            else:
                self.route.append([pixel * self.bfs_route[index][0], pixel * self.bfs_route[index][1]])


App()
