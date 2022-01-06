import pysnooper

@pysnooper.snoop()
def longestCommonPrefix(strs):
    ans = ''
    for i in zip(*strs):
        print(i)
        if len(set(i)) == 1:
            ans += i[0]
        else
            break
    return ans
 
if __name__ == 'main':
    longestCommonPrefix(["flower","flow","flight"])
