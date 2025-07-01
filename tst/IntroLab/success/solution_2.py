# options: --shift 2

s = input()
ans = ''
for i in s:
    ans += chr(97 + (ord(i) + 2 - 97) % 26)
print(ans)
