import random

class MazeGen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 if x % 2 == 1 and y % 2 == 1 else 1 for x in range(width)] for y in range(height)]
        # random.choice([0, height -1]), random.randint(1, width - 2)
        # random.randint(1, height -2), random.choice(0, width - 1)
        # random.choice([0, 3])
        # self.map[1][0] = 0  # 入口
        self.entrance = (random.choice([0, height -1]), random.randint(1, width - 2))
        self.exit = (random.randint(1, height -2), random.choice([0, width - 1]))
        self.map[self.entrance[0]][self.entrance[1]] = 0
        self.map[self.exit[0]][self.exit[1]] = 0
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
        # self.map[self.entrance[0]][self.entrance[1]] = 1
        # while True:
        #     x = random.randint(1, self.height-2)
        #     y = random.randint(1, self.width-2)
        #     if self.map[x][y] == 0:
        #         self.map[x][y] = 2
        #         break

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
        ans.append([self.width - 1, self.height - 2])
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
            roads = self.get_neighbor_road([now['x'], now['y']])
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

# width, height = 37, 21
# my_maze = Maze(width, height)
# my_maze.generate()
# print(my_maze.map)