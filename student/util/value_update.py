NO_INPUT = '-12344555'  # 随机字符串


def value(previous_value, input_value):
    """if not input value, then return the previous value"""
    if input_value == NO_INPUT:
        return previous_value
    else:
        return input_value
