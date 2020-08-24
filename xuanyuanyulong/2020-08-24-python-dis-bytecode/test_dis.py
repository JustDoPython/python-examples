import dis


s = """
def add(add_1, add_2):
    sum_value = add_1 + add_2

print("Hello World!")

import sys
"""

dis.dis(s)