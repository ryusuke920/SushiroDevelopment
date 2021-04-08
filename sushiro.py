"""
/Q&A/
・スシローのスクレイピングを始めた理由 ... 寿司が好きだから。
・スシローの品数 ... 166品（2021/04/07現在）
・役に立つの？ ... 役に立ちません。趣味です。
"""

import requests
from pathlib import Path
from bs4 import BeautifulSoup
import random

output_folder = Path("img").mkdir(exist_ok = True) # 重複している場合にエラーが出ないようにする
url = "https://www.akindo-sushiro.co.jp/menu/" # スシローの公式URL
html = requests.get(url).text # url内の文字を .text として取得
soup = BeautifulSoup(html, "lxml") # BeautifulSoupオブジェクトに変更

# 寿司の名前を取得する関数
def get_sushi_name():
    sushi_name = soup.select('li > a > span.txt-wrap > span.ttl') # 寿司の名前のspanタグを抽出
    sushi_name_list = [sushi.text for sushi in sushi_name] # spanタグ内の名称のみを抽出

    return sushi_name_list

# 寿司のpng形式のURLを取得する関数
def get_sushi_image_url():
    img_link_list = soup.select("li > a > span > img") # img タグのURLを抽出
    img_list = [] # imgのURLを保管する空配列
    for img in img_link_list:
        img_url = (img.attrs["src"]) # < > や img タグを取り除き、URLのみを抽出
        img_list.append(img_url)

    return img_list[6:] # 最初の6枚はジャンル別画像なのでスキップ

# 寿司の.pngを名称指定で取り込む関数
def get_sushi_image():
    sushi_name = get_sushi_name() # 寿司の名称をリストで取得
    for number, image_url in enumerate(get_sushi_image_url()):
        print(F"{number + 1}皿目、{sushi_name[number]}の取り込みが完了しました。") # debug用
        img_save_path = Path(F"/Users/ryusuke/documents/git/SushiroDevelopment/img/{sushi_name[number]}.png")
        response = requests.get(image_url)
        image = response.content
        with open(img_save_path, "wb") as product:
            product.write(image)

# 寿司の情報（値段（税別）・カロリー）を取得する関数
def get_sushi_price_calorie():

    # 値段について
    price_list = [] # 値段（税別）を格納する配列
    price_calorie_class_information = soup.select("li > a > span.txt-wrap > span.price")
    price_calorie_string_information = [list(information.text.split()) for information in price_calorie_class_information] # ex.) ['280円（税込308円）', '293kcal']
    for price_string_information in price_calorie_string_information:
        price_list.append(int(price_string_information[0].split("円")[0]))
    
    # カロリーについて
    calorie_list = [] # カロリーを格納する配列
    for calorie_string_information in price_calorie_string_information:
        if len(calorie_string_information) == 2: # 砂糖なしの場合
            calorie_list.append(int(calorie_string_information[1].split("k")[0]))
        else: # 砂糖ありの場合 <- length == 3
            calorie_list.append(int(calorie_string_information[2].split("k")[0]))   

    return price_list, calorie_list

# 寿司の情報（名称・値段・カロリー）をまとめて返す関数
def get_sushi_information():
    name_information = get_sushi_name() # 寿司の名称を取得
    price_information = get_sushi_price_calorie()[0] # 寿司の値段を取得
    calorie_information = get_sushi_price_calorie()[1] # 寿司のカロリーを取得
    sushis_information = []
    for number in range(len(name_information)):
        sushis_information.append([name_information[number], price_information[number], calorie_information[number], calorie_information[number] / price_information[number]])

    return sushis_information # 名称・値段（税別）・カロリー・カロリー / 円

# 食べたい寿司が無い時に自動で決めてくれる関数
def get_random_menu(money): # 所持金
    sushi_information = get_sushi_information()
    sushi_information.sort(key = lambda x: x[1], reverse = True) # 金額の高い順にソート
    eat_menu = [] # 食べる寿司を格納する配列
    now_money = 0 # 支払った金額

    while True:
        menu_number = random.randint(0, len(sushi_information) - 1)
        if now_money + sushi_information[menu_number][1] <= money:
            eat_menu.append([sushi_information[menu_number][0], int(sushi_information[menu_number][1])]) # 食べる寿司の名称・金額
            now_money += sushi_information[menu_number][1]
        if now_money + 100 > money:
            break 

    random_sushi_menu = [random_sushi[0] for random_sushi in eat_menu]
    random_sushi_money = [random_money[1] for random_money in eat_menu]

    print(F"あなたが{money}円以内で食べる寿司メニューは、\n")
    for number in range(len(random_sushi_menu)):
        print(F"{random_sushi_menu[number]} / {random_sushi_money[number]}円")
    print(F"\n合計金額は{sum(random_sushi_money)}円です。")

    return eat_menu



"""
〜画像の取り込み方〜
① 取り込みたい階層にターミナルで cd を使って移動します
② 実行します。終わりです。
"""
# get_sushi_image() # 寿司の画像が欲しい時に実行

"""
〜ランダムに寿司を選びたい方法〜
① 取り込みたい階層にターミナルで cd を使って移動します
② 下の引数に食べたい金額をセットします
② 実行します。終わりです。
"""
# get_random_menu(10000) # 食べたい寿司が決まらない時に実行