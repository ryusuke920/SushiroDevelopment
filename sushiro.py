import requests
from pathlib import Path
from bs4 import BeautifulSoup

output_folder = Path("img").mkdir(exist_ok = True) # 重複している場合にエラーが出ないようにする
url = "https://www.akindo-sushiro.co.jp/menu/" # スシローの公式URL
html = requests.get(url).text # url内の文字を .text として取得
soup = BeautifulSoup(html, "lxml") # BeautifulSoupオブジェクトに変更

# 寿司の名前を取得する関数
def get_sushi_name():
    sushi_name = soup.select('li > a > span.txt-wrap > span.ttl') # 寿司の名前のspanタグを抽出
    sushi_name_list = [sushi.text for sushi in sushi_name] # spanタグ内の名前のみを抽出
    return sushi_name_list

# 寿司のpng形式のURLを取得する関数
def get_sushi_image_url():
    img_link_list = soup.select("li > a > span > img") # img タグのURLを抽出
    img_list = [] # imgのURLを保管する空配列
    for img in img_link_list:
        img_url = (img.attrs["src"]) # < > や img タグを取り除き、URLのみを抽出
        img_list.append(img_url)
    return img_list[6:] # 最初の6枚はジャンル別画像なのでスキップ

# 寿司のpngを名前指定で取り込む関数
def get_sushi_image():
    sushi_name = get_sushi_name() # 寿司の名前をリストで取得
    for number, image_url in enumerate(get_sushi_image_url()):
        print(F"{number + 1}皿目、{sushi_name[number]}の取り込みが完了しました。") # debug用
        img_save_path = Path(F"/Users/ryusuke/documents/git/SushiroDevelopment/img/{sushi_name[number]}.png")
        response = requests.get(image_url)
        image = response.content
        with open(img_save_path, "wb") as product:
            product.write(image)


get_sushi_image()