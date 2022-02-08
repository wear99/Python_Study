q=[1,2,3,4,5,6,7,8,9]
# ab * a =ccc
for a in q:
    for b in q:
        for c in q:
            if (a * 10 + b) * a == c * 100 + c * 10 + c:
                print(a, b, c)
                 