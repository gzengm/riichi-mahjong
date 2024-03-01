def mpsz(t):
	mpsz = ''
	flag = ''

	for i in t:
		if i in range(9):
			if flag != '' and flag != 'm':
				mpsz += flag
			flag = 'm'
			mpsz += str(i + 1)
		elif i in range(9, 18):
			if flag != '' and flag != 'p':
				mpsz += flag
			flag = 'p'
			mpsz += str(i - 9 + 1)
		elif i in range(18, 27):
			if flag != '' and flag != 's':
				mpsz += flag
			flag = 's'
			mpsz += str(i - 18 + 1)
		elif i in range(27, 34):
			if flag != '' and flag != 'z':
				mpsz += flag
			flag = 'z'
			mpsz += str(i - 27 + 1)

	mpsz += flag
	return mpsz

def main():
	hai = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]
	print("all tehai pattern:")
	count = 0
	tehai = hai.copy()
	for i in hai:
		tehai.append(i)
		tehai.sort()
		print(mpsz(tehai))
		count += 1
		tehai = hai.copy()
	print("total:", count)

if __name__ == '__main__':
	main()
