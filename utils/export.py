import json
from utils.print import multi_style_msg


def _create_dir_if_not_exist(path):
    import pathlib
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def _clean_dir(path):
    if len(path) == 0:
        return path
    return path if path[-1] == '/' else path + '/'


def export_to_json(data, filename='data', path='', root='./data/final/', pretty=False):
    full_path = _clean_dir(root) + _clean_dir(path)
    _create_dir_if_not_exist(full_path)

    json_data = json.dumps(data, indent=2) if pretty else json.dumps(data, separators=(',', ':'))
    json_file = open(full_path + filename + '.json', 'w')
    json_file.write(json_data)

    print(multi_style_msg(
        ['Data exported to  ', [full_path + filename + '.json'], '  Woop woop!'],
        'success', decorator=True))