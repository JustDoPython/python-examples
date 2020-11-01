def sum_of_word(word):
    sum = 0
    for char in word:
        sum += ord(char) - 96  # 为什么需要减去 96
    return sum

with open('results.txt', 'w') as result:
    with open('words_alpha.txt', 'r') as file:
        for word in file.readlines():
            if sum_of_word(word.strip()) == 100:  # 注意这里的 strip
                result.write(word)