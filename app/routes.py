from app.logic import get_detal_data,get_today_info,running_spiders,get_today_fail_urls
from flask import Blueprint, render_template, request


main = Blueprint('main', __name__)

@main.route('/')
def index():
   
    # 获取当天的日志信息
    info = get_today_info()

    # 获取正在运行的爬虫
    spiders = running_spiders()
    
    return render_template('index.html',info=info, spiders=spiders)

@main.route('/details')
def getDetailInfo():
    # 获取分页数据
    page = int(request.args.get('page', 1))
    PAGE_SIZE = int(request.args.get('page', 10))
    datas, count = get_detal_data(page, PAGE_SIZE)
    
    # 分页信息
    total_pages = (count + PAGE_SIZE - 1) // PAGE_SIZE   
    return render_template('details.html', datas=datas, count=count, total_pages=total_pages, current_page=page)

@main.route('/running_spiders')
def running_spiders_route():
    # 获取正在运行的爬虫
    spiders = running_spiders()
    return render_template('running_spiders.html', spiders=spiders)

@main.route('/failed_urls')
def get_failed_urls():
    # 获取失败的URL
    urls = get_today_fail_urls()
    return render_template('failed_urls.html', urls=urls)