import time
import taichi as ti

ti.init()

@ti.func
def is_prime(n):
    result = True
    for k in range(2, int(n**0.5) + 1):
        if n % k == 0:
            result = False
            break
    return result

@ti.kernel
def count_primes(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime(k):
            count += 1
    
    return count

t0 = time.time()
print(count_primes(1000000))
t1 = time.time()

print(t1-t0)
