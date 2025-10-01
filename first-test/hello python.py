import json
import urllib.request
import urllib.parse

import requests


def using_urllib_get():
    print("=== 使用urllib发送请求 ===")

    # 1. 发送GET请求
    try:
        # 请求URL
        url = "https://pokeapi.co/api/v2/pokemon"

        # 发送请求
        with urllib.request.urlopen(url) as response:
            # 获取响应状态码
            print(f"GET请求状态码: {response.getcode()}")

            # 读取响应内容
            data = response.read()
            # 解码为字符串
            content = data.decode('utf-8')
            # 解析为JSON（如果响应是JSON格式）
            json_data = json.loads(content)

            print("GET响应内容（部分）:")
            print(f"IP地址: {json_data.get('origin')}")
            print(f"URL: {json_data.get('url')}")
            print(f"结果-json_data: {json_data}")

    except Exception as e:
        print(f"GET请求出错: {e}")


def using_urllib_post():
    # 2. 发送POST请求
    try:
        url = "https://pokeapi.co/api/v2/pokemon"

        # 准备POST数据
        post_data = {
            "name": "Python",
            "message": "Hello, World!",
            "numbers": [1, 2, 3]
        }

        # 将数据转换为JSON字符串并编码
        data = json.dumps(post_data).encode('utf-8')

        # 创建请求对象，设置请求头
        req = urllib.request.Request(
            url,
            data,
            {'Content-Type': 'application/json'}
        )

        # 发送请求
        with urllib.request.urlopen(req) as response:
            print(f"\nPOST请求状态码: {response.getcode()}")

            # 解析响应
            content = response.read().decode('utf-8')
            json_data = json.loads(content)

            print("POST响应中的数据:")
            print(f"收到的名称: {json_data.get('json', {}).get('name')}")
            print(f"结果-json_data: {json_data}")

    except Exception as e:
        print(f"POST请求出错: {e}")


def using_urllib_request_get():
    print("\n=== 使用requests发送请求 ===")

    # 1. 发送GET请求
    try:
        url = "https://pokeapi.co/api/v2/pokemon"

        # 可以添加查询参数
        params = {
            "param1": "value1",
            "param2": "value2"
        }

        # 发送请求
        response = requests.get(url, params=params)

        print(f"GET请求状态码: {response.status_code}")

        # 直接获取JSON响应
        json_data = response.json()

        print("GET响应内容（部分）:")
        print(f"查询参数: {json_data.get('args')}")
        print(f"结果-json_data: {json_data}")

    except Exception as e:
        print(f"GET请求出错: {e}")



def using_urllib_request_post():
    # 2. 发送POST请求
    try:
        url = "https://pokeapi.co/api/v2/pokemon"

        # 准备POST数据
        post_data = {
            "username": "test_user",
            "password": "test_pass",
            "hobbies": ["coding", "reading"]
        }

        # 发送请求
        response = requests.post(
            url,
            json=post_data,  # 自动设置Content-Type为application/json
            timeout=5  # 设置超时时间
        )

        print(f"\nPOST请求状态码: {response.status_code}")

        # 解析响应
        json_data = response.json()

        print("POST响应中的数据:")
        print(f"收到的用户名: {json_data.get('json', {}).get('username')}")
        print(f"结果-json_data: {json_data}")

    except requests.exceptions.Timeout:
        print("POST请求超时")
    except Exception as e:
        print(f"POST请求出错: {e}")


if __name__ == "__main__":
    # 使用urllib发送请求
    using_urllib_get()

    # 使用requests发送请求
    using_urllib_request_get()