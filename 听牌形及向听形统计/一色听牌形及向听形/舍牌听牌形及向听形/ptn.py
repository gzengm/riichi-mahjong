import itertools
import json

def tompsz(hai):
	mpsz = ''
	f = ''
	for i in hai:
		if i in range(9):
			if f != '' and f != 'm':
				mpsz += f
			f = 'm'
			mpsz += str(i + 1)
		elif i in range(9, 18):
			if f != '' and f != 'p':
				mpsz += f
			f = 'p'
			mpsz += str(i - 9 + 1)
		elif i in range(18, 27):
			if f != '' and f != 's':
				mpsz += f
			f = 's'
			mpsz += str(i - 18 + 1)
		elif i in range(27, 34):
			if f != '' and f != 'z':
				mpsz += f
			f = 'z'
			mpsz += str(i - 27 + 1)
	mpsz += f
	return mpsz

def combi(a, r):
	ret = []
	t = list(itertools.combinations(a, r))
	for i in t:
		ret.append(list(i))
	return ret

def multi(a, b):
	ret = []
	for i in a:
		for j in b:
			ret.append(i + j)
	return ret

def create_set_from(ptn):
	ptnset = [[], [], [], []]
	for i in range(4):
		ptnset[i] = [[] for k in range(15)]
		for j in range(15):
			ptnset[i][j] = set()
			for k in ptn[i][j]:
				ptnset[i][j].add(hash(tompsz(k)))
	return ptnset

# a and b are in [[...], [...], ...] form
# make sure k in a and b is sorted
def removeptn(a, b):
	bset = set()
	for k in b:
		bset.add(hash(tompsz(k)))
	ret = []
	for k in a:
		if hash(tompsz(k)) not in bset:
			ret.append(k)
	return ret

def sortptn(ptn):
	for i in range(4):
		for j in range(15):
			for k in ptn[i][j]:
				if len(k) > 1:
					k.sort()
			ptn[i][j].sort()
			# delete repeated pattern
			k = 0
			while k < len(ptn[i][j]) - 1:
				if ptn[i][j][k] == ptn[i][j][k + 1]:
					ptn[i][j].pop(k + 1)
				else:
					k += 1

def printptn(ptn):
	for i in range(4):
		print(['manzu:', 'pinzu:', 'souzu:', 'jihai:'][i])
		for j in range(15):
			print("maisuu(number of hai):", j)
			for k in ptn[i][j]:
				print(tompsz(k))
			print("total:", len(ptn[i][j]))

