from app.utils.RedisManage import RedisConnectionManager
from datetime import datetime, timedelta
import json

task_redis_server = RedisConnectionManager.get_connection()
sorted_set_key = 'key_sorted_set'
running = 'running_spiders'
date_log = 'date_log'


class LogCollectionService(object):

    @classmethod
    def page_key(cls, page, PAGE_SIZE=10):

        start_index = (page - 1) * PAGE_SIZE
        end_index = start_index + PAGE_SIZE - 1

        # 从有序集合中获取分页的键
        keys = task_redis_server.zrevrange(sorted_set_key, start_index, end_index)

        return keys
    
    @classmethod
    def count_key(cls):
        # 获取有序集合的长度
        count = task_redis_server.zcard(sorted_set_key)
        return count
    
    @classmethod
    def get_data_by_key(cls,keys:list):
    
    # 从哈希表中获取数据
        datas = []
        
        for key in keys:
            
            data = task_redis_server.hgetall(key)
            # 将bytes转换为string类型
            # 转为字典
            str_data = {
                'name': data[b'name'].decode('utf-8'),
                'source': data[b'source'].decode('utf-8'),
                'site_name': data[b'site_name'].decode('utf-8'),
                'time': data[b'time'].decode('utf-8'),
                'today_all_request': int(data[b'today_all_request'].decode('utf-8')),
                'today_success_request': int(data[b'today_success_request'].decode('utf-8')),
                'today_fail_request': int(data[b'today_fail_request'].decode('utf-8')),
                'this_time_all_request': int(data[b'this_time_all_request'].decode('utf-8')),
                'this_time_success_request': int(data[b'this_time_success_request'].decode('utf-8')),
                'this_time_fail_request': int(data[b'this_time_fail_request'].decode('utf-8')),
                'last_time': data[b'last_time'].decode('utf-8'),
                'run_time': data[b'run_time'].decode('utf-8'),
                'crawl_count': int(data[b'crawl_count'].decode('utf-8')),
                'failed_urls':  json.loads(data[b'failed_urls'].decode('utf-8'))
            }

            datas.append(str_data)

        return datas
    

    @classmethod
    def get_key_by_datetime(cls,date: datetime):
        
        # 获取今天所有数据
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)
        
            # 从有序集合中获取今天的键
            keys = task_redis_server.zrangebyscore(sorted_set_key, start_of_day.timestamp(), end_of_day.timestamp())

            return keys
  

    @classmethod
    def analyse_data(cls,datas):
        # 今天爬取的所有数据
        today_all_request = 0
        # 今天爬取的成功所有数据
        today_success_request = 0
        # 今天爬取的失败所有数据
        today_fail_request = 0

        # 失败列表
        all_failed_urls = []

        for data in datas:
            today_all_request += data['today_all_request']
            today_success_request += data['today_success_request']
            today_fail_request += data['today_fail_request']
            all_failed_urls.extend(data['failed_urls'])

        return today_all_request, today_success_request, today_fail_request, all_failed_urls
    

    @classmethod
    def get_running_spiders(cls):
        
        # task_redis_server.rpush('running_spiders', self.name)
        if task_redis_server.exists(running):
            keys = task_redis_server.lrange(running, 0, -1)
            return keys
        else:
            return []    


    @classmethod
    def save_date_log(cls, datetime:datetime,value:dict):

        # 将数据存入哈希表
        datetimes = datetime.strftime('%Y-%m-%d')
        task_redis_server.hset(date_log, datetimes, json.dumps(value))
    
    @classmethod
    def get_date_log(cls):

        # 读取所有数据
        data = task_redis_server.hgetall(date_log)

        # 将字典的键转换为字符串
        data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}


        # 将字典的键转换为日期并排序
        sorted_keys = sorted(data.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)
        
        # 创建一个新的有序字典
        sorted_data = {key: data[key] for key in sorted_keys}
      
        return sorted_data