# -*- coding: utf-8 -*-
import pymysql
import networkx as nx
from settings import max_nodes, sql_template



def init():
	conn = pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = 'root',
			password = '111',
			charset ='utf8',
			db = 'online_social_networks')
	cursor = conn.cursor()
	return conn, cursor

def execute(cursor, conn, sql):
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		print("存入数据库失败")
		conn.rollback()
	# 向数据库提交执行的语句

def get_all_user():
	fname = "advogato"
	users = set()
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(" ")
			source = combo[0]
			target = combo[1]
			users.add(source)
			users.add(target)
	print(len(users))
	print(users)

def load_data_into_mysql():
	fname = "advogato"
	cnt = 0
	content = "source = {}, target = {}, and relation = {}"
	conn, cursor = init()
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(" ")
			source = combo[0]
			target = combo[1]
			relation = combo[2]
			if source == target:
				continue
			print(content.format(source, target, relation))
			sql = sql_template.format(source, target, relation)
			execute(cursor, conn, sql)
			cnt += 1
	print(cnt)

def paths(source, target, cutoff=4):
	fname = "advogato"
	edges = []
	with open(fname, 'r') as file:
		for line in file:
			line = line.strip()
			combo = line.split(" ")
			source_1 = combo[0]
			target_1 = combo[1]
			relation = combo[2]
			if source_1 == target_1:
				continue
			edges.append((source_1, target_1, relation))
	print(source)
	G = nx.DiGraph()
	G.add_weighted_edges_from(edges)
	print(G.number_of_edges())
	paths = list(nx.all_simple_paths(G,source,target, cutoff=int(cutoff)))
	print(len(paths))
	# print(paths)
	nodes = []
	if len(paths) > max_nodes:
		for i in range(0,max_nodes):
			print(paths[i])
			for j in range(0, len(paths[i])-1):
				source = paths[i][j]
				target = paths[i][j+1]
				relation = G.get_edge_data(source, target)
				node = {'source':source, 'target': target, 'type': "resolved", 'rela': relation['weight']}
				nodes.append(node)
				print(node)
	else:
		print(paths)
		for i in range(0,len(paths)):
			for j in range(0, len(paths[i])-1):
				source = paths[i][j]
				target = paths[i][j+1]
				relation = G.get_edge_data(source, target)
				node = {'source':source, 'target': target, 'type': "resolved", 'rela': relation['weight']}
				nodes.append(node)
	print(nodes)
	return nodes


if __name__ == '__main__':
	pass