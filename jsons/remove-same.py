import json

if __name__ == '__main__':
    unique_set = []
    result_obj = {}
    with open("localization/zh-Hans-Testing.json", mode='r', encoding='utf8') as load_file:
        json_data = json.load(load_file)
        print(json_data)
        for key, value in json_data.items():
            if key in unique_set:
                continue
            else:
                # key = key.capitalize()
                key = key.title()
                unique_set.append(key)
                result_obj[key] = value

    print(result_obj, unique_set)
    with open("localization/zh_CN.json", mode='w', encoding='utf8') as write_file:
        json.dump(result_obj, write_file, ensure_ascii=False, indent=4)
