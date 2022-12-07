import random
from math import sin, cos, pi, log
from tkinter import *
 
 # 画布的宽
CANVAS_WIDTH = 840 
# 画布的高 
CANVAS_HEIGHT = 680 
# 画布中心的X轴坐标 
CANVAS_CENTER_X = CANVAS_WIDTH / 2  
# 画布中心的Y轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  
# 放大比例
IMAGE_ENLARGE = 11  
 
HEART_COLOR = "#EEAEEE"  
 
"""
    爱心函数生成器
    -shrink_ratio: 放大比例
    -t: 参数
"""
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    # 基础函数
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(3 * t))
 
    # 放大
    x*=IMAGE_ENLARGE
    y*=IMAGE_ENLARGE
    # 移到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
 
    return int(x), int(y)
 
"""
    随机内部扩散
    -x: 原x
    -y: 原y
    -beta: 强度
""" 
def scatter_inside(x, y, beta=0.15):
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
 
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
 
    return x - dx, y - dy
 
 
"""
    抖动
    -x: 原x
    -y: 原y
    -ratio: 比例
""" 
def shrink(x, y, ratio):
   
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy
 
 
"""
    自定义曲线函数，调整跳动周期
    -p: 参数
"""
def curve(p):
    # 可以尝试换其他的动态函数，达到更有力量的效果（贝塞尔？）
    return 2 * (2 * sin(4 * p)) / (2 * pi)
 

# 爱心类
class Heart:
    def __init__(self, generate_frame=20):
        # 原始爱心坐标集合
        self._points = set()  
        # 边缘扩散效果点坐标集合
        self._edge_diffusion_points = set()  
        # 中心扩散效果点坐标集合
        self._center_diffusion_points = set()  
        # 每帧动态点坐标
        self.all_points = {}  
        self.build(2000)
 
        self.random_halo = 1000
 
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)
 
    def build(self, number):
        # 爱心
        for _ in range(number):
            # 随机不到的地方造成爱心有缺口
            t = random.uniform(0, 2 * pi)  
            x, y = heart_function(t)
            self._points.add((x, y))
 
        # 爱心内扩散
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
 
        # 爱心内再次扩散
        point_list = list(self._points)
        for _ in range(10000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.27)
            self._center_diffusion_points.add((x, y))
 
    @staticmethod
    def calc_position(x, y, ratio):
        # 调整缩放比例
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.420)  # 魔法参数
 
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
 
        return x - dx, y - dy
 
    def calc(self, generate_frame):
         # 圆滑的周期的缩放比例
        ratio = 15 * curve(generate_frame / 10 * pi) 
 
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
 
        all_points = []
 
        # 光环
        heart_halo_point = set()  
        # 光环的点坐标集合
        for _ in range(halo_number):
            # 随机不到的地方造成爱心有缺口
            t = random.uniform(0, 2 * pi)  
            # 魔法参数
            x, y = heart_function(t, shrink_ratio=-15)  
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # 处理新的点
                heart_halo_point.add((x, y))
                x += random.randint(-60, 60)
                y += random.randint(-60, 60)
                size = random.choice((1, 1, 2))
                all_points.append((x, y, size))
                all_points.append((x+20, y+20, size))
                all_points.append((x-20, y -20, size))
                all_points.append((x+20, y - 20, size))
                all_points.append((x - 20, y +20, size))
 
        # 轮廓
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
 
        # 内容
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
 
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
 
        self.all_points[generate_frame] = all_points
 
    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)
 
 
def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(1, draw, main, render_canvas, render_heart, render_frame + 1)
 
 
if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)

    text2 = Label(root, text="爱你",font = ("Helvetica", 18), fg = "#c12bec" ,bg = "black") #
    text2.place(x=395, y=350)

    root.mainloop()