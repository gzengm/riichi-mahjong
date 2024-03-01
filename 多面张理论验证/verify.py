import json
import copy

def multi(a, b):
	ret = []
	for i in a:
		for j in b:
			ret.append(i + j)
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

def sortptn(ptn):
	for i in range(len(ptn)):
		for k in ptn[i]:
			if len(k) > 1:
				k.sort()
		ptn[i].sort()
		# 去重
		j = 0
		while j < len(ptn[i]) - 1:
			if ptn[i][j] == ptn[i][j + 1]:
				ptn[i].pop(j + 1)
			else:
				j += 1

def findagari():
	agari = [[] for k in range(15)]
	a = {k : 0 for k in range(1, 10)}
	for i in range(15):
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
	sortptn(agari)
	return agari

def fprintptn(f, ptn):
	for i in range(len(ptn)):
		print(str(i)+"枚和了形", file = f)
		for k in ptn[i]:
			print(toint(k), file = f)
		print("总数："+str(len(ptn[i]))+"\n", file = f)
		f.flush()

def find_agari():
	# 找到所有清一色一般和了形
	agari = findagari()

	# 输出到txt文件
	agaritxt = open("agari.txt", "w")
	fprintptn(agaritxt, agari)
	agaritxt.close()

	# 保存agari变量的值到json文件
	agarijson = open("agari.json", "w")
	print(json.dumps(agari), file = agarijson)
	agarijson.close()

# hand是一个含1~9的列表，用于表示手牌
def toint(hand):
	ret = 0
	for i in hand:
		ret = ret * 10 + i
	return ret

def create_set_from(ptn):
	n = len(ptn)
	ptnset = [set() for k in range(n)]
	for i in range(n):
		for k in ptn[i]:
			ptnset[i].add(toint(k) if isinstance(k, list) else k)
	return ptnset

# 返回值：tanki表示单骑听牌，shanpon表示双碰听牌，ryanmen表示两面听牌（含嵌张、边张）
# 单骑听牌构成雀头，双碰听牌构成刻子，两面听牌构成顺子
def check_machi_type(agariset, hand, machi):
	tanki = shanpon = ryanmen = False
	if machi in hand:
		k = hand.copy()
		k.remove(machi)
		# 检查是否为单骑听牌
		k.sort()
		key = toint(k)
		if key in agariset[len(k)]:
			tanki = True
		# 检查是否为双碰听牌
		if machi in k:
			k.remove(machi)
			k.sort()
			key = toint(k)
			if key in agariset[len(k)]:
				shanpon = True
	# 检查是否为两面听牌
	if machi-2 in hand and machi-1 in hand:
		k = hand.copy()
		k.remove(machi-2)
		k.remove(machi-1)
		k.sort()
		key = toint(k)
		if key in agariset[len(k)]:
			ryanmen = True
	if machi-1 in hand and machi+1 in hand:
		k = hand.copy()
		k.remove(machi-1)
		k.remove(machi+1)
		k.sort()
		key = toint(k)
		if key in agariset[len(k)]:
			ryanmen = True
	if machi+1 in hand and machi+2 in hand:
		k = hand.copy()
		k.remove(machi+1)
		k.remove(machi+2)
		k.sort()
		key = toint(k)
		if key in agariset[len(k)]:
			ryanmen = True
	return tanki, shanpon, ryanmen

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
					tanki, shanpon, ryanmen = check_machi_type(agariset, rk, m)
					if key not in machidicts[i]:
						machidicts[i][key] = [[m], [m] if tanki else [], [m] if shanpon else [], [m] if ryanmen else []]
					else:
						machidicts[i][key][0].append(m)
						if tanki:
							machidicts[i][key][1].append(m)
						if shanpon:
							machidicts[i][key][2].append(m)
						if ryanmen:
							machidicts[i][key][3].append(m)
		tenpai[i] = sorted([k for k in machidicts[i]])
	return tenpai, machidicts

