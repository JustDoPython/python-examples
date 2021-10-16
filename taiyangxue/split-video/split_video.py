import math
import os

# 获取视频时长
import subprocess as sp
def get_video_duration(filename):

    cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i %s" % filename
    print(cmd)
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    p.wait()
    # p.stdout
    strout, strerr = p.communicate() # 去掉最后的回车
    print(strout, strerr)
    ret = strout.decode("utf-8").strip() # 去掉最后的回车
    print(ret)
    return ret


# 将视频拆分成一分钟的小段
def cut_video(filename, outfile, start, length=90):
    cmd = "ffmpeg -i %s -ss %d -t %d -c copy %s" % (filename, start, length, outfile)
    p = sp.Popen(cmd, shell=True)
    p.wait()
    return

# 计算分段
def split_video(filename, outdir, length=90, overwrite=True):

    duration = math.floor(float(get_video_duration(filename)))
    part = math.floor(duration / length)

    basenames = os.path.basename(filename).split('.')

    mainname = basenames[0]
    extname = basenames[1]
    start = 0
    partindex = 1
    for i in range(0, part):
        outname = os.path.join(outdir, ''.join([mainname, "_", str(partindex), ".", extname]))
        if os.path.exists(outname):
            if overwrite:
                os.remove(outname)
            else:
                print("文件已生成，跳过")
                continue

        cut_video(filename, outname, start, length)
        start += length
        partindex += 1
        pass
    return partindex


# 获取文件
def main(dir):
    outdir = os.path.join(dir, "output")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for fname in os.listdir(dir):
        fname = os.path.join(dir, os.path.join(dir, fname))
        if os.path.isfile(fname):
            split_video(fname, outdir)
            
if __name__ == '__main__':
    main(r"D:\Project\marketing\videos")


