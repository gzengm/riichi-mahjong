import copy
import itertools

# example:
# parameter: hai = [0, 1, 2, 12, 12, 12, 22, 23, 24, 29, 29, 32, 32, 32]
# output: "123m444p567s33666z"
def tompsz(hai):
	mpsz = ''
	f = 'x'
	for i in hai:
		if i in range(9):
			f = 'm'
			mpsz += str(i+1)
		elif i in range(9, 18):
			if f != 'x' and f != 'p':
				mpsz += f
			f = 'p'
			mpsz += str(i - 9 + 1)
		elif i in range(18, 27):
			if f != 'x' and f != 's':
				mpsz += f
			f = 's'
			mpsz += str(i - 18 + 1)
		elif i in range(27, 34):
			if f != 'x' and f != 'z':
				mpsz += f
			f = 'z'
			mpsz += str(i - 27 + 1)
	mpsz += f
	return mpsz

# example:
# parameters: n = 4, r = 2 (0 <= n <= 4, 0 <= r <= n)
# return: ret = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
# special cases:
# parameters: n = 0 and r != 0, return: ret = []
# parameters: r = 0, return: ret = [[]]
def combi(n, r):
	ret = []
	a = list(itertools.combinations_with_replacement([0, 1, 2, 3][0 : n], r))
	for i in a:
		ret.append(list(i))
	return ret

# example:
# parameters: a = [[1], [2], [3]], b = [[3, 4, 5], [4, 5, 6], [5, 6, 7]]
# return: ret = [[1, 3, 4, 5], [1, 4, 5, 6], [1, 5, 6, 7], [2, 3, 4, 5], [2, 4, 5, 6], [2, 5, 6, 7], [3, 3, 4, 5], [3, 4, 5, 6], [3, 5, 6, 7]]
# special case:
# parameters: a = [] or b = [], return: ret = []
def multi(a, b):
	ret = []
	for i in a:
		for j in b:
			ret.append(i + j)
	return ret

def suuptn(n_kotsu, n_shuntsu, a):
	rs = []
	if n_kotsu >= 1:
		# search for kotsu
		for i in range(9):
			t = a[:]
			if t[i] >= 3:
				t[i] -= 3
				ts = suuptn(n_kotsu - 1, n_shuntsu, t)
				for j in range(len(ts)):
					ts[j].extend([i] * 3)
					rs.append(ts[j])
	elif n_shuntsu >= 1:
		# search for shuntsu
		for i in range(7):
			t = a[:]
			if (t[i] >= 1) and (t[i + 1] >= 1) and (t[i + 2] >= 1):
				t[i] -= 1
				t[i + 1] -= 1
				t[i + 2] -= 1
				ts = suuptn(n_kotsu, n_shuntsu - 1, t)
				for j in range(len(ts)):
					ts[j].extend([i, i + 1, i + 2])
					rs.append(ts[j])
	else:
		return [[]]
	return rs

def jiptn(n_kotsu, a):
	rs = []
	if n_kotsu >= 1:
		# search for kotsu
		for i in range(7):
			t = a[:]
			if t[i] >= 3:
				t[i] -= 3
				ts = jiptn(n_kotsu - 1, t)
				for j in range(len(ts)):
					ts[j].extend([i] * 3)
					rs.append(ts[j])
	else:
		return [[]]
	return rs

