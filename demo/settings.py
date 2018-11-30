max_nodes_per_level = 5             # 控制每层显示的邻居节点的个数
max_nodes = 10               # 控制路径搜索时，显示每层展示的邻居节点个数
sql_template = 'insert into relationship (source_user,target_user,trust_level) values("{}","{}","{}")'

source_template = '''
    select * from relationship where source_user="{}"
'''
all_template = '''
    select * from relationship where source_user="{}" and target_user="{}"
'''
target_template = '''
    select * from relationship where target_user="{}"
'''

entity_url = 'https://api.ownthink.com/kg/knowledge?entity={}'
mention_url = 'https://api.ownthink.com/kg/ambiguous?mention={}'
info_url = 'https://api.ownthink.com/bot?token=openbot&info={}'

level_to_int = {
    'Master':1.0,
    'Journeyer':0.75,
    'Apprentice':0.5,
    'Observer':0.25
}