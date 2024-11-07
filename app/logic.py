from app.server.LogCollectionService import LogCollectionService




def get_detal_data(page=1, PAGE_SIZE=10):
        """
        获取分页数据
        
        Args:
            page (int, optional): 页码，默认为1. Defaults to 1.
            PAGE_SIZE (int, optional): 每页数据量，默认为10. Defaults to 10.
        
        Returns:
            tuple: 包含数据和总数量的元组 (datas, count).
        """
        # 获取分页的键
        keys = LogCollectionService.page_key(page, PAGE_SIZE)
        # 获取数据
        datas = LogCollectionService.get_data_by_key(keys)
        # 获取总数
        count = LogCollectionService.count_key()

        return datas, count


def get_today_info():
        """
        获取当天的日志信息。
        
        Args:
            无参数。
        
        Returns:
            dict: 包含当天请求信息的字典，包含以下键：
                - today_all_request (int): 当天总请求数。
                - today_success_request (int): 当天成功请求数。
                - today_fail_request (int): 当天失败请求数。
                - all_failed_urls (list): 所有失败的URL列表。
        
        """
        keys = LogCollectionService.get_key_by_today()
        datas = LogCollectionService.get_data_by_key(keys)
        today_all_request, today_success_request, today_fail_request, all_failed_urls = LogCollectionService.analyse_data(datas)
        
        dict = {
            'today_all_request': today_all_request,
            'today_success_request': today_success_request,
            'today_fail_request': today_fail_request,
            'all_failed_urls': all_failed_urls
        }
         
        return dict


def running_spiders():
    # 获取正在运行的爬虫
    running_spiders = LogCollectionService.get_running_spiders()
    return running_spiders