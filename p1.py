f = open('text.txt','r')
word1= f.readlines()
b = str(word1[0])
word = b.split()
p=[]
for i in word :
    print(i)
    a = int(i)
    p.append(a)
p.sort()
x = len(p)
if x %2 == 1:
    print("median is ",p[x//2])
else :
    print("median is ", p[x//2-1])
