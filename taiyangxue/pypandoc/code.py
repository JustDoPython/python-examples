import pypandoc

input = "**Hello World!**"
output = pypandoc.convert_text(input, 'html', format='md')

print(output)

input = """
# Pandoc

Pandoc 是个牛X的工具

## 用法

- `convert_text`
- `convert_file`
"""
output = pypandoc.convert_text(input, 'html', format='md')
print(output)

output = pypandoc.convert_text(input, 'rst', format='md')
print(output)

convert_test(input, 'epub', format='md', outputfile='test.epub')