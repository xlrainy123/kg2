# encoding=utf8
from flask import Flask
from flask import render_template, request
from datetime import timedelta
from utils import KG_View, question2info, mention2entity, advogato_data_KG_target, source_template, target_template, get_paths, advogato_data_KG_source, get_page_rank
import json
from baidu import get_baidu_url

app = Flask(__name__)
app.config['debug'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)



@app.route('/')
def hello_world():
    return render_template('page_rank_2.html')
    # return render_template('index1.html')
    # return render_template('attribute.html')

@app.route('/attribute')
def get_attribute():
    pairs = {}
    pairs['1'] = 1
    pairs['2'] = 2
    print(pairs)
    return json.dumps(pairs)

@app.route('/evaluation_2')
def page_rank_2():
    return render_template('page_rank_2.html')

@app.route('/evaluation')
def show_evaluation_results():
    return render_template('page_rank.html')

@app.route('/demo')
def show_demo():
    print("请求方式为:", request.method)
    entity = request.args.to_dict().get('entity', '')
    # mention = request.args.to_dict().get('mention','')
    if entity == '':
        return render_template('demo.html')
    elif "source:" in entity:
        print(entity)
        line = entity.split(':')
        params = line[1].split(",")
        contents = advogato_data_KG_source('source', params[0], int(params[1]))
        print(contents)
        return render_template('index.html', contents=contents)
    elif "target:" in entity:
        print(entity)
        line = entity.split(':')
        contents = advogato_data_KG_target('target', line[1])
        print(contents)
        return render_template('index.html', contents=contents)
    elif "mention:" in entity:
        print(entity)
        line = entity.strip().split(":")
        mention = line[1]
        contents = mention2entity(mention)
        print(contents)
        return render_template('index.html', contents=contents)
    elif "attr:" in entity:
        print(entity)
        line = entity.strip().split(":")
        user = line[1]
        contents = get_page_rank(user)
        print(contents)
        return render_template('index.html', contents=contents)
    elif "path:" in entity:
        print(entity)
        line = entity.strip().split(":")
        entities = line[1].split(",")
        source = entities[0]
        target = entities[1]
        cutoff = entities[2]
        print(source, target, cutoff)
        contents = get_paths(source, target, cutoff)
        return render_template('index.html', contents=contents)
    else:
        contents = KG_View(entity)
        print(contents)
        return render_template('index.html', contents=contents[0])

@app.route('/search')
def show_search():
    return render_template('search.html')

@app.route('/answer')
def question():
    # print("请求方式为:", request.method)
    # question = request.args.to_dict().get('question', '')
    # if question == '':
    #     return "你可能忘记提问了, 试试/answer?question=刘德华的妻子是谁"
    # print(question)
    # answer = question2info(question)
    # print(answer)
    # return json.dumps(answer, ensure_ascii=False)
    return render_template("robot.html")

@app.route('/mention')
def mention():
    print("请求方式为:", request.method)
    mention = request.args.to_dict().get('mention', '')
    if mention == '':
        return "你可能忘记提问了, 试试/mention?mention=泡泡糖"
    print(mention)
    answers = mention2entity(mention)
    print(answers)
    return json.dumps(answers, ensure_ascii=False)


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
