x=input()
if(x.rsplit('.')[1].lower() in ['png','jpg','jpeg']):
    print("yes")
else:
    print("n")
print(x.rsplit('.')[1].lower())
print(x)