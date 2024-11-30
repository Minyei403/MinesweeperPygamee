s ={}
alist = ["Hello",2,3,"babo", 4,"babo",5,5,5,"babo","babo","babo",2]
for word in alist:
    if word in s:
        s[word] += 1
    else:
        s[word] = 1
sorted_s = sorted(s.values())
print(s)
print(sorted_s)
print(sorted_s[-1:-4:-1])
