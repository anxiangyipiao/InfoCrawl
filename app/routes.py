from flask import Blueprint, render_template
from app.logic import get_redis_data

main = Blueprint('main', __name__)




@main.route('/')
def index():
    # 从 Redis 中读取数据
    data = get_redis_data()
    
    # 渲染模板并传递数据
    return render_template('index.html', data=data)