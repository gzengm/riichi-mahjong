def tompsz(tehai):
	mpsz = ''
	f = ''
	for i in tehai:
		if 0 <= i and i < 9:
			if f != '' and f != 'm':
				mpsz += f
			f = 'm'
			mpsz += str(i + 1)
		elif 9 <= i and i < 18:
			if f != '' and f != 'p':
				mpsz += f
			f = 'p'
			mpsz += str(i - 9 + 1)
		elif 18 <= i and i < 27:
			if f != '' and f != 's':
				mpsz += f
			f = 's'
			mpsz += str(i - 18 + 1)
		elif 27 <= i and i < 34:
			if f != '' and f != 'z':
				mpsz += f
			f = 'z'
			mpsz += str(i - 27 + 1)
	mpsz += f
	return mpsz

def main():
	manzu = list(range(9))
	pinzu = [i + 9 for i in range(9)]
	souzu = [i + 18 for i in range(9)]
	jihai = [i + 27 for i in range(7)]
	hai = [manzu, pinzu, souzu, jihai]
	fhai = [True, True, True, True]
	i = 0
	for flag in fhai:
		if not flag:
			hai.remove(hai[i])
		else:
			i += 1
			if i > 3:
				break
	for i in range(len(hai)):
		hai += hai[0]
		hai.pop(0)

	print("all tehai pattern:")
	count = 0
	tehai = []
	for i in range(len(hai)):
		for j in range(i + 1, len(hai)):
			for k in range(j + 1, len(hai)):
				for m in range(k + 1, len(hai)):
					for n in range(m + 1, len(hai)):
						for p in range(n + 1, len(hai)):
							for q in range(p + 1, len(hai)):
								tehai += [hai[i]] * 2
								tehai += [hai[j]] * 2
								tehai += [hai[k]] * 2
								tehai += [hai[m]] * 2
								tehai += [hai[n]] * 2
								tehai += [hai[p]] * 2
								tehai += [hai[q]] * 2
								print(tompsz(tehai))
								count += 1
								tehai= []
	print("total:", count)

if __name__ == '__main__':
	main()
