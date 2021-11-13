import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def gcd(pair):
    '''
    求解最大公约数
    '''
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i
    
    assert False, "Not reachable"

# 待求解的数据
NUMBERS = [
    (1963309, 2265973), (5948475, 2734765),
    (1876435, 4765849), (7654637, 3458496),
    (1823712, 1924928), (2387454, 5873948),
    (1239876, 2987473), (3487248, 2098437),
    (1963309, 2265973), (5948475, 2734765),
    (1876435, 4765849), (7654637, 3458496),
    (1823712, 1924928), (2387454, 5873948),
    (1239876, 2987473), (3487248, 2098437),
    (3498747, 4563758), (1298737, 2129874)
]

if __name__ == '__main__':
    ## 顺序求解
    start = time.time()
    results = list(map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'顺序执行时间: {delta:.3f} 秒')

    ## 多线程求解
    start = time.time()
    pool1 = ThreadPoolExecutor(max_workers=4)
    results = list(pool1.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'并发执行时间: {delta:.3f} 秒')
    
    ## 并行求解
    start = time.time()
    pool2 = ProcessPoolExecutor(max_workers=4)
    results = list(pool2.map(gcd, NUMBERS))
    end = time.time()
    delta = end - start
    print(f'并行执行时间: {delta:.3f} 秒')
