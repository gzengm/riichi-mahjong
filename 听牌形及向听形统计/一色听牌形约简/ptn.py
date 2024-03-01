import itertools
import json

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

# hai is a list of numbers
def toint(hai):
	ret = 0
	for i in hai:
		ret = ret * 10 + i + 1
	return ret

# gaps over 3 would be regarded as 3
def calcgaps(s):
	ret = '' # gap is '' for single hai
	for i in range(len(s) - 1):
		x = int(s[i + 1]) - int(s[i])
		ret += str(x if x <= 2 else 3)
	return ret

def maxdev5(s):
	maxd = 0
	for c in s:
		d = abs(5-int(c))
		if d > maxd:
			maxd = d
	return maxd

def avgs(s):
	sum = 0.0
	for c in s:
		sum += int(c)
	return sum / len(s)

def revert_str(s):
	ret = ''
	for i in s:
		ret = i + ret
	return ret

def remove_str(a, b):
	for c in b:
		if c in a:
			a = a.replace(c, '', 1)
		else:
			a = None
			break
	return a

def nhai(haistr):
	ret = {}
	for c in haistr:
		if c not in ret:
			ret[c] = 1
		else:
			ret[c] += 1
	return ret

# calculate maisuu of haistr when its machihai is machistr
def c_maisuu(haistr, machistr):
	ret = 0
	for c in machistr:
		ret += (4 - haistr.count(c))
	return ret

# e is a key-value tuple (k, v) of menchan, k as an integer, v as a list of integers
# this function is used in list.sort() function as 'key' parameter
def compare_by_maisuu(e):
	k, v = e
	return c_maisuu(str(k), str(toint(v)))

def create_set_from(ptn):
	n = len(ptn)
	ptnset = [set() for k in range(n)]
	for i in range(n):
		for k in ptn[i]:
			ptnset[i].add(toint(k))
	return ptnset

def sortptn(ptn):
	for i in range(len(ptn)):
		for k in ptn[i]:
			if len(k) > 1:
				k.sort()
		ptn[i].sort()
		# delete repeated pattern
		j = 0
		while j < len(ptn[i]) - 1:
			if ptn[i][j] == ptn[i][j + 1]:
				ptn[i].pop(j + 1)
			else:
				j += 1

def fprintptn(f, ptn):
	for i in range(len(ptn)):
		print("maisuu(number of hai):", i, file = f)
		for k in ptn[i]:
			print(toint(k), file = f)
		print("total:", len(ptn[i]), file = f)

def fprintmachi(f, ptn, machi):
	for i in range(len(ptn)):
		print("maisuu(number of hai):", i, file = f)
		for k in ptn[i]:
			print(k, "\tmachi:", toint(machi[i][str(k)]), file = f)
		print("total:", len(ptn[i]), file = f)
		f.flush()

def fprintgaps(gapstxt, tenpai, tenpaigaps, machigaps):
	for i in range(15):
		print("maisuu:", i, file = gapstxt)
		for j in range(len(tenpai[i])):
			print(tenpaigaps[i][j], "\tmachi:", machigaps[i][j], file = gapstxt)
		print("total:", len(tenpai[i]), file = gapstxt)

def fprintmenchan(f, ptn, machi, sortby = None):
	menchan = [{} for k in range(9)]
	for i in range(len(ptn)):
		for k in ptn[i]:
			mchai = machi[i][str(k)]
			menchan[len(mchai) - 1][k] = mchai
	for i in range(9):
		print(i + 1, "menchan:", file = f)
		mcitems = menchan[i].items()
		if sortby != None:
			mcitems = list(mcitems)
			mcitems.sort(key = sortby)
		for k, v in mcitems:
			print(k, "\tmachi:", toint(v), "\tmaisuu:", c_maisuu(str(k), str(toint(v))), file = f)
		print("total:", len(menchan[i]), file = f)
	return menchan

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

def findallptn():
	hai = [k for k in range(9)]
	aptn = [[] for k in range(15)]
	for i in range(15):
		aptn[i] = allptn(hai, i)
	return aptn

def find_all():
	# find all pattern
	aptn = findallptn()

	# print to txt
	aptntxt = open("aptn.txt", "w")
	fprintptn(aptntxt, aptn)
	aptntxt.close()

	# write to json
	aptnjson = open("aptn.json", "w")
	print(json.dumps(aptn), file = aptnjson)
	aptnjson.close()

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

