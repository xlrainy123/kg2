# encoding=utf8
import requests
from data.data_model import init, execute, paths
from settings import max_nodes_per_level, source_template, target_template, entity_url, mention_url, info_url, \
    level_to_int
from baidu import get_baidu_url
import networkx as nx
from PIL import Image
import json
import random


def KG_View(entity):
    url = entity_url.format(entity)
    sess = requests.get(url)  # 请求
    text = sess.text  # 获取返回的数据

    response = eval(text)  # 转为字典类型
    knowledge = response['data']
    nodes = []
    if len(knowledge) == 0:
        return []
    baike_url = get_baidu_url(knowledge['entity'])
    source_node = knowledge['entity'] + '\r\n' + baike_url
    for avp in knowledge['avp']:
        if avp[1] == knowledge['entity']:
            continue
        node = {'source': source_node, 'target': avp[1], 'type': "resolved", 'rela': avp[0]}
        nodes.append(node)
    links = []
    for i in range(len(nodes)):
        node = nodes[i]
        links.append(node)
    print(links)
    nodes = []
    nodes.append(links)
    nodes.append(source_node)
    return nodes


def advogato_data_KG_source(kind, entity, level):
    conn, cursor = init()
    sql = source_template.format(entity)
    entity01 = {}
    nodes = []
    cursor.execute(sql)
    results = cursor.fetchall()
    per_level_nodes = 0
    for row in results:
        source_node = row[1]
        target_node = row[2]
        entity01[source_node] = 1  # 表示已经查询过了
        entity01[target_node] = 0  # 表示还未查询
        node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
        nodes.append(node)
        per_level_nodes += 1
        if per_level_nodes > max_nodes_per_level:
            break
    helper(entity01, nodes, level - 1, conn, cursor)
    return nodes


def helper(entity01, nodes, level, conn, cursor):
    if level <= 0:
        return
    per_level_nodes = 0
    for entity in list(entity01.keys()):
        print(entity)
        used = entity01[entity]
        if used == 1:
            continue
        sql = source_template.format(entity)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            entity01[entity] = 1
            entity01[row[2]] = 0
            # entity01.update({entity:1, row[2]:0})
            node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
            nodes.append(node)
            per_level_nodes += 1
            if per_level_nodes > max_nodes_per_level:
                break
    helper(entity01, nodes, level - 1, conn, cursor)


def advogato_data_KG_target(kind, entity):
    '''
    这个暂时没什么用
    :param kind:
    :param entity:
    :return:
    '''
    conn, cursor = init()
    if kind == 'source':
        sql = source_template.format(entity)
    else:
        sql = target_template.format(entity)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    nodes = []  # 最终结果
    seconds = []
    cnt = 0
    for row in results:
        node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
        nodes.append(node)
        seconds.append(row[2])
        cnt += 1
        if cnt > max_nodes_per_level:
            break
    thirds = []
    cnt = 0
    for source in seconds:
        sql = source_template.format(source)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
            nodes.append(node)
            thirds.append(row[2])
            cnt += 1
            if cnt > max_nodes_per_level:
                break
    cnt = 0
    for source in thirds:
        sql = source_template.format(source)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            node = {'source': row[1], 'target': row[2], 'type': "resolved", 'rela': row[3]}
            nodes.append(node)
            cnt += 1
            if cnt > max_nodes_per_level:
                break
    print(nodes)

    return nodes


def mention2entity(mention):
    '''
    获取歧义关系
    :param mention:
    :return:
    '''
    if mention == "习大大":
        nodes = []
        node = {'source': mention, 'target': "习近平", 'type': "resolved", 'rela': '同名'}
        nodes.append(node)
        second_nodes = KG_View("习近平")
        for node in second_nodes[0]:
            nodes.append(node)
        return nodes
    else:
        url = mention_url.format(mention)
        sess = requests.get(url)
        text = sess.text
        entities = eval(text)  # 转为字典类型
        print(entities)
        print(entities['data'])
        nodes = []
        for row in entities['data']:
            print("row[0]:", row[0])
            contents = KG_View(row[0])
            if len(contents) == 0:
                node = {'source': mention, 'target': row[0], 'type': "resolved", 'rela': '同名'}
                nodes.append(node)
                continue
            second_nodes = contents[0]
            source_node = contents[1]
            node = {'source': mention, 'target': source_node, 'type': "resolved", 'rela': '同名'}
            nodes.append(node)
            for node in second_nodes:
                print(node)
                if node['rela'] == '国籍':
                    continue
                if node['rela'] == '民族':
                    continue
                if node['rela'] == '中文名':
                    continue
                nodes.append(node)
    return nodes