def allptn(a, n):
	ret = []
	for i in range(n // 4 + 1):
		for j in range((n - 4 * i) // 3 + 1):
			for k in range((n - 4 * i - 3 * j) // 2 + 1):
				t = a
				for kung in combi(t, i):
					for e in kung:
						t.remove(e)
					for pong in combi(t, j):
						for e in pong:
							t.remove(e)
						for toitsu in combi(t, k):
							for e in toitsu:
								t.remove(e)
							for single in combi(t, n - 4 * i - 3 * j - 2 * k):
								hai = []
								for e in kung:
									hai.extend([e] * 4)
								for e in pong:
									hai.extend([e] * 3)
								for e in toitsu:
									hai.extend([e] * 2)
								for e in single:
									hai.extend([e])
								hai.sort()
								ret.append(hai)
							for e in toitsu:
								t.append(e)
						for e in pong:
							t.append(e)
					for e in kung:
						t.append(e)
	ret.sort()
	return ret

def agariptn(n_pong, n_chow, a):
	ret = []
	if n_pong >= 1:
		for i in a:
			t = a.copy()
			if t[i] <= 1:
				t[i] += 3
				ret.extend(multi([[i] * 3], agariptn(n_pong - 1, n_chow, t)))
	elif n_chow >= 1:
		for i in list(a.keys())[:-2]:
			t = a.copy()
			if t[i] <= 3 and t[i + 1] <= 3 and t[i + 2] <= 3:
				t[i] += 1
				t[i + 1] += 1
				t[i + 2] += 1
				ret.extend(multi([[i, i + 1, i + 2]], agariptn(n_pong, n_chow - 1, t)))
	else:
		return [[]]
	return ret

def toitsuptn(n_toitsu, a):
	ret = []
	if n_toitsu >= 1:
		for i in a:
			t = a.copy()
			if t[i] < 2:
				t[i] += 2
				ret.extend(multi([[i] * 2], toitsuptn(n_toitsu - 1, t)))
	else:
		return [[]]
	return ret

def findallptn():
	hai = [[], [], [], []]
	for i in range(4):
		hai[i] = [k + i * 9 for k in range(9 if i in range(3) else 7)]
	aptn = [[], [], [], []]
	for i in range(4):
		aptn[i] = [[] for k in range(15)]
		for j in range(15):
			aptn[i][j] = allptn(hai[i], j)
	return aptn

# tf marks whether to take toitsu agari pattern into account
def findagari(tf):
	agari = [[], [], [], []]
	for i in range(4):
		agari[i] = [[] for k in range(15)]
		a = {}
		for k in range(9 if i in range(3) else 7):
			a[k + i * 9] = 0
		for j in range(15):
			# find normal agari pattern
			n_meld = j // 3
			if j % 3 == 2:
				for k in a.keys():
					t = a.copy()
					t[k] += 2
					if i in range(3):
						for n_pong in range(n_meld + 1):
							n_chow = n_meld - n_pong
							agari[i][j].extend(multi([[k] * 2], agariptn(n_pong, n_chow, t)))
					else:
						agari[i][j].extend(multi([[k] * 2], agariptn(n_meld, 0, t)))
			elif j % 3 == 0:
				if i in range(3):
					for n_pong in range(n_meld + 1):
						n_chow = n_meld - n_pong
						agari[i][j].extend(agariptn(n_pong, n_chow, a))
				else:
					agari[i][j].extend(agariptn(n_meld, 0, a))
			# find toitsu agari pattern
			if tf and j % 2 == 0:
				n_toitsu = j // 2
				agari[i][j].extend(toitsuptn(n_toitsu, a))
	sortptn(agari)
	return agari

def findtoitsu():
	toitsu = [[], [], [], []]
	for i in range(4):
		toitsu[i] = [[] for k in range(15)]
		a = {}
		for k in range(9 if i in range(3) else 7):
			a[k + i * 9] = 0
		for j in range(15):
			if j % 2 == 0:
				n_toitsu = j // 2
				toitsu[i][j].extend(toitsuptn(n_toitsu, a))
	sortptn(toitsu)
	return toitsu

def findtenpai(agari):
	# create agariset for quick search
	agariset = create_set_from(agari)
	tenpai = [[], [], [], []]
	for i in range(4):
		tenpai[i] = [[] for k in range(15)]
		a = {}
		for k in range(9 if i in range(3) else 7):
			a[k + i * 9] = 0
		for j in range(15):
			for k in agari[i][j]:
				t = a.copy()
				for m in k:
					t[m] += 1
				uniq = set(k)
				for m in uniq:
					for n in t.keys():
						if m != n and t[n] < 4:
							rk = k.copy()
							rk.remove(m)
							rk.append(n)
							rk.sort()
							if hash(tompsz(rk)) not in agariset[i][j]:
								tenpai[i][j].append(rk)
	sortptn(tenpai)
	return tenpai

def findshanten(remain, prevten):
	# create prevtenset for quick search
	prevtenset = create_set_from(prevten)
	shanten = [[], [], [], []]
	for i in range(4):
		shanten[i] = [[] for k in range(15)]
		a = {}
		for k in range(9 if i in range(3) else 7):
			a[k + i * 9] = 0
		for j in range(15):
			for k in remain[i][j]:
				t = a.copy()
				for m in k:
					t[m] += 1
				is_shanten = False
				for m, n in itertools.product(set(k), t.keys()):
					if m != n and t[n] < 4:
						rk = k.copy()
						rk.remove(m)
						rk.append(n)
						rk.sort()
						if hash(tompsz(rk)) in prevtenset[i][j]:
							is_shanten = True
							break
				if is_shanten:
					shanten[i][j].append(k)
	sortptn(shanten)
	return shanten

def main():
	# # find all pattern
	# aptn = findallptn()
	# # printptn(aptn)
	# # print(aptn)
	with open("aptn.json") as f:
		aptn = json.load(f)

	# # find normal agari pattern
	# agari = findagari(tf = False)
	# # printptn(agari)
	# # print(agari)
	# with open("agari.json") as f:
	# 	agari = json.load(f)

	# # find normal agari pattern together with toitsu agari pattern
	# agaritoi = findagari(tf = True)
	# # printptn(agaritoi)
	# # print(agaritoi)
	with open("agaritoi.json") as f:
		agaritoi = json.load(f)
	agari = agaritoi

	# # find normal tenpai pattern
	# tenpai = findtenpai(agari)
	# # printptn(tenpai)
	# # print(tenpai)
	# with open("tenpai.json") as f:
	# 	tenpai = json.load(f)

	# normal tenpai pattern together with toitsu tenpai pattern
	with open("tenpaitoi.json") as f:
		tenpaitoi = json.load(f)
	tenpai = tenpaitoi

	# # find normal shanten1 pattern
	# remain = [[], [], [], []]
	# for i in range(4):
	# 	remain[i] = [[] for k in range(15)]
	# 	for j in range(15):
	# 		remain[i][j] = removeptn(removeptn(aptn[i][j], agari[i][j]), tenpai[i][j])
	# shanten1 = findshanten(remain, tenpai)
	# # printptn(shanten1)
	# # print([remain, shanten1])
	# with open("shanten1.json") as f:
	# 	[remain, shanten1] = json.load(f)

	# normal shanten1 pattern together with toitsu shanten1 pattern
	with open("shanten1toi.json") as f:
		[remain, shanten1toi] = json.load(f)
	shanten1 = shanten1toi

	# # find normal shanten2 pattern
	# for i in range(4):
	# 	for j in range(15):
	# 		remain[i][j] = removeptn(remain[i][j], shanten1[i][j])
	# shanten2 = findshanten(remain, shanten1)
	# # printptn(shanten2)
	# # print([remain, shanten2])
	# with open("shanten2.json") as f:
	# 	[remain, shanten2] = json.load(f)

	# normal shanten2 pattern together with toitsu shanten2 pattern
	with open("shanten2toi.json") as f:
		[remain, shanten2toi] = json.load(f)
	shanten2 = shanten2toi

	# # find normal shanten3 pattern
	# for i in range(4):
	# 	for j in range(15):
	# 		remain[i][j] = removeptn(remain[i][j], shanten2[i][j])
	# shanten3 = findshanten(remain, shanten2)
	# # printptn(shanten3)
	# # print([remain, shanten3])
	# with open("shanten3.json") as f:
	# 	[remain, shanten3] = json.load(f)

	# normal shanten3 pattern together with toitsu shanten3 pattern
	with open("shanten3toi.json") as f:
		[remain, shanten3toi] = json.load(f)
	shanten3 = shanten3toi

	# # find normal shanten4 pattern
	# for i in range(4):
	# 	for j in range(15):
	# 		remain[i][j] = removeptn(remain[i][j], shanten3[i][j])
	# shanten4 = findshanten(remain, shanten3)
	# # printptn(shanten4)
	# # print([remain, shanten4])
	# with open("shanten4.json") as f:
	# 	[remain, shanten4] = json.load(f)

	# normal shanten4 pattern together with toitsu shanten4 pattern
	with open("shanten4toi.json") as f:
		[remain, shanten4toi] = json.load(f)
	shanten4 = shanten4toi

	# # combined code to find shanten[0~3] pattern at once (would also cost combined running time)
	# # [Error]: remain = [[[] for k in range(15)]] * 4
	# # Don't use the above way to assign 'remain'. It would make remain[0], remain[1],
	# # remain[2], remain[3] to be exactly the same object in memory.
	# remain = [[[] for k in range(15)], [[] for k in range(15)], [[] for k in range(15)], [[] for k in range(15)]]
	# shanten = [[], [], [], []]
	# for s in range(4):
	# 	for i in range(4):
	# 		for j in range(15):
	# 			if s == 0:
	# 				remain[i][j] = removeptn(removeptn(aptn[i][j], agari[i][j]), tenpai[i][j])
	# 			else:
	# 				remain[i][j] = removeptn(remain[i][j], shanten[s - 1][i][j])
	# 	shanten[s] = findshanten(remain, tenpai if s == 0 else shanten[s - 1])
	# 	print('shanten', s + 1, ':', sep = '')
	# 	printptn(shanten[s])

if __name__ == '__main__':
	main()
