def separate_key_data(data):
    decoded_data = data.decode('utf-8')
    pairs = decoded_data.split('&')
    data_list = []
    for i in pairs:
        keys = i.split('=')
        value = keys[1].replace('+', ' ')
        key_value = {keys[0]: value}
        data_list.append(key_value)
    print(data_list)
    return data_list
