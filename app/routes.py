from app.logic import get_detal_data,get_date_info,running_spiders,read_day_data
from flask import Blueprint, render_template, request
import json


main = Blueprint('main', __name__)

@main.route('/')
def index():
   
    # 获取当天的日志信息

    info = get_date_info()

    chart = read_day_data()

    # 获取正在运行的爬虫
    spiders = running_spiders()
    
    return render_template('index.html',info=info, spiders=spiders, chart_data=chart)



@main.route('/details')
def getDetailInfo():
    # 获取分页数据
    page = int(request.args.get('page', 1))
    PAGE_SIZE = 10
    datas, count = get_detal_data(page, PAGE_SIZE)
    
    # 分页信息
    total_pages = (count + PAGE_SIZE - 1) // PAGE_SIZE   
    return render_template('details.html', datas=datas, count=count, total_pages=total_pages, current_page=page)