# cf marks whether to take chitoitsu agari pattern into account
def findagari(cf = False):
	agari = [[] for k in range(15)]
	a = {k : 0 for k in range(9)}
	for i in range(15):
		# find normal agari pattern
		n_meld = i // 3
		if i % 3 == 2:
			for k in a.keys():
				t = a.copy()
				t[k] += 2
				for n_pong in range(n_meld + 1):
					n_chow = n_meld - n_pong
					agari[i].extend(multi([[k] * 2], agariptn(n_pong, n_chow, t)))
		elif i % 3 == 0:
			for n_pong in range(n_meld + 1):
				n_chow = n_meld - n_pong
				agari[i].extend(agariptn(n_pong, n_chow, a))
	# find chitoitsu agari pattern
	if cf:
		agari[14].extend(toitsuptn(7, a))
	sortptn(agari)
	return agari

def find_agari():
	# find agari pattern
	agari = findagari() # not include chitoitsu agari pattern

	# print to txt
	agaritxt = open("agari.txt", "w")
	fprintptn(agaritxt, agari)
	agaritxt.close()

	# write to json
	agarijson = open("agari.json", "w")
	print(json.dumps(agari), file = agarijson)
	agarijson.close()

def find_agarichi():
	# find normal agari pattern together with chitoitsu agari pattern
	agarichi = findagari(cf = True) # include chitoitsu agari pattern

	# print to txt
	agarichitxt = open("agarichi.txt", "w")
	fprintptn(agarichitxt, agarichi)
	agarichitxt.close()

	# write to json
	agarichijson = open("agarichi.json", "w")
	print(json.dumps(agarichi), file = agarichijson)
	agarichijson.close()

def findtenpai(agari):
	tenpai = [[] for k in range(15)]
	tenpaiset = [set() for k in range(15)]
	agariset = create_set_from(agari)
	for i in range(14):
		for k in agari[i + 1]:
			for m in set(k):
				rk = k.copy()
				rk.remove(m)
				rk.sort()
				key = toint(rk)
				if key not in agariset[i] and key not in tenpaiset[i]:
					tenpai[i].append(rk)
					tenpaiset[i].add(key)
	sortptn(tenpai)
	return tenpai

def find_tenpai():
	# load normal agari pattern from json
	with open("agari.json") as f:
		agari = json.load(f)

	# find normal tenpai pattern
	tenpai = findtenpai(agari)

	# print to txt
	tenpaitxt = open("tenpai.txt", "w")
	fprintptn(tenpaitxt, tenpai)
	tenpaitxt.close()

	# write to json
	tenpaijson = open("tenpai.json", "w")
	print(json.dumps(tenpai), file = tenpaijson)
	tenpaijson.close()

def find_tenpaichi():
	# load normal agari pattern together with chitoitsu agari pattern from json
	with open("agarichi.json") as f:
		agarichi = json.load(f)

	# find normal tenpai pattern together with chitoitsu tenpai pattern
	tenpaichi = findtenpai(agarichi)

	# print to txt
	tenpaichitxt = open("tenpaichi.txt", "w")
	fprintptn(tenpaichitxt, tenpaichi)
	tenpaichitxt.close()

	# write to json
	tenpaichijson = open("tenpaichi.json", "w")
	print(json.dumps(tenpaichi), file = tenpaichijson)
	tenpaichijson.close()

def findtenpaimachi(agari):
	tenpai = [[] for k in range(15)]
	machidicts = [{} for k in range(15)]
	agariset = create_set_from(agari)
	for i in range(14):
		for k in agari[i + 1]:
			for m in set(k):
				rk = k.copy()
				rk.remove(m)
				rk.sort()
				key = toint(rk)
				if key not in agariset[i]:
					strkey = str(key)
					if strkey not in machidicts[i]:
						machidicts[i][strkey] = [m]
					else:
						machidicts[i][strkey].append(m)
		tenpai[i] = sorted([int(k) for k in machidicts[i]])
	return tenpai, machidicts

def find_tenpaimachi():
	# load normal agari pattern together with chitoitsu agari pattern from json
	with open("agarichi.json") as f:
		agarichi = json.load(f)
	agari = agarichi

	# find tenpai pattern together with their machihai
	tenpai, machi = findtenpaimachi(agari)

	# print to txt
	tenpaimachitxt = open("tenpaimachi.txt", "w")
	fprintmachi(tenpaimachitxt, tenpai, machi)
	tenpaimachitxt.close()

	# write to json
	tenpaimachijson = open("tenpaimachi.json", "w")
	print(json.dumps([tenpai, machi]), file = tenpaimachijson)
	tenpaimachijson.close()

