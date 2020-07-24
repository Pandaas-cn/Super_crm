# -*- coding: utf-8 -*-
# @Time     :2020/5/27 21:33
# @Author   :12257
# @SoftWare :PyCharm
from django.conf import settings
from django.utils.safestring import mark_safe


class MyPagenation():

    def __init__(self, page, total_count, per_page_num, page_num_show, base_url, get_data=None):
        """

        :param page: 当前页
        :param total_count: 数据总数量
        :param per_page_num: 每页数据
        :param page_num_show: 显示的页码数
        :param base_url: 基本路径
        :param get_data: 查询数据_Query_dict?
        """
        self.base_url = base_url
        self.get_data = get_data
        per_page_num = settings.PER_PAGE_NUM  # 每页显示多少数据
        page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数
        customer_count = total_count
        div, mod = divmod(customer_count, per_page_num)
        if mod:
            page_num_count = div + 1
        else:
            page_num_count = div
        try:
            self.page = int(page)
        except Exception as e:
            self.page = 1
        if self.page <= 0:
            self.page = 1
        elif self.page > page_num_count:
            self.page = page_num_count
        self.page_num_count = page_num_count
        start_num = (self.page - 1) * per_page_num
        end_num = self.page * per_page_num
        page_num_half_show = page_num_show // 2
        page_num_start_show = self.page - page_num_half_show
        page_num_end_show = self.page + page_num_half_show + 1
        if page_num_start_show <= 0:  # 异常分页判断
            page_num_start_show = 1
            page_num_end_show = page_num_show + 1
        elif page_num_end_show > page_num_count:
            page_num_start_show = page_num_count - page_num_show + 1
            page_num_end_show = page_num_count + 1
        if page_num_count < page_num_end_show:
            page_num_end_show = page_num_count + 1
        self.start_num = start_num
        self.end_num = end_num
        self.page_num_start_show = page_num_start_show
        self.page_num_end_show = page_num_end_show

    @property
    def start_num_show(self):
        return self.start_num

    @property
    def end_num_show(self):
        return self.end_num

    def page_html(self):
        page_num_range = range(self.page_num_start_show, self.page_num_end_show)
        page_html = ''
        first_page_html = f'<nav aria-label="Page navigation"><ul class="pagination"><li><a href="/{self.base_url}/1?{self.get_data}" aria-label="Previous"><span ' \
                          'aria-hidden="true">首页</span></a></li>'
        page_html += first_page_html
        page_pre = ''
        page_html += page_pre
        if self.page <= 1:
            pre_page = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span ' \
                       'aria-hidden="true">&laquo;</span></a></li>'
        else:
            pre_page = f'<li><a href="/{self.base_url}/{self.page - 1}?{self.get_data}" aria-label="Previous"><span ' \
                       'aria-hidden="true">&laquo;</span></a></li>'
        page_html += pre_page
        for i in page_num_range:
            if i == self.page:
                page_html += f'<li class="active"><a href="/{self.base_url}/{i}?{self.get_data}">{i}</a></li>'
            else:
                page_html += f'<li><a href="/{self.base_url}/{i}?{self.get_data}">{i}</a></li>'
        if self.page >= self.page_num_count:
            page_next_html = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li> '
        else:
            page_next_html = f'<li><a href="/{self.base_url}/{self.page + 1}?{self.get_data}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        page_html += page_next_html
        last_page_html = f'<li><a href="/{self.base_url}/{self.page_num_count}?{self.get_data}" aria-label="Previous"><span ' \
                         'aria-hidden="true">尾页</span></a></li></ul></nav>'
        page_html += last_page_html
        return mark_safe(page_html)
