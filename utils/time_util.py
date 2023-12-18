from datetime import datetime, timedelta


def get_remaining_seconds():
    """
    获取当前时间距离当天 00:00 的剩余秒数

    Returns:
        float: 当前时间距离当天 00:00 的剩余秒数
    """
    # 获取当前时间
    now = datetime.now()

    # 获取当天的 00:00 时间
    midnight = datetime.combine(now.date(), datetime.min.time())

    # 计算当前时间距离当天的 00:00 的时间差
    time_difference = midnight - now

    # 获取剩余秒数
    remaining_seconds = time_difference.total_seconds()

    return remaining_seconds


def get_remaining_seconds_until_midnight():
    """
    获取当前时间距离明天 00:00 的剩余秒数

    Returns:
        float: 当前时间距离明天 00:00 的剩余秒数
    """
    # 获取当前时间
    now = datetime.now()

    # 获取明天的 00:00 时间
    tomorrow_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 计算当前时间距离明天的 00:00 的时间差
    time_difference = tomorrow_midnight - now

    # 获取剩余秒数
    remaining_seconds = time_difference.total_seconds()

    return remaining_seconds

if __name__ == '__main__':
    print(get_remaining_seconds_until_midnight())
    print(get_remaining_seconds())