def calc_gaps():
	# load tenpai pattern (include chitoitsu tenpai pattern) together with their machihai from json
	with open("tenpaimachi.json") as f:
		[tenpai, machi] = json.load(f)

	# start calculating gaps
	# another avaliable definition of gaps: distance between any hai and the first hai
	# such as, gaps of 2223 are 0001, gaps of 4577 are 0133
	tenpaigaps = [[] for k in range(15)]
	machigaps = [[] for k in range(15)]
	for i in range(15):
		n = len(tenpai[i])
		tenpaigaps[i] = [[] for k in range(n)]
		machigaps[i] = [[] for k in range(n)]
		for j in range(n):
			k = str(tenpai[i][j])
			tenpaigaps[i][j] = calcgaps(k)
			machigaps[i][j] = calcgaps(str(toint(machi[i][k])))

	# print gaps for checking use
	gapstxt = open("gaps.txt", "w")
	fprintgaps(gapstxt, tenpai, tenpaigaps, machigaps)
	gapstxt.close()

	# write gaps to json file for quick load
	gapsjson = open("gaps.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsjson)
	gapsjson.close()

def del_c1():
	# load tenpai pattern (include chitoitsu tenpai pattern) together with their machihai from json
	with open("tenpaimachi.json") as f:
		[tenpai, machi] = json.load(f)

	# load gaps from json
	with open("gaps.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 1
	delc1msg = open("delc1msg.txt", "w")
	for i in range(15):
		j = 0
		while j < len(tenpai[i]):
			tj = str(tenpai[i][j]) # string
			tgj = tenpaigaps[i][j] # string
			mgj = machigaps[i][j] # string
			k = j + 1
			while k < len(tenpai[i]):
				tk = str(tenpai[i][k]) # string
				tgk = tenpaigaps[i][k] # string
				mgk = machigaps[i][k] # string
				if mgj == mgk and tgj == tgk or mgj == mgk[::-1] and tgj == tgk[::-1]:
					print("Repeated in case 1:", tj, "&", tk, file = delc1msg)
					print("Length:", i, file = delc1msg)
					deltj = False
					mdtj = maxdev5(tj)
					mdtk = maxdev5(tk)
					if mdtj > mdtk:
						deltj = True
					elif mdtj == mdtk:
						lotj = int(tj[-1]) - int(tj[0])
						lotk = int(tk[-1]) - int(tk[0])
						if lotj > lotk:
							deltj = True
						elif lotj == lotk:
							abstj = abs(5-avgs(tj))
							abstk = abs(5-avgs(tk))
							if abstj > abstk:
								deltj = True
					if deltj:
						print("Delete:", tj, file = delc1msg)
						del tenpai[i][j], tenpaigaps[i][j]
						del machi[i][tj], machigaps[i][j]
						j -= 1
						break
					else:
						print("Delete:", tk, file = delc1msg)
						del tenpai[i][k], tenpaigaps[i][k]
						del machi[i][tk], machigaps[i][k]
						k -= 1
				k += 1
			j += 1
	delc1msg.close()

	# print remained items after checking case 1
	c1txt = open("tenpaimachic1.txt", "w")
	fprintmachi(c1txt, tenpai, machi)
	c1txt.close()

	# write remained items to json after checking case 1
	c1json = open("tenpaimachic1.json", "w")
	c1json.write(json.dumps([tenpai, machi]))
	c1json.close()

	# print revised gaps for checking use
	gapsc1txt = open("gapsc1.txt", "w")
	fprintgaps(gapsc1txt, tenpai, tenpaigaps, machigaps)
	gapsc1txt.close()

	# write revised gaps after checking case 1 to json for quick load
	gapsc1json = open("gapsc1.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc1json)
	gapsc1json.close()

	# print menchan
	menchantxt = open("menchanc1.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc1.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc1sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc1sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def del_c2():
	# load remained tenpaimachi after checking case 1 from json
	with open("tenpaimachic1.json") as f:
		[tenpai, machi] = json.load(f)

	# load revised gaps after checking case 1 from json
	with open("gapsc1.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 2
	delc2msg = open("delc2msg.txt", "w")
	for i in range(15):
		j = 0
		while j < len(tenpai[i]):
			tj = str(tenpai[i][j]) # string
			tgj = tenpaigaps[i][j] # string
			mj = str(toint(machi[i][tj])) # string
			mgj = machigaps[i][j] # string
			k = j + 1
			while k < len(tenpai[i]):
				tk = str(tenpai[i][k]) # string
				tgk = tenpaigaps[i][k] # string
				mk = str(toint(machi[i][tk])) # string
				mgk = machigaps[i][k] # string
				if (tgj == tgk or tgj == tgk[::-1]) and (mgj in mgk or mgk in mgj):
					print("Repeated in case 2:", tj, "&", tk, file = delc2msg)
					print("Length:", i, file = delc2msg)
					deltj = False
					lenmj = len(mj)
					lenmk = len(mk)
					if lenmj < lenmk:
						deltj = True
					elif lenmj == lenmk:
						mdtj = maxdev5(tj)
						mdtk = maxdev5(tk)
						if mdtj > mdtk:
							deltj = True
						elif mdtj == mdtk:
							lotj = int(tj[-1]) - int(tj[0])
							lotk = int(tk[-1]) - int(tk[0])
							if lotj > lotk:
								deltj = True
							elif lotj == lotk:
								abstj = abs(5-avgs(tj))
								abstk = abs(5-avgs(tk))
								if abstj > abstk:
									deltj = True
					if deltj:
						print("Delete:", tj, file = delc2msg)
						del tenpai[i][j], tenpaigaps[i][j]
						del machi[i][tj], machigaps[i][j]
						j -= 1
						break
					else:
						print("Delete:", tk, file = delc2msg)
						del tenpai[i][k], tenpaigaps[i][k]
						del machi[i][tk], machigaps[i][k]
						k -= 1
				k += 1
			j += 1
	delc2msg.close()

	# print remained tenpaimachi after checking case 2
	c2txt = open("tenpaimachic2.txt", "w")
	fprintmachi(c2txt, tenpai, machi)
	c2txt.close()
	c2json = open("tenpaimachic2.json", "w")
	c2json.write(json.dumps([tenpai, machi]))
	c2json.close()

	# print revised gaps after checking case 2
	gapsc2txt = open("gapsc2.txt", "w")
	fprintgaps(gapsc2txt, tenpai, tenpaigaps, machigaps)
	gapsc2txt.close()

	# write revised gaps to json after checking case 2
	gapsc2json = open("gapsc2.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc2json)
	gapsc2json.close()

	# print menchan
	menchantxt = open("menchanc2.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc2.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc2sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc2sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def del_c3():
	# load normal agari pattern together with chitoitsu agari pattern from json
	with open("agarichi.json") as f:
		agarichi = json.load(f)
	agari = agarichi

	# load tenpaiex and machiex from json
	with open("tenpaimachi.json") as f:
		[tenpaiex, machiex] = json.load(f)

	# load tenpai and machi after checking case 2 from json
	with open("tenpaimachic2.json") as f:
		[tenpai, machi] = json.load(f)

	# load revised gaps after checking case 2 from json
	with open("gapsc2.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 3
	delc3msg = open("delc3msg.txt", "w")
	agariset = create_set_from(agari)
	for k in range(15):
		m = 0
		while m < len(tenpai[k]):
			tk = str(tenpai[k][m]) # string
			mk = toint(machi[k][tk]) # integer
			found = False
			for i in range(k):
				for j in range(len(tenpaiex[i])):
					tj = str(tenpaiex[i][j]) # string
					mj = toint(machiex[i][tj]) # integer
					if mj == mk:
						s = remove_str(tk, tj)
						if not s or int(s) not in agariset[k-i]:
							continue
						print("Repeated in case 3:", tj, "&", tk, file = delc3msg)
						print("Length:", i, "&", k, file = delc3msg)
						print("Delete:", tk, file = delc3msg)
						del tenpai[k][m], tenpaigaps[k][m]
						del machi[k][tk], machigaps[k][m]
						found = True
						break
				if found:
					break
			if not found:
				m += 1
	delc3msg.close()

	# print remained tenpaimachi after checking case 3
	c3txt = open("tenpaimachic3.txt", "w")
	fprintmachi(c3txt, tenpai, machi)
	c3txt.close()
	c3json = open("tenpaimachic3.json", "w")
	c3json.write(json.dumps([tenpai, machi]))
	c3json.close()

	# print revised gaps after checking case 3
	gapsc3txt = open("gapsc3.txt", "w")
	fprintgaps(gapsc3txt, tenpai, tenpaigaps, machigaps)
	gapsc3txt.close()

	# write revised gaps to json after checking case 3
	gapsc3json = open("gapsc3.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc3json)
	gapsc3json.close()

	# print menchan
	menchantxt = open("menchanc3.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc3.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc3sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc3sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def del_c4():
	# load normal agari pattern together with chitoitsu agari pattern from json
	with open("agarichi.json") as f:
		agarichi = json.load(f)
	agari = agarichi

	# load original tenpaimachi from json
	with open("tenpaimachi.json") as f:
		[tenpaiex, machiex] = json.load(f)

	# load remained tenpaimachi after checking case 3 from json
	with open("tenpaimachic3.json") as f:
		[tenpai, machi] = json.load(f)

	# load revised gaps after checking case 3 from json
	with open("gapsc3.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 4
	delc4msg = open("delc4msg.txt", "w")
	agariset = create_set_from(agari)
	for k in range(15):
		m = 0
		while m < len(tenpai[k]):
			tk = str(tenpai[k][m]) # string
			# find hai that is a kung
			ntk = nhai(tk)
			n4 = []
			for hai in ntk:
				if ntk[hai] == 4:
					n4.append(int(hai) - 1)
			# there is no kung in this tehai
			if n4 == []:
				m += 1
				continue
			mk = toint(sorted(set(machi[k][tk] + n4))) # integer
			found = False
			for i in range(15):
				for j in range(len(tenpaiex[i])):
					tj = str(tenpaiex[i][j]) # string
					mj = toint(machiex[i][tj]) # integer
					if mj == mk:
						s = remove_str(tk, tj)
						if not s or int(s) not in agariset[k-i]:
							continue
						print("Repeated in case 4:", tj, "&", tk, file = delc4msg)
						print("Length:", i, "&", k, file = delc4msg)
						print("Delete:", tk, file = delc4msg)
						del tenpai[k][m], tenpaigaps[k][m]
						del machi[k][tk], machigaps[k][m]
						found = True
						break
				if found:
					break
			if not found:
				m += 1
	delc4msg.close()

	# print remained tenpaimachi after checking case 4
	c4txt = open("tenpaimachic4.txt", "w")
	fprintmachi(c4txt, tenpai, machi)
	c4txt.close()
	c4json = open("tenpaimachic4.json", "w")
	c4json.write(json.dumps([tenpai, machi]))
	c4json.close()

	# print revised gaps after checking case 4
	gapsc4txt = open("gapsc4.txt", "w")
	fprintgaps(gapsc4txt, tenpai, tenpaigaps, machigaps)
	gapsc4txt.close()

	# write revised gaps to json after checking case 4
	gapsc4json = open("gapsc4.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc4json)
	gapsc4json.close()

	# print menchan
	menchantxt = open("menchanc4.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc4.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc4sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc4sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def del_c5():
	# load remained tenpaimachi after checking case 4 from json
	with open("tenpaimachic4.json") as f:
		[tenpai, machi] = json.load(f)

	# load revised gaps after checking case 4 from json
	with open("gapsc4.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 5
	delc5msg = open("delc5msg.txt", "w")
	print("Single wait chitoitsu pattern (in case 5):", file = delc5msg)
	m = 0
	while m < len(tenpai[13]):
		tk = str(tenpai[13][m]) # string
		mk = toint(machi[13][tk]) # integer
		if mk > 10:
			m += 1
			continue
		ntk = nhai(tk)
		ntoitsu = 0
		for hai in ntk:
			if ntk[hai] == 2:
				ntoitsu += 1
		if ntoitsu == 6:
			print("Delete:", tk, "\tMachi:", mk, file = delc5msg)
			del tenpai[13][m], tenpaigaps[13][m]
			del machi[13][tk], machigaps[13][m]
		else:
			m += 1
	delc5msg.close()

	# print remained tenpaimachi after checking case 5
	c5txt = open("tenpaimachic5.txt", "w")
	fprintmachi(c5txt, tenpai, machi)
	c5txt.close()
	c5json = open("tenpaimachic5.json", "w")
	c5json.write(json.dumps([tenpai, machi]))
	c5json.close()

	# print revised gaps after checking case 5
	gapsc5txt = open("gapsc5.txt", "w")
	fprintgaps(gapsc5txt, tenpai, tenpaigaps, machigaps)
	gapsc5txt.close()

	# write revised gaps to json after checking case 5
	gapsc5json = open("gapsc5.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc5json)
	gapsc5json.close()

	# print menchan
	menchantxt = open("menchanc5.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc5.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc5sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc5sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def findagarimachi(agari):
	agarimachi = [{}, {}, {}, {}]
	for i in [2, 5, 8, 11]:
		ii = (i - 2) // 3
		for ta in agari[i]:
			for j in range(9):
				tb = ta + [j]
				tb.sort()
				if tb in agari[i + 1]:
					tta = toint(ta)
					if tta not in agarimachi[ii]:
						agarimachi[ii][tta] = [j]
					else:
						agarimachi[ii][tta].append(j)
	return agarimachi

def find_agarimachi():
	# load normal agari pattern together with chitoitsu agari pattern from json
	with open("agarichi.json") as f:
		agarichi = json.load(f)
	agari = agarichi

	# calculate agarimachi
	# agarimachi is a list of 4 dicts, agarimachi[i] is a dict whose keys are i*3+2 length agari pattern that are possible to add 1 hai to become i*3+3 length agari pattern and the values are such hai
	agarimachi = findagarimachi(agari)

	# print agarimachi for checking use
	agarimachitxt = open("agarimachi.txt", "w")
	for i in range(4):
		print("maisuu:", i*3+2, file = agarimachitxt)
		for j in agarimachi[i]:
			print(j, "\tmachi:", toint(agarimachi[i][j]), file = agarimachitxt)
		print("total:", len(agarimachi[i]), file = agarimachitxt)
	agarimachitxt.close()

	# print agarimachi to json for quick load
	agarimachijson = open("agarimachi.json", "w")
	print(json.dumps(agarimachi), file = agarimachijson)
	agarimachijson.close()

def calc_agarimachi_gaps():
	# load agarimachi from json
	with open("agarimachi.json") as f:
		agarimachi = json.load(f)

	# start calculating gaps
	# another definition of gaps: the gap of hai a is the distance between a and the first hai of tehai.
	agarigaps = [{} for k in range(4)]
	machigaps = [{} for k in range(4)]
	for i in range(4):
		for j in agarimachi[i]:
			k = agarimachi[i][j]
			agarigaps[i][j] = calcgaps(j)
			machigaps[i][j] = calcgaps(str(toint(k)))

	# print agarigaps and machigaps for checking use
	amgapstxt = open("agarimachigaps.txt", "w")
	for i in range(4):
		print("maisuu:", i*3+2, file = amgapstxt)
		for j in agarimachi[i]:
			print("tehai:", j, "\tmachi:", agarimachi[i][j], file = amgapstxt)
			print("gaps:", agarigaps[i][j], "\tmachigaps:", machigaps[i][j], file = amgapstxt)
		print("total:", len(agarimachi[i]), file = amgapstxt)
	amgapstxt.close()

	# write agarigaps and machigaps to json file for quick load
	amgapsjson = open("agarimachigaps.json", "w")
	print(json.dumps([agarigaps, machigaps]), file = amgapsjson)
	amgapsjson.close()

def del_c6():
	# load agarimachi from json
	with open("agarimachi.json") as f:
		agarimachi = json.load(f)

	# load agarimachigaps from json
	with open("agarimachigaps.json") as f:
		[agaps, mgaps] = json.load(f)

	# load remained tenpaimachi after checking case 5 from json
	with open("tenpaimachic5.json") as f:
		[tenpai, machi] = json.load(f)

	# load revised gaps after checking case 5 from json
	with open("gapsc5.json") as f:
		[tenpaigaps, machigaps] = json.load(f)

	# delete repeated items matching case 6
	delc6msg = open("delc6msg.txt", "w")
	for i in [4, 7, 10, 13]:
		j = 0
		while j < len(tenpai[i]):
			bf = False
			tj = str(tenpai[i][j]) # string
			mj = str(toint(machi[i][tj])) # string
			for p in range(0, (i-2)//3+1):
				q = (i-[2, 5, 8, 12][p]-2)//3
				for x in agarimachi[p]:
					sa = remove_str(tj, x)
					if sa == None or sa not in agarimachi[q]:
						continue
					mx = str(toint(agarimachi[p][x]))
					ma = remove_str(mj, mx)
					if ma == None:
						continue
					mga = calcgaps(ma)
					agx = agaps[p][x]
					mgx = mgaps[p][x]
					agsa = agaps[q][sa]
					mgsa = mgaps[q][sa]
					k = j + 1
					while k < len(tenpai[i]):
						tk = str(tenpai[i][k]) # string
						mk = str(toint(machi[i][tk])) # string
						if c_maisuu(tj, mj) != c_maisuu(tk, mk):
							k += 1
							continue
						for y in agarimachi[p]:
							my = str(toint(agarimachi[p][y]))
							mb = remove_str(mk, my)
							if mb == None:
								continue
							mgb = calcgaps(mb)
							agy = agaps[p][y]
							mgy = mgaps[p][y]
							if agx == agy and mgx == mgy or agx == agy[::-1] and mgx == mgy[::-1]:
								sb = remove_str(tk, y)
								if sb == None or sb not in agarimachi[q]:
									continue
								agsb = agaps[q][sb]
								mgsb = mgaps[q][sb]
								if mga != mgsa or mgb != mgsb:
									continue
								if (mga == mgb and mgsa == mgsb and agsa == agsb
									or mga == mgb[::-1] and mgsa == mgsb[::-1] and agsa == agsb[::-1]):
									print("Repeated in case 6:", tj, "&", tk, file = delc6msg)
									print("Length:", i, file = delc6msg)
									deltj = False
									lenmj = len(mj)
									lenmk = len(mk)
									if lenmj < lenmk:
										deltj = True
									elif lenmj == lenmk:
										mdtj = maxdev5(tj)
										mdtk = maxdev5(tk)
										if mdtj > mdtk:
											deltj = True
										elif mdtj == mdtk:
											lotj = int(tj[-1]) - int(tj[0])
											lotk = int(tk[-1]) - int(tk[0])
											if lotj > lotk:
												deltj = True
											elif lotj == lotk:
												abstj = abs(5-avgs(tj))
												abstk = abs(5-avgs(tk))
												if abstj > abstk:
													deltj = True
									if deltj:
										print("Delete:", tj, file = delc6msg)
										del tenpai[i][j], tenpaigaps[i][j]
										del machi[i][tj], machigaps[i][j]
										j -= 1
										bf = True
										break
									else:
										print("Delete:", tk, file = delc6msg)
										del tenpai[i][k], tenpaigaps[i][k]
										del machi[i][tk], machigaps[i][k]
										k -= 1
										break
						if bf:
							break
						k += 1
					if bf:
						break
				if bf:
					break
			j += 1
	delc6msg.close()

	# print remained tenpaimachi after checking case 6
	c6txt = open("tenpaimachic6.txt", "w")
	fprintmachi(c6txt, tenpai, machi)
	c6txt.close()
	c6json = open("tenpaimachic6.json", "w")
	c6json.write(json.dumps([tenpai, machi]))
	c6json.close()

	# print revised gaps after checking case 6
	gapsc6txt = open("gapsc6.txt", "w")
	fprintgaps(gapsc6txt, tenpai, tenpaigaps, machigaps)
	gapsc6txt.close()

	# write revised gaps to json after checking case 6
	gapsc6json = open("gapsc6.json", "w")
	print(json.dumps([tenpaigaps, machigaps]), file = gapsc6json)
	gapsc6json.close()

	# print menchan
	menchantxt = open("menchanc6.txt", "w")
	menchan = fprintmenchan(menchantxt, tenpai, machi) # sortby = None, sort by tehai
	menchanjson = open("menchanc6.json", "w")
	menchanjson.write(json.dumps(menchan))
	menchanjson.close()

	# print menchan sorted by maisuu
	menchanmstxt = open("menchanc6sortbms.txt", "w")
	menchanms = fprintmenchan(menchanmstxt, tenpai, machi, sortby = compare_by_maisuu) # sort by machi maisuu
	menchanmstxt.close()
	menchanmsjson = open("menchanc6sortbms.json", "w")
	menchanmsjson.write(json.dumps(menchanms))
	menchanmsjson.close()

def main():
	# find_all()

	# find_agari()

	# find_tenpai()

	# find_agarichi()

	# find_tenpaichi()

	# find_tenpaimachi()

	# delete repeated items
	# repeated cases:
	# (1-1) 34 and 45, 12 and 89, 1114 and 1115 ...
	# calculate gaps of tenpai and machi, gaps are the same for identical tenpai pattern.
	# (1-2) 1113 and 1333, 1112 and 8999, 1189 and 1255 ...
	# gaps can also be symmetric for identical tenpai pattern.
	# (2) 12 and 45, 1233 and 4456 ...
	# penchan 12 is actually an edge case of ryanmen 45, ryanmen 45 waits 36 and penchan 12 waits 03 (0 removed). we can remove such repeated items for further simplification.
	# (3) 23 and 2377 and 23789 ...
	# they have same machi 14, and remove 23 from them forms agari patterns, thus they are extensions of 23.
	# (4) 4477 and 3344445577 and 4455667777 ...
	# one of the original machihai is a kung (it happens in shanpon or shanpon fukugou pattern), so that machihai is disabled. we can delete them as repeated pattern.
	# (5) single wait chitoitsu tenpai pattern
	# we only need to specially memorize those chitoitsu tenpai pattern which can also be normal tenpai pattern, such as 1122334455677, it waits 3 and 6, 3 to be normal agari pattern, 6 to be chitoitsu agari pattern (or normal agari pattern). chitoitsu tenpai pattern such as 1122335566779 is not a normal tenpai pattern, we can easily recognize them thus we don't need to specially memorize them, so we delete them as repeated pattern.
	# (6-1) 3366 (machi: 36) and 4455 (machi: 45) and 4466 (machi: 46) ...
	# shanpon pattern or shanpon fukugou pattern, if two tehai differs only in shanpon hai, and their machihai differs only in shanpon hai, thus the two tehai are repeated in this case.
	# (6-2) 2255567 (machi: 258) and 3455566 (256), 1134567888 (machi: 1258) and 1133345678 (machi: 1369) ...
	# when deleted xx from tehai a, deleted x from a's machi hai, deleted yy from b, deleted y from b's machi hai, a with its machi hai equals b with its machi hai. x and y are in range(9). Here, "equals" means mgj == mgk and agj == agk or mgj == mgk[::-1] and agj == agk[::-1], agj and agk are gaps of tehai of agari[2, 5, 8, 11], mgj and mgk are gaps of machi hai that can turn agari[2, 5, 8, 11] to agari[3, 6, 9, 12]. case 6-1 is included here.
	# (6-3) 1112367888 (machi: 1458) and 1112366678 (machi: 1469) ...
	# after deleted x from tehai a, deleted x's machi hai from a's machi hai, deleted y from tehai b, deleted y's machi hai from b's machi hai, a and b becomes equaled. Here, x and y are equaled, and they are from agarimachi[i] and i is in range(4) (agarimachi[0] is about case 6-2) and i*3+2 is smaller than length of a and b (a and b are of same length, of course). Here, "equaled" means mgj == mgk and agj == agk or mgj == mgk[::-1] and agj == agk[::-1], where agj is gaps of a, agk is gaps of b, mgj is gaps of agarimachi[i][a], mgk is gaps of agarimachi[i][b].

	# calc_gaps()

	# del_c1()

	del_c2()

	del_c3()

	del_c4()

	del_c5()

	# find_agarimachi()

	# calc_agarimachi_gaps()

	del_c6()

	# prevent an empty main() function
	pass

	# We can construct all tenpai pattern with manzu, pinzu, souzu and jihai using the remained tenpai pattern and agari pattern. Here is the way to construct all tenpai pattern:
	# (1) Let's name agari pattern with maisuu of 2, 5, 8 and 11 as jantou agari pattern, thus we can build a tenpai pattern from combination of two jantou agari pattern.
	# (2) We can construct a tenpai pattern by combining one simplified tenpai pattern of some color and one or more agari pattern of some colors. The only condition is that all maisuu of hai didn't exceeds 4. Considering that we need only simplified tenpai pattern, thus these tenpai pattern is exactly chinitsu tenpai pattern. However, we can remove tenpai pattern which matches situation (1) from here. And tenpai pattern whose machi decreases because some maisuu of hai exceeds 4 could be regarded as repeated pattern.
	# (3) Jihai agari pattern and jihai tenpai pattern should also be considered in situation (1) and situation (2). However, we can also ignore them, because they could only be toitsu and kotsu, which have been considered in suupai pattern, which means jihai pattern are actually part of suupai pattern.
	# (4) Special cases: single wait chitoitsu pattern and kokushi tenpai pattern. There is only one 13-menchan kokushi tenpai pattern and C(13,2)=13*12/2=78 tanki kokushi tenpai pattern. We can list them at the last.

if __name__ == '__main__':
	main()