def question2info(question):
    '''
    问答
    :param questtion:
    :return:
    '''
    url = info_url.format(question)
    sess = requests.get(url)
    text = sess.text
    answer = eval(text)
    print(answer)
    return answer


def get_paths(source, target, cutoff):
    return paths(source, target, cutoff)


'''
    page_rank值
'''


def get_page_rank():
    fname = "advogato"
    edges = []
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            combo = line.split(" ")
            source_1 = combo[0]
            target_1 = combo[1]
            relation = level_to_int[combo[2]]
            if source_1 == target_1:
                continue
            edges.append((source_1, target_1, relation))
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    pr = nx.pagerank(G, alpha=0.9)
    print(pr)
    cnt = 0
    pairs = normalizatiion(pr)
    with open("page_rank.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')
    print(cnt)


def set_size_image():
    file = "logo.png"
    out_file = "out_logo.jpg"
    logo = Image.open(file)
    (x, y) = logo.size
    print(x, y)
    x1 = 50
    y1 = 50
    out = logo.resize((x1, y1), Image.ANTIALIAS)
    out.save(out_file, quality=95)


'''
    生成图
'''


def generate_graph():
    fname = "advogato"
    edges = []
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            combo = line.split(" ")
            source_1 = combo[0]
            target_1 = combo[1]
            relation = level_to_int[combo[2]]
            if source_1 == target_1:
                continue
            edges.append((source_1, target_1, relation))
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    return G


'''
    计算网络中数据的中心性指标
'''


def get_centrality():
    G = generate_graph()
    pairs = nx.degree_centrality(G)
    cnt = 0
    for name, value in pairs.items():
        cnt += 1
        print(name, value)
    print(cnt)
    pairs = normalizatiion(pairs)
    with open("centrality.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')


'''
eigenvector_centrality
'''


def get_eigenvector_centrality():
    G = generate_graph()
    pairs = nx.eigenvector_centrality(G)
    cnt = 0
    for name, value in pairs.items():
        cnt += 1
        print(name, value)
    print(cnt)
    pairs = normalizatiion(pairs)
    with open("eigenvector_centrality.txt", 'w') as data:
        for name, value in pairs.items():
            content = name + "," + str(value)
            data.write(content + '\n')


'''
    归一化
'''


def normalizatiion(pairs):
    min_value = 1000000
    max_value = -1000000
    for name, value in pairs.items():
        min_value = min(min_value, value)
        max_value = max(max_value, value)
    print(min_value, max_value)
    for name, value in pairs.items():
        value = (value - min_value) / (max_value - min_value)
        pairs.update({name: value})
    print(pairs)
    return pairs


def test():
    with open("page_rank_2.json", 'rb') as f:
        contents = json.load(f)
        nodes = contents['nodes']
        links = contents['links']
        cnt = 0
        for pair in nodes:
            if pair['name'] == "PositionErrorCallback":
                print(cnt)
                break
            cnt += 1


def generate_json_file():
    all_file = {}
    with open("page_rank_2.json", 'rb') as f:
        contents = json.load(f)
        type = contents['type']
        categories = contents['categories']
        print(type)
        print(categories)
        all_file["type"] = type
        all_file["categories"] = categories
    nodes = []
    name2int = {}
    cnt = 0
    with open("page_rank.txt", 'r') as data:
        for line in data:
            combo = line.strip().split(",")
            name = combo[0]
            value = combo[1]
            print(name, value)
            category = random.randint(0, 4)
            # print("category:",category)
            node = {'name': name, 'value': float(value)*10, 'category': category}
            name2int[name] = cnt
            if len(nodes) == 300:
                continue
            nodes.append(node)
            print(node)
            cnt += 1
    # print(nodes)
    all_file["nodes"] = nodes

    # print(name2int)
    links = []
    with open("advogato", 'r') as data:
        for line in data:
            combo = line.strip().split(" ")
            source = combo[0]
            target = combo[1]
            if source == target:
                continue
            # print(name2int[source], name2int[target])
            link = {
                       "source": name2int[source],
                       "target": name2int[target]
                   }
            links.append(link)
            if len(links) == 700:
                break
            # print(len(links))
    all_file["links"] = links

    # print(all_file)
    with open("test_json.json", 'w') as data:
        json.dump(all_file, data)

if __name__ == '__main__':
    # KG_View('习近平')
    # advogato_data_KG_target('raph', "1", 'miguel')
    # mention2entity('马云')
    # path_test()
    # question2info("美国总统是谁？")
    # get_page_rank()
    # set_size_image()
    # get_eigenvector_centrality()
    generate_json_file()
    # print(random.randint(0,4))
