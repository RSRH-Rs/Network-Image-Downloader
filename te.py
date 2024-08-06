a = [1,2,2]
b = [4,6,9]

c = []

[c.append([i,x]) for i,x in zip(a,b)]

print(c)