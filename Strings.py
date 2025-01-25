a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)
if 'Lorem' in a:
    print('1) Y')
if 'lorem' in a:
    print('2) Y')
if 'Lorem' in a[0:-1]:
    print('3) Y')
if 'Lorem' in a[2:-1]:
    print('4) Y')