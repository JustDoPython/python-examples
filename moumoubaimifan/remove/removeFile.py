import os
import zlib
import glob

def scanning_floder(glob_path):
    crc32Dict = {}
    for fname in glob.glob(glob_path, recursive=True):
        if os.path.isfile(fname):
            crc = crc32(fname)
            if crc in crc32Dict:
                print('已经存在文件：' + crc32Dict.get(crc))
                print('重复文件：' + fname)
                print('删除文件：' + fname)
                os.remove(fname)
                print('')
            else:
                crc32Dict[crc] = fname

def crc32(file_path):
    with open(file_path, 'rb') as f:
        hash = 0
        while True:
            s = f.read(1024)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

scanning_floder(r"C:\Users\xxxx\Documents\WeChat Files\xxx\FileStorage\**\*")    
