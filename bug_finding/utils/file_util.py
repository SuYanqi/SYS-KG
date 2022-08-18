"""json文件输入输出"""
import json
import pickle
from datetime import datetime


# datetime无法写入json文件，用这个处理一下
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # convert the ISO8601 string to a datetime object
        converted = datetime.datetime.strptime(obj.value, "%Y%m%dT%H:%M:%S")
        if isinstance(converted, datetime.datetime):
            return converted.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(converted, datetime.date):
            return converted.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, converted)


class FileUtil:
    @staticmethod
    def load_json(filepath):
        """
        从文件中取数据
        :param filepath:
        :return:
        """
        with open(filepath, 'r') as load_f:
            data_list = json.load(load_f)
        return data_list

    @staticmethod
    def dump_json(filepath, data_list):
        with open(filepath, 'w') as f:
            json.dump(data_list, f)

    @staticmethod
    def load_pickle(filepath):
        """
        load 从数据文件中读取数据（object）
        :param filepath:
        :return:
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    @staticmethod
    def dump_pickle(filepath, data):
        """
        dump 将数据（object）写入文件
        :param filepath:
        :param data:
        :return:
        """
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def get_file_names_in_directory(directory, file_type="*"):
        """
        get '.file_type' file_names (paths) in directory
        @param directory: the path of directory
        @type directory: Path("", "", "")
        @param file_type: file type, such as ftl, html, xhtml
        @type file_type: string
        @return: file_names
        @rtype: [string, string, ...]
        """
        file_names = []
        for file_name in directory.glob(f"*.{file_type}"):
            file_names.append(str(file_name))
        return file_names
