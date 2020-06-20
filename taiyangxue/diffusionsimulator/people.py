import numpy as np
import matplotlib.pyplot as plt


class People(object):
    def __init__(self, count=1000, first_infected_count=3):
        self.count = count
        self.first_infected_count = first_infected_count
        self.init()

    def init(self):
        self._people = np.random.normal(250, 100, (self.count, 2))  # 产生中值为1，幅度为正负100的，count组样本，每个样本有两个值 作为位置
        self.reset()

    def reset(self):
        self._round = 0  # 表示哪一次循环
        self._status = np.array([0] * self.count)
        self._timer = np.array([0] * self.count)
        self.random_people_state(self.first_infected_count, 1)

    def random_people_state(self, num, state=1):
        """随机挑选人设置状态
        """
        assert self.count > num
        # TODO：极端情况下会出现无限循环
        n = 0
        while n < num:
            i = np.random.randint(0, self.count)
            if self._status[i] == state:
                continue
            else:
                self.set_state(i, state)
                n += 1

    def set_state(self, i, state):
        self._status[i] = state
        # 记录状态改变的时间
        self._timer[i] = self._round  # 哪次循环中状态发生在哪次循环中

    def move(self, width=1, x=.0):
        movement = np.random.normal(0, width, (self.count, 2))

        normal = np.random.normal(0, 1, self.count)
        switch = np.where(normal < x, 1, 0)
        movement[switch == 0] = 0  # 随机产生不移动的情况
        self._people = self._people + movement # 位置发生变换

    def change_state(self):  # 设置成为确证
        dt = self._round - self._timer
        # 必须先更新时钟再更新状态
        d = np.random.randint(3, 7)
        # print("change_state:", (self._status == 1) & ((dt == d) | (dt > 14)))
        self._timer[(self._status == 1) & ((dt == d) | (dt > 14))] = self._round
        self._status[(self._status == 1) & ((dt == d) | (dt > 14))] += 1

    def affect(self, safe_distance=5):
        """感染最接近的健康人"""
        # np.vstack((self._people[self._status == 1],self._people[self._status == 2]))
        for inf in self._people[(self._status == 1) | (self._status == 2)]: # self.infected:
            dm = (self._people - inf) ** 2
            d = dm.sum(axis=1) ** 0.5  # 计算一个欧氏距离  (x1,y1) (x2,y2)  ==> ((x1-x2)^2 + (y1-y2)^2)^(1/2)
            sorted_index = d.argsort()
            for i in sorted_index:
                if d[i] >= safe_distance:
                    break  # 超出范围，不用管了
                if self._status[i] > 0: # 已经感染的排除掉
                    continue
                self._status[i] = 1
                # 记录状态改变的时间
                self._timer[i] = self._round
                break  # 只传 1 个

    def update(self):
        """每一次迭代更新"""
        self.change_state()
        self.affect()
        self.move(3, 1.99)
        self._round += 1