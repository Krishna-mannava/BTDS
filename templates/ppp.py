n=int(input())
l=list(map(int,input().split()))
large=max(l)
for i in range(n):
    if(l[i]==large):
        l[i]=-999999999999
        break
print(large,max(l))