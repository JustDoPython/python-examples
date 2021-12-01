#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

from tqdm import tqdm
from time import sleep
from tqdm import trange

for char in tqdm(['h', 'e', 'l', 'l', 'o']):
    sleep(0.25)

for i in tqdm(range(100)):
    sleep(0.05)

for i in trange(100):
    sleep(0.05)

pbar = tqdm(range(5))
for char in pbar:
    pbar.set_description("Progress %d" %char)
    sleep(1)


with tqdm(total=100) as pbar:
    for i in range(1, 5):
        sleep(1)
        # 更新进度
        pbar.update(10*i)

with tqdm(total=100, colour='yellow') as pbar:
    for i in range(1, 5):
        sleep(1)
        # 更新进度
        pbar.update(10*i)


for i in trange(3, desc='outer loop'):
    for i in trange(100, desc='inner loop', leave=False):
        sleep(0.01)














