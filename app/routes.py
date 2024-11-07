from app.logic import get_detal_data,get_today_info,running_spiders
from flask import Blueprint, render_template, request


main = Blueprint('main', __name__)



@main.route('/')
def index():
    # 获取分页数据
    page = int(request.args.get('page', 1))
    PAGE_SIZE = int(request.args.get('page', 10))
    datas, count = get_detal_data(page, PAGE_SIZE)
    
    # 分页信息
    total_pages = (count + PAGE_SIZE - 1) // PAGE_SIZE
    
    return render_template('index.html', datas=datas, count=count, total_pages=total_pages, current_page=page)

@main.route('/today_info')
def today_info():
    # 获取当天的日志信息
    info = get_today_info()
    return render_template('today_info.html', info=info)

@main.route('/running_spiders')
def running_spiders_route():
    # 获取正在运行的爬虫
    spiders = running_spiders()
    return render_template('running_spiders.html', spiders=spiders)

