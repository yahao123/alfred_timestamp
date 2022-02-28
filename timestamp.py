from datetime import datetime
import time
import sys
import pytz


def timestamp_to_datetime(timestamp, tz=None):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (datetime 格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回 datetime 格式 {datetime}2016-02-25 20:21:04.242000
    """

    local_dt_time = datetime.fromtimestamp(timestamp / 1000.0, tz=tz).strftime('%Y-%m-%d %H:%M:%S')
    return local_dt_time


def strtime_to_datetime(timestr):
    """将字符串格式的时间 (含毫秒) 转为 datetiem 格式
    :param timestr: {str}'2016-02-25 20:21:04.242'
    :return: {datetime}2016-02-25 20:21:04.242000
    """
    format = '%Y-%m-%d %H:%M:%S'
    if '.' in timestr:
        format = '%Y-%m-%d %H:%M:%S.%f'

    local_datetime = datetime.strptime(timestr, format)
    return local_datetime


def datetime_to_timestamp(datetime_obj):
    """将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :return: 13 位的毫秒时间戳 1456402864242
    """
    local_timestamp = time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0
    return int(local_timestamp)


def strtime_to_timestamp(local_timestr):
    """将本地时间 (字符串格式，含毫秒) 转为 13 位整数的毫秒时间戳
    :param local_timestr: {str}'2016-02-25 20:21:04.242'
    :return: 1456402864242
    """
    local_datetime = strtime_to_datetime(local_timestr)
    timestamp = datetime_to_timestamp(local_datetime)
    return timestamp


def datetime_to_strtime(datetime_obj):
    """将 datetime 格式的时间 (含毫秒) 转为字符串格式
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :return: {str}'2016-02-25 20:21:04.242'
    """

    local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    return local_str_time


def current_datetime():
    """返回本地当前时间, 包含datetime 格式, 字符串格式, 时间戳格式
    :return: (datetime 格式, 字符串格式, 时间戳格式)
    """

    # 当前时间：datetime 格式
    local_datetime_now = datetime.now()
    # 当前时间：字符串格式
    local_strtime_now = datetime_to_strtime(local_datetime_now)
    # 当前时间：时间戳格式 13位整数
    local_timestamp_now = datetime_to_timestamp(local_datetime_now)
    return local_datetime_now, local_strtime_now, local_timestamp_now


def current_timestamp(time_zone):
    # 当前时间：datetime 格式
    local_datetime_now = datetime.now(tz=time_zone)
    # 当前时间：时间戳格式 13位整数
    return datetime_to_timestamp(local_datetime_now)


def getTimeZoneList():
    tzList = []
    # 查询中国所拥有的时区
    # cn = pytz.country_timezones('cn')
    # for i in cn:
    #     print(pytz.timezone(i))
    #     print(type(pytz.timezone(i)))
    #     tzList.append(pytz.timezone(i))
    # # 查询美国所拥有的时区
    # us = pytz.country_timezones('us')
    # for i in us:
    #     tzList.append(pytz.timezone(i))

    tzList.append(pytz.timezone("UTC"))
    tzList.append(pytz.timezone("Asia/Shanghai"))
    return tzList


def build_result(result):
    item_str = '<item uid="timestamp" arg="{}"><title>{}</title><subtitle>Press Enter to ' \
               'paste</subtitle><icon>icon.png</icon></item> '
    xml_prefix = """<?xml version="1.0" encoding="utf-8"?>\n<items>"""
    item_xml = ""
    for i in result:
        copy_value = i['value']
        item_xml = item_xml + item_str.format(copy_value, i['key'] + " " + str(copy_value))
    return xml_prefix + item_xml + '</items>'


if __name__ == '__main__':
    param = "now"
    # 获取到时区列表
    tzList = getTimeZoneList()
    if len(sys.argv) >= 2:
        param = sys.argv[1]
    result = []
    try:
        # 获取当前时间戳
        if param == 'now':
            """获取当前时间戳"""
            for tz in tzList:
                timestamp = current_timestamp(tz)
                timestampMap = {'key': str(tz), 'value': timestamp}
                result.append(timestampMap)
        elif len(param) == 13:
            """时间戳转换成时间"""
            for tz in tzList:
                timeStr = timestamp_to_datetime(int(param), tz)
                timestampMap = {'key': str(tz), 'value': timeStr}
                result.append(timestampMap)
        else:
            """时间格式转换成时间戳"""
            # print(param)
            # 将时间字符串转换成时间戳
            timestampMap = {'key': 'timestamp', 'value': strtime_to_timestamp(param)}
            result.append(timestampMap)
    except Exception as e:
        timestampMap = {'key': '格式有误', 'value': '格式有误'}
    sys.stdout.write(build_result(result))
