from lxml import html


def get_item(item):
    name = item.xpath("./div/div[1]/a/@title")[0]
    url = homepage_url + item.xpath("./div/div[1]/a/@href")[0]
    print([name, url])

    address = item.xpath("./div/a[1]/text()")[1].strip()

    area_type = item.xpath("./div/a[2]/span[2]/text()")[0]
    area_str = item.xpath("./div/a[2]/span[last()]/text()")[0]
    area = area_str.replace("建面 ", "").replace("㎡", "")

    price = item.xpath("./div/div[4]/div[1]/span[1]/text()")[0]
    total_str = item.xpath("./div/div[4]/div[2]/text()")[0]
    total = total_str.replace("总价", "").replace("(万/套)", "")

    arr = [name, url, address, area_type, area, price, total]
    return arr


def get_error_item(item):
    name = item.xpath("./div/div[1]/a/@title")[0]
    url = homepage_url + item.xpath("./div/div[1]/a/@href")[0]

    return [name, url]


def get_data(total_page):
    data = []
    error_data = []
    for j in range(1, total_page + 1):
        file_content = ""
        try:
            with open(f"pages/page{j}.html") as f:
                file_content = f.read()
            tree = html.fromstring(file_content)
        except:
            continue

        lists = tree.xpath("/html/body/div[6]/ul[2]/li")
        for i in range(len(lists)):
            item = lists[i]
            try:
                arr = get_item(item)
                data.append(arr)
            except:
                error_str = get_error_item(item)
                error_info = (
                    f"error in page {j}, item {i+1}, {error_str[0]}, {error_str[1]}"
                )
                error_data.append(error_info)
                print(error_info)
                continue
    return [data, error_data]


def write_data_to_file(data, error_data):
    with open("house_data.txt", "w", encoding="utf-8") as target:
        for da in data:
            target.write(str(da) + "\n")
        target.write("-----------------\n")
        for da in error_data:
            target.write(str(da) + "\n")


if __name__ == "__main__":
    # 文件数量，不小于实际数量即可
    total_page = 99
    # 列表地址，用于获取首页地址
    init_url = ""
    # 首页网址，用于拼接楼盘页面地址
    homepage_url = init_url.split("/loupan")[0]
    data, error_data = get_data(total_page)
    write_data_to_file(data, error_data)