def fprintmachi(f, ptn, machi):
	for i in range(len(ptn)):
		print(str(i)+"枚听牌形", file = f)
		for k in ptn[i]:
			print('{0:13}\t待牌：{1:9}\t单骑待牌：{2:9}\t双碰待牌：{3:9}\t两面待牌：{4:9}'.format(str(k), str(toint(machi[i][k][0])), str(toint(machi[i][k][1])), str(toint(machi[i][k][2])), str(toint(machi[i][k][3]))), file = f)
		print("总数："+str(len(ptn[i]))+"\n", file = f)
		f.flush()

def find_tenpaimachi():
	# 从json文件中加载agari变量
	with open("agari.json") as f:
		agari = json.load(f)

	# 找到所有的清一色听牌形及其待牌
	tenpai, machi = findtenpaimachi(agari)

	# 输出到txt文件
	tenpaimachitxt = open("tenpaimachi.txt", "w")
	fprintmachi(tenpaimachitxt, tenpai, machi)
	tenpaimachitxt.close()

	# 保存[tenpai, machi]变量到json文件
	tenpaimachijson = open("tenpaimachi.json", "w")
	print(json.dumps([tenpai, machi]), file = tenpaimachijson)
	tenpaimachijson.close()

def nhai(hand):
	num = {k : 0 for k in set(hand)}
	for hai in hand:
		num[hai] += 1
	return num

def count_anko(hand):
	count = 0
	num = nhai(hand)
	for hai in num:
		if num[hai] >= 3:
			count += 1
	return count

# 旧版decompo函数，返回按从左往右的顺序找到的第一个拆解
def decompo_old(tenpaiset, hand):
	for hai in hand:
		parts = []
		if hai+1 in hand and hai+2 in hand:
			num = nhai(hand)
			t = hand.copy()
			t.remove(hai)
			t.remove(hai+1)
			t.remove(hai+2)
			if num[hai] >= 2 and num[hai+1] >= 2 and num[hai+2] >= 2:
				# 取出顺子[hai, hai, hai+1, hai+1, hai+2, hai+2]
				t.remove(hai)
				t.remove(hai+1)
				t.remove(hai+2)
				parts.append(toint([hai]*2 + [hai+1]*2 + [hai+2]*2))
			else:
				# 取出顺子[hai, hai+1, hai+2]
				parts.append(toint([hai, hai+1, hai+2]))
			p = decompo(tenpaiset, t)
			if p != None:
				parts.extend(p)
				return parts
	if toint(hand) in tenpaiset[len(hand)]:
		parts.append(toint(hand))
	else:
		parts = None
	return parts

