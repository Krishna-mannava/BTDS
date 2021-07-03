"""n=int(input())
l=list(map(int,input().split()))
largest=-9999999999
smallest=-9999999998
for i in range(n):
    if(largest<l[i]):
        largest=l[i]
for i in range(n):
    if(smallest<l[i] and smallest!=largest):
        smallest=l[i]
print(largest,smallest)      """
def printlarge(arr, arr_size):
    if (arr_size < 2):
        print("none")
        return
    largest = second = -2454635434;
    for i in range(0, arr_size):
        largest = max(largest, arr[i]);
    print(largest,end=" ")
    for i in range(0, arr_size):
        if (arr[i] != largest):
            second = max(second, arr[i]);
    if (second == -2454635434):
        print("no");
    else:
        print(second)
n=int(input())
l=list(map(int,input().split()))
printlarge(l,n)