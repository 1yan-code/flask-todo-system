# 导入Flask核心库、json处理库、跨域支持库
from flask import Flask, render_template, request, jsonify
import json
import os

# 1. 初始化Flask应用
app = Flask(__name__)
# 定义数据存储文件路径
DATA_FILE = "todo_data.json"

# 2. 初始化数据文件（首次运行自动创建空的JSON文件）
def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

# 3. 定义路由1：访问首页，渲染前端页面（http://127.0.0.1:5000/）
@app.route('/')
def index():
    return render_template('index.html')

# 4. 定义路由2：查询所有待办事项（GET请求，前端获取待办列表）
@app.route('/api/todo', methods=['GET'])
def get_all_todo():
    init_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        todo_list = json.load(f)
    return jsonify({"code": 200, "data": todo_list})

# 5. 定义路由3：新增待办事项（POST请求，前端提交新待办）
@app.route('/api/todo', methods=['POST'])
def add_todo():
    init_data_file()
    # 获取前端提交的待办内容
    todo_content = request.json.get("content")
    if not todo_content:
        return jsonify({"code": 400, "msg": "待办内容不能为空！"})
    
    # 读取原有数据，生成新待办（id自增、默认未完成）
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        todo_list = json.load(f)
    new_id = len(todo_list) + 1
    new_todo = {
        "id": new_id,
        "content": todo_content,
        "is_done": False  # False=未完成，True=已完成
    }
    todo_list.append(new_todo)
    
    # 保存到JSON文件
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todo_list, f, ensure_ascii=False, indent=4)
    return jsonify({"code": 200, "msg": "添加成功！", "data": new_todo})

# 6. 定义路由4：修改待办状态/内容（PUT请求，完成/取消完成、编辑内容）
@app.route('/api/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    init_data_file()
    update_data = request.json
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        todo_list = json.load(f)
    
    # 查找对应id的待办并修改
    for todo in todo_list:
        if todo["id"] == todo_id:
            if "content" in update_data:
                todo["content"] = update_data["content"]
            if "is_done" in update_data:
                todo["is_done"] = update_data["is_done"]
            # 保存修改后的数据
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(todo_list, f, ensure_ascii=False, indent=4)
            return jsonify({"code": 200, "msg": "修改成功！"})
    return jsonify({"code": 404, "msg": "待办事项不存在！"})

# 7. 定义路由5：删除待办事项（DELETE请求，删除指定待办）
@app.route('/api/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    init_data_file()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        todo_list = json.load(f)
    
    # 过滤掉要删除的待办
    new_todo_list = [todo for todo in todo_list if todo["id"] != todo_id]
    if len(new_todo_list) == len(todo_list):
        return jsonify({"code": 404, "msg": "待办事项不存在！"})
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_todo_list, f, ensure_ascii=False, indent=4)
    return jsonify({"code": 200, "msg": "删除成功！"})

# 程序入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)