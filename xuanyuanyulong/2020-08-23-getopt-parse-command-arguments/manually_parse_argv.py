import sys


for index, command_arg in enumerate(sys.argv[1:]):
    if command_arg.startswith('--'):
        try:
            value = sys.argv[1:][index+1]
            if not value.startswith('-'):
                print("%s 为长参数，参数值为 %s" % (command_arg, value))
                continue
        except IndexError:
            pass
        
        print("%s 为长参数，无参数值" % command_arg)

    elif command_arg.startswith('-'):
        try:
            value = sys.argv[1:][index+1]
            if not value.startswith('-'):
                print("%s 为短参数，参数值为 %s" % (command_arg, value))
                continue
        except IndexError:
            pass
        
        print("%s 为短参数，无参数值" % command_arg)


