s = input()
ans = ''
for i in s:
    ans += chr(97 + (ord(i) + 1 - 97) % 26)
print(ans)