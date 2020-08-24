import sys
import getopt


opts, args = getopt.getopt(sys.argv[1:], 'd:t:', ["author=", "country=", "auto"])

print(opts)
print(args)