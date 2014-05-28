arr = []

for i in range(10):
	arr.append(i)
print arr

for i in range(20):
	arr.append(i)
	if len(arr)>10:
		arr.pop(0)
	print arr

print "finally:"
print arr

