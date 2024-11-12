from app.logic import get_detal_data,get_date_info,running_spiders,get_five_day_data
from flask import Blueprint, render_template, request


main = Blueprint('main', __name__)

@main.route('/')
def index():
   
    # 获取当天的日志信息
    info = get_date_info()
    
    # 获取正在运行的爬虫
    spiders = running_spiders()
    
    return render_template('index.html',info=info, spiders=spiders)

@main.route('/five_day')
def get_day_data():
    

    datetime_list2, today_all_request, today_success_request, today_fail_request = get_five_day_data(5)


    dict = {
        'datetime_list2': datetime_list2,
        'all_request': today_all_request,
        'success_request': today_success_request,
        'fail_request': today_fail_request
    }



    return render_template('index.html', dict=dict)



@main.route('/details')
def getDetailInfo():
    # 获取分页数据
    page = int(request.args.get('page', 1))
    PAGE_SIZE = 10
    datas, count = get_detal_data(page, PAGE_SIZE)
    
    # 分页信息
    total_pages = (count + PAGE_SIZE - 1) // PAGE_SIZE   
    return render_template('details.html', datas=datas, count=count, total_pages=total_pages, current_page=page)