def decompo(tenpaiset, hand):
	ok = False
	parts = []
	for hai in hand:
		if hai+1 in hand and hai+2 in hand:
			# 取出顺子[hai, hai+1, hai+2]
			t = hand.copy()
			t.remove(hai)
			t.remove(hai+1)
			t.remove(hai+2)
			p = decompo(tenpaiset, t)
			if p != None:
				parts.extend(multi([[toint([hai, hai+1, hai+2])]], p))
				ok = True
	# 合并相同的顺子
	for p in range(len(parts)):
		r = 0
		while r < len(parts[p]) - 1:
			s = r + 1
			while s < len(parts[p]):
				a = str(parts[p][r])
				b = str(parts[p][s])
				if set(a) == set(b):
					parts[p].pop(s)
					parts[p][r] = int(''.join(sorted(list(set(a))*((len(a)+len(b))//3))))
				else:
					s += 1
			r += 1
	# 需要先合并相同的顺子后再进行去除重复的拆解，否则去重不彻底
	# 原因是拆解中存在667788和678+678，导致sorted(parts[p]) == sorted(parts[q])的值为False
	# 去除重复的拆解
	p = 0
	while p < len(parts) - 1:
		q = p + 1
		while q < len(parts):
			if sorted(parts[p]) == sorted(parts[q]):
				parts.pop(q)
			else:
				q += 1
		p += 1
	if not ok:
		if toint(hand) in tenpaiset[len(hand)]:
			parts.append([toint(hand)])
		else:
			parts = None
	return parts

def check_machi(tenpai, parts, machi):
	with open("agari.json") as f:
		agari = json.load(f)
	agariset = create_set_from(agari)

	pmachi = [{} for i in range(15)]
	for i in range(15):
		for k in tenpai[i]:
			pmachi[i][k] = []
			for j in range(len(parts[i][k])):
				rpa = str(parts[i][k][j][-1])
				m = copy.deepcopy(machi[len(rpa)][rpa])
				num = nhai([int(c) for c in str(k)])
				# 不参与传递的听牌
				m0 = m1 = m2 = m3 = []
				# 已参与传递的听牌
				passed = {p : set() for p in parts[i][k][j][:-1]}
				n = 0
				while n < len(m[0]):
					mc = m[0][n]
					for p in parts[i][k][j][:-1]:
						pp = [int(c) for c in str(p)]
						# 拆解部分为暗刻
						if len(set(pp)) == 1:
							anko = pp[0]
							# 检查单骑复合形
							d = mc - anko
							if mc in m[1] and (d == 1 or d == 2 or d == -1 or d == -2
								# 1个顺子将距离连接起来
								or (d == 4 or d == 5)
								and (toint([anko+1, anko+2, anko+3]) in parts[i][k][j] or toint([anko+1, anko+1, anko+2, anko+2, anko+3, anko+3]) in parts[i][k][j])
								or (d == -4 or d == -5)
								and (toint([anko-3, anko-2, anko-1]) in parts[i][k][j] or toint([anko-3, anko-3, anko-2, anko-2, anko-1, anko-1]) in parts[i][k][j])
								# 2个顺子将距离连接起来
								or (d == 7 or d == 8)
								and (toint([anko+1, anko+2, anko+3]) in parts[i][k][j] or toint([anko+1, anko+1, anko+2, anko+2, anko+3, anko+3]) in parts[i][k][j])
								and (toint([anko+4, anko+5, anko+6]) in parts[i][k][j] or toint([anko+4, anko+4, anko+5, anko+5, anko+6, anko+6]) in parts[i][k][j])
								or (d == -7 or d == -8)
								and (toint([anko-3, anko-2, anko-1]) in parts[i][k][j] or toint([anko-3, anko-3, anko-2, anko-2, anko-1, anko-1]) in parts[i][k][j])
								and (toint([anko-6, anko-5, anko-4]) in parts[i][k][j] or toint([anko-6, anko-6, anko-5, anko-5, anko-4, anko-4]) in parts[i][k][j])
								# 3个顺子将距离连接起来
								or (d == 10 or d == 11)
								and (toint([anko+1, anko+2, anko+3]) in parts[i][k][j] or toint([anko+1, anko+1, anko+2, anko+2, anko+3, anko+3]) in parts[i][k][j])
								and (toint([anko+4, anko+5, anko+6]) in parts[i][k][j] or toint([anko+4, anko+4, anko+5, anko+5, anko+6, anko+6]) in parts[i][k][j])
								and (toint([anko+7, anko+8, anko+9]) in parts[i][k][j] or toint([anko+7, anko+7, anko+8, anko+8, anko+9, anko+9]) in parts[i][k][j])
								or (d == -10 or d == -11)
								and (toint([anko-3, anko-2, anko-1]) in parts[i][k][j] or toint([anko-3, anko-3, anko-2, anko-2, anko-1, anko-1]) in parts[i][k][j])
								and (toint([anko-6, anko-5, anko-4]) in parts[i][k][j] or toint([anko-6, anko-6, anko-5, anko-5, anko-4, anko-4]) in parts[i][k][j])
								and (toint([anko-9, anko-8, anko-7]) in parts[i][k][j] or toint([anko-9, anko-9, anko-8, anko-8, anko-7, anko-7]) in parts[i][k][j])):
								# 新增的听牌为单骑的筋与暗刻的筋之外的那组筋的两面听牌
								# 距离为1的单骑
								if abs(d) % 3 == 1:
									if d > 0:
										new1 = mc + 1
										new2 = mc - 2
									else:
										new1 = mc - 1
										new2 = mc + 2
									if new1 in range(1, 10) and new1 not in m[3]:
										m[0].append(new1)
										m[3].append(new1)
									if new2 in range(1, 10) and new2 not in m[3]:
										m[0].append(new2)
										m[3].append(new2)
								# 距离为2的单骑
								else:
									if d > 0:
										new = mc - 1
									else:
										new = mc + 1
									if new not in m[3]:
										m[0].append(new)
										m[3].append(new)
							# 检查双碰复合形
							if mc in m[2]:
								if ((mc == anko-1 and anko+1 in m[2]) or (mc == anko+1 and anko-1 in m[2])
									or (mc == anko-2 and anko-1 in m[2]) or (mc == anko-1 and anko-2 in m[2])
									or (mc == anko+2 and anko+1 in m[2]) or (mc == anko+1 and anko+2 in m[2])):
									# 新增的听牌为暗刻部分的单骑听牌
									if anko not in m[1]:
										m[0].append(anko)
										m[1].append(anko)
								# AABBCCC形还会增加AB的两面听牌，即A-1和B+1
								if ((mc == anko-2 and anko-1 in m[2]) or (mc == anko-1 and anko-2 in m[2])
									or (mc == anko+2 and anko+1 in m[2]) or (mc == anko+1 and anko+2 in m[2])
									# 1个顺子将双碰与暗刻的距离连接起来
									or ((mc == anko-5 and anko-4 in m[2]) or (mc == anko-4 and anko-5 in m[2]))
									and (toint([anko-3, anko-2, anko-1]) in parts[i][k][j] or toint([anko-3, anko-3, anko-2, anko-2, anko-1, anko-1]) in parts[i][k][j])
									or ((mc == anko+5 and anko+4 in m[2]) or (mc == anko+4 and anko+5 in m[2]))
									and (toint([anko+1, anko+2, anko+3]) in parts[i][k][j] or toint([anko+1, anko+1, anko+2, anko+2, anko+3, anko+3]) in parts[i][k][j])
									# 2个顺子将双碰与暗刻的距离连接起来
									or ((mc == anko-8 and anko-7 in m[2]) or (mc == anko-7 and anko-8 in m[2]))
									and (toint([anko-3, anko-2, anko-1]) in parts[i][k][j] or toint([anko-3, anko-3, anko-2, anko-2, anko-1, anko-1]) in parts[i][k][j])
									and (toint([anko-6, anko-5, anko-4]) in parts[i][k][j] or toint([anko-6, anko-6, anko-5, anko-5, anko-4, anko-4]) in parts[i][k][j])
									or ((mc == anko+8 and anko+7 in m[2]) or (mc == anko+7 and anko+8 in m[2]))
									and (toint([anko+1, anko+2, anko+3]) in parts[i][k][j] or toint([anko+1, anko+1, anko+2, anko+2, anko+3, anko+3]) in parts[i][k][j])
									and (toint([anko+4, anko+5, anko+6]) in parts[i][k][j] or toint([anko+4, anko+4, anko+5, anko+5, anko+6, anko+6]) in parts[i][k][j])):
									# 新增的听牌为AB的两面听牌，即A-1和B+1
									d = abs(mc - anko)
									if d % 3 == 2:
										if mc > anko:
											new1 = mc - 2
											new2 = mc + 1
										else:
											new1 = mc - 1
											new2 = mc + 2
									else:
										if mc > anko:
											new1 = mc - 1
											new2 = mc + 2
										if mc < anko:
											new1 = mc - 2
											new2 = mc + 1
									if d == 1 or d == 2:
										if new1 in range(1, 10) and new1 not in m[3]:
											m[0].append(new1)
											m[3].append(new1)
										if new2 in range(1, 10) and new2 not in m[3]:
											m[0].append(new2)
											m[3].append(new2)
									else:
										if new1 in range(1, 10) and new1 not in m[3] and new1 not in m3:
											m0.append(new1)
											m3.append(new1)
										if new2 in range(1, 10) and new2 not in m[3] and new2 not in m3:
											m0.append(new2)
											m3.append(new2)
							# 检查两面复合形
							if mc in m[3] and mc == anko:
								# 新增的听牌为雀头部分，即与暗刻部分的双碰听牌
								# 只找出拆解后剩余部分的雀头
								# hand = [int(c) for c in rpa]
								# num_rpa = nhai(hand)
								# for hai in num_rpa:
								# 	if num_rpa[hai] >= 2:
								# 		hand.remove(hai)
								# 		hand.remove(hai)
								# 		if toint(hand) in agariset[i-2]:
								# 			if hai not in m[2] and hai not in m2:
								# 				m0.append(hai)
								# 				m2.append(hai)
								# 			if anko not in m[2] and anko not in m2:
								# 				m0.append(anko)
								# 				m2.append(anko)
								# 		hand.append(hai)
								# 		hand.append(hai)
								# 		hand.sort()
								# 找出所有可以作为雀头的对子作为听牌
								hand = [int(c) for c in str(k)]
								hand.remove(anko)
								hand.remove(anko)
								for hai in num:
									if hai != anko and num[hai] >= 2:
										hand.remove(hai)
										hand.remove(hai)
										if toint(hand) in agariset[i-4]:
											if hai not in m[2]:
												m[0].append(hai)
												m[2].append(hai)
											if anko not in m[2]:
												m[0].append(anko)
												m[2].append(anko)
										hand.append(hai)
										hand.append(hai)
										hand.sort()
						# 拆解部分为顺子
						else:
							# 检查单骑听牌的传递
							if mc in m[1]:
								if mc == pp[0]-1:
									if pp[-1] in range(1, 10) and pp[-1] not in m[1]:
										m[0].append(pp[-1])
										m[1].append(pp[-1])
										passed[p].add(pp[0]-1)
										passed[p].add(pp[-1])
								elif mc == pp[-1]+1:
									if pp[0] in range(1, 10) and pp[0] not in m[1]:
										m[0].append(pp[0])
										m[1].append(pp[0])
										passed[p].add(pp[-1]+1)
										passed[p].add(pp[0])
							# 检查双碰听牌的传递
							if mc in m[2] and len(pp) == 6:
								if mc == pp[0]-1:
									if pp[-1] in range(1, 10) and pp[-1] not in m[2]:
										m[0].append(pp[-1])
										m[2].append(pp[-1])
										passed[p].add(pp[0]-1)
										passed[p].add(pp[-1])
								elif mc == pp[-1]+1:
									if pp[0] in range(1, 10) and pp[0] not in m[2]:
										m[0].append(pp[0])
										m[2].append(pp[0])
										passed[p].add(pp[-1]+1)
										passed[p].add(pp[0])
							# 检查两面听牌的传递
							if mc == pp[0]:
								if pp[-1]+1 in range(1, 10) and pp[-1]+1 not in m[3] and pp[-1]+1 not in passed[p]:
									m[0].append(pp[-1]+1)
									m[3].append(pp[-1]+1)
							elif mc == pp[-1]:
								if pp[0]-1 in range(1, 10) and pp[0]-1 not in m[3] and pp[0]-1 not in passed[p]:
									m[0].append(pp[0]-1)
									m[3].append(pp[0]-1)
					n += 1
				# 听牌传递后，除去已使用了4枚的听牌
				m[0].extend(m0)
				m[0] = sorted(set(m[0]))
				m[1].sort()
				m[2].sort()
				m[3].extend(m3)
				m[3] = sorted(set(m[3]))
				for mc in m[0]:
					if mc in num and num[mc] == 4:
						m[0].remove(mc)
						if mc in m[1]:
							m[1].remove(mc)
						if mc in m[2]:
							m[2].remove(mc)
						if mc in m[3]:
							m[3].remove(mc)
				pmachi[i][k].append(copy.deepcopy(m))
	return pmachi

def fprintparts(txtfile, tenpai, parts, pmachi, machi):
	for i in range(15):
		print(str(i)+"枚听牌形", file = txtfile)
		for k in tenpai[i]:
			for j in range(len(parts[i][k])):
				print('{0:13}\t拆解{1:4}{2:17}\t待牌: {3:27}\t原待牌: {4:27}\t{5:1}'.format(str(k), str(j+1)+': ',
					'+'.join([str(p) for p in parts[i][k][j]]),
					str([toint(m) for m in pmachi[i][k][j]]),
					str([toint(m) for m in machi[i][str(k)]]),
					"√" if pmachi[i][k][j][0] == machi[i][str(k)][0] else "×"), file = txtfile)
		print("总数："+str(len(tenpai[i])), file = txtfile)
		txtfile.flush()

def classify_tenpai():
	# 从json文件中加载tenpai和machi
	with open ("tenpaimachi.json") as f:
		[tenpai, machi] = json.load(f)

	noanko_tenpai = [[] for k in range(15)]
	oneanko_tenpai = [[] for k in range(15)]
	multianko_tenpai = [[] for k in range(15)]
	noanko_machi = [{} for k in range(15)]
	oneanko_machi = [{} for k in range(15)]
	multianko_machi = [{} for k in range(15)]

	for i in range(15):
		for k in tenpai[i]:
			n_anko = count_anko(str(k))
			if n_anko == 0:
				noanko_tenpai[i].append(k)
				noanko_machi[i][k] = machi[i][str(k)]
			elif n_anko == 1:
				oneanko_tenpai[i].append(k)
				oneanko_machi[i][k] = machi[i][str(k)]
			else:
				multianko_tenpai[i].append(k)
				multianko_machi[i][k] = machi[i][str(k)]

	noanko_txt = open("noanko_machi.txt", "w")
	fprintmachi(noanko_txt, noanko_tenpai, noanko_machi)
	noanko_txt.close()
	noanko_json = open("noanko_machi.json", "w")
	print(json.dumps([noanko_tenpai, noanko_machi]), file = noanko_json)
	noanko_json.close()

	oneanko_txt = open("oneanko_machi.txt", "w")
	fprintmachi(oneanko_txt, oneanko_tenpai, oneanko_machi)
	oneanko_txt.close()
	oneanko_json = open("oneanko_machi.json", "w")
	print(json.dumps([oneanko_tenpai, oneanko_machi]), file = oneanko_json)
	oneanko_json.close()

	multianko_txt = open("multianko_machi.txt", "w")
	fprintmachi(multianko_txt, multianko_tenpai, multianko_machi)
	multianko_txt.close()
	multianko_json = open("multianko_machi.json", "w")
	print(json.dumps([multianko_tenpai, multianko_machi]), file = multianko_json)
	multianko_json.close()

def verify_noanko(tenpaiset, machi):
	with open("noanko_machi.json") as f:
		[tenpai, machix] = json.load(f)

	parts = [{} for k in range(15)]
	for i in range(15):
		for k in tenpai[i]:
			hand = [int(c) for c in str(k)]
			parts[i][k] = []
			# 取出顺子判断听牌
			parts[i][k].extend(decompo(tenpaiset, hand))

	pmachi = check_machi(tenpai, parts, machi)
	noanko_txt = open("noanko.txt", "w")
	fprintparts(noanko_txt, tenpai, parts, pmachi, machi)
	noanko_txt.close()
	noanko_json = open("noanko.json", "w")
	print(json.dumps([tenpai, parts, pmachi]), file = noanko_json)
	noanko_json.close()

def verify_oneanko(tenpaiset, machi):
	with open("oneanko_machi.json") as f:
		[tenpai, machix] = json.load(f)

	parts = [{} for k in range(15)]
	for i in range(15):
		for k in tenpai[i]:
			hand = [int(c) for c in str(k)]
			# 取出暗刻后判断是否听牌
			num = nhai(hand)
			anko = 0
			for hai in num:
				if num[hai] >= 3:
					anko = hai
					break
			if anko != 0:
				hand.remove(anko)
				hand.remove(anko)
				hand.remove(anko)
			parts[i][k] = []
			if toint(hand) in tenpaiset[len(hand)]:
				# 取出暗刻后听牌时，取出顺子判断听牌
				parts[i][k] = multi([[toint([anko]*3)]], decompo(tenpaiset, hand))
			else:
				# 取出暗刻后未听牌时，该暗刻在手牌构成上不可作为暗刻使用，取出顺子判断听牌
				hand = [int(c) for c in str(k)]
				parts[i][k].extend(decompo(tenpaiset, hand))

	pmachi = check_machi(tenpai, parts, machi)
	oneanko_txt = open("oneanko.txt", "w")
	fprintparts(oneanko_txt, tenpai, parts, pmachi, machi)
	oneanko_txt.close()
	oneanko_json = open("oneanko.json", "w")
	print(json.dumps([tenpai, parts, pmachi]), file = oneanko_json)
	oneanko_json.close()

def verify_multianko(tenpaiset, machi):
	with open("multianko_machi.json") as f:
		[tenpai, machix] = json.load(f)

	parts = [{} for k in range(15)]
	for i in range(15):
		for k in tenpai[i]:
			hand = [int(c) for c in str(k)]
			# 取出所有暗刻后判断是否听牌
			num = nhai(hand)
			anko = []
			for hai in num:
				if num[hai] >= 3:
					anko.append(hai)
					hand.remove(hai)
					hand.remove(hai)
					hand.remove(hai)
			parts[i][k] = []
			if toint(hand) in tenpaiset[len(hand)]:
				# 取出所有暗刻后听牌时，取出顺子判断听牌
				p = []
				for hai in anko:
					p.append(toint([hai]*3))
				parts[i][k] = multi([p], decompo(tenpaiset, hand))
			else:
				# 取出所有暗刻后未听牌时，取出个别暗刻后判断是否听牌，听牌的话则取出顺子判断听牌
				ok = False
				for hai in anko:
					hand = [int(c) for c in str(k)]
					hand.remove(hai)
					hand.remove(hai)
					hand.remove(hai)
					if toint(hand) in tenpaiset[len(hand)]:
						parts[i][k].extend(multi([[toint([hai]*3)]], decompo(tenpaiset, hand)))
						ok = True
				if not ok:
					hand = [int(c) for c in str(k)]
					parts[i][k].extend(decompo(tenpaiset, hand))

	pmachi = check_machi(tenpai, parts, machi)
	multianko_txt = open("multianko.txt", "w")
	fprintparts(multianko_txt, tenpai, parts, pmachi, machi)
	multianko_txt.close()
	multianko_json = open("multianko.json", "w")
	print(json.dumps([tenpai, parts, pmachi]), file = multianko_json)
	multianko_json.close()

def verify_tenpaimachi():
	# classify_tenpai()

	with open("tenpaimachi.json") as f:
		[tenpai, machi] = json.load(f)
	tenpaiset = create_set_from(tenpai)

	# verify_noanko(tenpaiset, machi)
	verify_oneanko(tenpaiset, machi)
	# verify_multianko(tenpaiset, machi)

def main():
	# find_agari()
	# find_tenpaimachi()
	verify_tenpaimachi()

if __name__ == '__main__':
	main()