def main():
	mentsu = [0, 3, 6, 9, 12]
	janmen = [2, 5, 8, 11, 14]
	# rs[0] for suupai mentsu, rs[1] for suupai janmen, rs[2] for jihai mentsu, rs[3] for jihai janmen
	rs = [[], [], [], []]

	# suupai mentsu
	rs[0] = [[], [], [], [], []]
	for n_suu in mentsu:
		a = [4] * 9
		n_mentsu = n_suu // 3
		for n_kotsu in range(n_mentsu + 1):
			n_shuntsu = n_mentsu - n_kotsu
			rs[0][n_mentsu].extend(suuptn(n_kotsu, n_shuntsu, a))

	# suupai jantou mentsu
	rs[1] = [[], [], [], [], []]
	for n_suu in janmen:
		a = [4] * 9
		# search for jantou
		for jan in range(9):
			t = a[:]
			t[jan] = t[jan] - 2
			n_mentsu = (n_suu - 2) // 3
			for n_kotsu in range(n_mentsu + 1):
				n_shuntsu = n_mentsu - n_kotsu
				suu_ptn = suuptn(n_kotsu, n_shuntsu, t)
				for k in suu_ptn:
					k.extend([jan] * 2)
				rs[1][n_mentsu].extend(suu_ptn)

	# jihai mentsu
	rs[2] = [[], [], [], [], []]
	for n_ji in mentsu:
		a = [4] * 9
		n_mentsu = n_ji // 3
		rs[2][n_mentsu].extend(jiptn(n_mentsu, a))

	# jihai jantou mentsu
	rs[3] = [[], [], [], [], []]
	for n_ji in janmen:
		a = [4] * 9
		# search for jantou
		for jan in range(7):
			t = a[:]
			t[jan] = t[jan] - 2
			n_mentsu = (n_ji - 2) // 3
			ji_ptn = jiptn(n_mentsu, t)
			for k in ji_ptn:
				k.extend([jan] * 2)
			rs[3][n_mentsu].extend(ji_ptn)

	# sort rs and delete repeated pattern
	for i in range(4):
		for j in range(5):
			if len(rs[i][j]) >= 2:
				for k in rs[i][j]:
					k.sort()
				rs[i][j].sort()
				k = 0
				while (k < len(rs[i][j]) - 1):
					if rs[i][j][k] == rs[i][j][k + 1]:
						rs[i][j].pop(k + 1)
					else:
						k += 1

	# # print rs
	# for i in range(4):
	# 	if (i == 0):
	# 		print("suupai mentsu:")
	# 	elif (i == 1):
	# 		print("suupai jantou mentsu:")
	# 	elif (i == 2):
	# 		print("jihai mentsu:")
	# 	elif (i == 3):
	# 		print("jihai jantou mentsu:")
	# 	for j in range(5):
	# 		print("number of mentsu:", j)
	# 		print(rs[i][j])
	# 		print("total:", len(rs[i][j]))

	# normal pattern
	# """
	# rman: manzu, rpin: pinzu, rsou: souzu
	rman = [copy.deepcopy(rs[0]), copy.deepcopy(rs[1])]
	rpin = [copy.deepcopy(rs[0]), copy.deepcopy(rs[1])]
	rsou = [copy.deepcopy(rs[0]), copy.deepcopy(rs[1])]
	for i in range(2):
		for j in range(5):
			for k in range(len(rman[i][j])):
				for m in range(len(rman[i][j][k])):
					rpin[i][j][k][m] += 9
					rsou[i][j][k][m] += 18

	# rji: jihai
	rji = [copy.deepcopy(rs[2]), copy.deepcopy(rs[3])]
	for i in range(2):
		for j in range(5):
			for k in range(len(rji[i][j])):
				for m in range(len(rji[i][j][k])):
					rji[i][j][k][m] += 27

	# rhai: suupai(manzu, pinzu and souzu) and jihai
	rhai = [rman, rpin, rsou, rji]
	fhai = [True, True, True, True]
	i = 0
	for flag in fhai:
		if not flag:
			rhai.remove(rhai[i])
		else:
			i += 1
			if i > 3:
				break
	lr = len(rhai)

	# # print rhai
	# f = 0
	# for i in range(len(rhai)):
	# 	while not fhai[f]:
	# 		f += 1
	# 	print(['manzu:', 'pinzu:', 'souzu:', 'jihai:'][f])
	# 	f += 1
	# 	for j in range(2):
	# 		if j == 0:
	# 			print("mentsu:")
	# 		elif j == 1:
	# 			print("jantou mentsu:")
	# 		for k in range(5):
	# 			print("number of mentsu:", k)
	# 			print(rhai[i][j][k])
	# 			print("total:", len(rhai[i][j][k]))

	# find and print all tehai pattern
	print("all tehai pattern:")
	# rhai[0~3][1][a] + rhai[0~3][0][b] + rhai[0~3][0][c] + rhai[0~3][0][d] + rhai[0~3][0][e],
	# a, b, c, d, e is the number of mentsu, a + b + c + d + e = 4,
	# a, b, c, d, e >= 0, b, c, d, e as a whole has no repetion
	abcde = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 0], [2, 1, 1, 0, 0], [3, 1, 0, 0, 0], [4, 0, 0, 0, 0]]
	bicidiei = [combi(lr, 4)] + [multi(combi(lr, 3), [[0]])] + [multi(combi(lr, 2), [[0, 0]])] + [multi(combi(lr, 1), [[0, 0, 0]])] + [[[0, 0, 0, 0]]]
	tpn = {}
	hai = []
	nhai = [0] * 34
	for i in range(len(abcde)):
		[a, b, c, d, e] = abcde[i]
		for ai in range(lr):
			for [bi, ci, di, ei] in bicidiei[i]:
				for j in rhai[ai][1][a]:
					for k in rhai[bi][0][b]:
						for m in rhai[ci][0][c]:
							for n in rhai[di][0][d]:
								for p in rhai[ei][0][e]:
									for h in (j + k + m + n + p):
										hai.append(h)
										nhai[h] += 1
									ok = True
									for num in nhai:
										if num > 4:
											ok = False
											break
									if ok:
										hai.sort()
										haistr = tompsz(hai)
										key = hash(haistr)
										if not tpn.__contains__(key):
											tpn[key] = None
											print(haistr)
									hai = []
									nhai = [0] * 34
	print("total:", len(tpn))
	# """

	# toitsu pattern
	"""
	# find toitsu pattern in normal pattern
	# toitsu[0] for suupai pattern and toitsu[1] for jihai pattern
	toitsu = [[], []]
	# toitsu[0~1][0~14] = [], 0 ~ 14 is maisuu(number of hai)
	toitsu[0] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
	toitsu[1] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
	# reflection from i, j to maisuu(number of hai)
	mai = [mentsu[:], janmen[:], mentsu[:], janmen[:]]
	for i in range(4):
		for j in range(5):
			for tehai in rs[i][j]:
				nhai = [0] * 34
				for hai in tehai:
					nhai[hai] += 1
				istoitsu = True
				for num in nhai:
					if num != 0 and num != 2:
						istoitsu = False
						break
				if istoitsu:
					toitsu[i // 2][mai[i][j]].append(tehai)

	# # print toitsu
	# for i in range(2):
	# 	if i == 0:
	# 		print("suupai toitsu:")
	# 	elif i == 1:
	# 		print("jihai toitsu:")
	# 	for j in range(15):
	# 		print("maisuu(number of hai):", j)
	# 		print(toitsu[i][j])
	# 		print("total:", len(toitsu[i][j]))

	# toiman: manzu, toipin: pinzu, toisou: souzu, toiji: jihai
	toiman = copy.deepcopy(toitsu[0])
	toipin = copy.deepcopy(toitsu[0])
	toisou = copy.deepcopy(toitsu[0])
	toiji = copy.deepcopy(toitsu[1])
	for i in range(15):
		for j in range(len(toiman[i])):
			for k in range(len(toiman[i][j])):
				toipin[i][j][k] += 9
				toisou[i][j][k] += 18
	for i in range(15):
		for j in range(len(toiji[i])):
			for k in range(len(toiji[i][j])):
				toiji[i][j][k] += 27

	# toihai: suupai(manzu, pinzu, souzu) and jihai
	toisuu = [toiman, toipin, toisou]
	fhai = [True, True, True, True]
	fsuu = fhai[:3]
	fji = fhai[3]
	i = 0
	for flag in fsuu:
		if not flag:
			toisuu.remove(toisuu[i])
		else:
			i += 1
			if i > 2:
				break
	toihai = toisuu[:]
	if fji:
		toihai.append(toiji)
	ls = len(toisuu)
	lt = len(toihai)

	# # print toihai
	# f = 0
	# for i in range(len(toihai)):
	# 	while not fhai[f]:
	# 		f += 1
	# 	print(['manzu:', 'pinzu:', 'souzu:', 'jihai:'][f])
	# 	f += 1
	# 	for j in range(15):
	# 		print("maisuu(number of hai):", j)
	# 		print(toihai[i][j])
	# 		print("total:", len(toihai[i][j]))

	# find and print all toitsu tehai pattern
	print("all toitsu tehai pattern:")
	# suupai: 0, 2, 6, 8, 12, 14, jihai: 0, 2
	# a + b + c + d + e + f + g = 14, a, b, c, d, e, f, g are in [0, 2, 6, 8, 12, 14]
	# combinations of a, b, c, d, e, f, g must result in 4 mentsu and only 1 jantou
	abc = [[6, 6, 2], [8, 6, 0], [12, 2, 0], [14, 0, 0]]
	aibici = [multi(combi(ls, 2), combi(lt, 1)), multi(multi(combi(ls, 1), combi(ls, 1)), [[0]]), multi(multi(combi(ls, 1), combi(lt, 1)), [[0]]), multi(combi(ls, 1), [[0, 0]])]
	tpn = {}
	tehai = []
	nhai = [0] * 34
	for i in range(len(abc)):
		[a, b, c] = abc[i]
		for [ai, bi, ci] in aibici[i]:
			for j in toihai[ai][a]:
				for k in toihai[bi][b]:
					for m in toihai[ci][c]:
						for hai in j + k + m:
							tehai.append(hai)
							nhai[hai] += 1
						ok = True
						for num in nhai:
							# if num > 4
							if num >= 4:
								ok = False
								break
						if ok:
							tehai.sort()
							haistr = tompsz(tehai)
							key = hash(haistr)
							if not tpn.__contains__(key):
								tpn[key] = None
								print(haistr)
						tehai = []
						nhai = [0] * 34
	print("total:", len(tpn))
	"""

if __name__ == '__main__':
	main()
