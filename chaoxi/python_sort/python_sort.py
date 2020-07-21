# 冒泡排序
def bubble_s(data):
    length = len(data)
    # 第二层循环：循环一次，表示相邻两个元素进行了一次比较
    for i in range(length):
        for j in range(1, length - i):
            if data[j - 1] > data[j]:
                # 相邻元素进行替换
                data[j], data[j - 1] = data[j - 1], data[j]
    print(data)

# 选择排序
def select_s(data):
    # 第一层循环：取出数组中的所有元素
    for i in range(len(data)):
        temp = i   # 取出第一个元素用来比较
        # 第二层循环：从第i后面的一个值开始循环，与data[i]进行比较
        for j in range(i+1,len(data)):
            if data[j] < data[temp]:
                data[temp], data[j] = data[j], data[temp]
    print(data)



# 插入排序
# 将第一个元素作为有序区的元素，从无序区取出一个元素与有序区元素进行逐个比较，并加入到有序区，依次循环

def insert_s(data):
    # 第一层循环： 从第二个元素开始循环取出元素，取出的元素再与有序区元素进行比较
    for i in range(1,len(data)):
        temp = data[i]
        j = i-1
        while j>=0 and temp < data[j]:
            data[j+1] = data[j]
            j = j-1    # 在与前面一个元素进行比较，所以j 需要减1
        # 当j = -1 就跳出循环，将temp值赋给第一个值，即data[0]
        data[j+1] = temp
    print(data)



# 快速排序
def partition(data, left, right):
    temp = data[left]
    while left < right:
        # 如果最右边的值大于中间值，则最右边值往后退一个位置，反之，就将值赋值给最左边位置
        while left < right and data[right] >= temp:
            right = right - 1
        data[left] = data[right]
        # 如果最左边的值小于中间值，则最左边值往前进一个位置，反之，就将值赋值给最右边位置
        while left < right and data[left] <= temp:
            left = left + 1
        data[right] = data[left]
    # 循环结束，即可定位到中间位置，将初始值，赋值到这个位置
    data[left] = temp
    return left


def quick_sort(data, left, right):
    if left < right:
        mid = partition(data, left, right)
        quick_sort(data, left, mid)
        quick_sort(data, mid + 1, right)




# 计数排序
def count_sort(data):
    count = [0 for _ in range(len(data)+1)]
    for i in data:
        count[i] += 1
    data.clear()
    for index, nums in enumerate(count):
        for j in range(nums):
            data.append(index)