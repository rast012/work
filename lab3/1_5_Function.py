def permute(s, chosen=""):
    if not s:
        print(chosen)
    else:
        for i in range(len(s)):
            permute(s[:i] + s[i+1:], chosen + s[i])
string = input()
permute(string)
