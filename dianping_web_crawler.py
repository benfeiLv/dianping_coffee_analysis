# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
import requests
import time
from openpyxl import Workbook

def get_content(font_name):
    wb = Workbook()
    sheet = wb.active
    sheet.title = '大众点评成都咖啡店650家信息'
    sheet['A1'] = 'name'
    sheet['B1'] = 'address'
    sheet['C1'] = 'mean-price'
    sheet['D1'] = 'review-num'
    sheet['E1'] = 'taste-num'
    sheet['F1'] = 'envir-num'
    sheet['G1'] = 'service-num'
    sheet['H1'] = 'recommend'
    
    #首先获取大众点评网页数据，这里只爬取了前45页
    for i in range(1,45):  
        time.sleep(40)
        url = 'http://www.dianping.com/chengdu/ch10/g132p' + str(i)
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie':  your cookie,
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/chengdu/ch10/g132',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
        html = requests.get(url, headers=headers).text
        #下面对加密文本进行解码替换:
        for code,value in font_name.items():  
            code_str = code 
            text = value
        #再在html文本中进行对比，如果文本中的编码字符与字典中的解码字符一致，就进行替换
            if code_str in html:
                html = html.replace(code_str,text)
                
        try:
            #接着对网页进行解析，提取需要的数据
            bs = BeautifulSoup(html,'lxml')
            coffee_info = bs.find('div', id='shop-all-list')    
            shops = coffee_info.find_all('li', class_="")
            #依次提取每家店的店名、地址、人均消费、评论数、各项评分、推荐菜品
            for shop in shops:
                store_name = shop.find('h4').get_text()
                address = shop.find('span', class_='addr').get_text()
                mean_price = shop.find('a', class_='mean-price')
                #这里存在部分店铺没有人均价格的情况，要分开讨论
                if mean_price.find('b') == None:
                    price = 'NaN'
                else:
                    price = mean_price.find('b').get_text()
                    price = price.replace(' ', '')
                #点评数
                review = shop.find('a', class_='review-num')
                review_num = review.find('b').get_text()
                review_num = review_num.replace('\n', '')  
                #口味、环境、服务评分
                shop_num = shop.find('span', class_='comment-list')
                taste = shop_num.find_all('b')[0].get_text()
                taste = taste.replace('\n', '')  
                envir = shop_num.find_all('b')[1].get_text()
                envir = envir.replace('\n', '')  
                service = shop_num.find_all('b')[2].get_text()
                service = service.replace('\n', '')  
                #因为有小部分店铺没有推荐菜，需要加入一个判断
                if shop.find('div', class_='recommend') != None:
                    recommend = shop.find('div', class_='recommend').get_text()
                    recommend = recommend.replace('\n', '')  
                    #print(recommend)
                    sheet.append([store_name,address,price,review_num,taste,envir,service,recommend])
                else:
                    sheet.append([store_name,address,price,review_num,taste,envir,service])
        except:
            continue
            
    wb.save('your_file_name.xlsx') 
            
def get_font():
    #这是标签为shopNum和address的字体文件
    font = TTFont('51fbf957.woff')
    #获取所有字体的上面对应的编码
    font_names = font.getGlyphOrder()
    #下面这些就是打开FontCreator软件后解析 人均多少 那个字体文件得到 所有文字和数字，共603个：
    texts = ['','','1','2','3','4','5','6','7','8',
    '9','0','店','中','美','家','馆','小','车','大',
    '市','公','酒','行','国','品','发','电','金','心',
    '业','商','司','超','生','装','园','场','食','有',
    '新','限','天','面','工','服','海','华','水','房',
    '饰','城','乐','汽','香','部','利','子','老','艺',
    '花','专','东','肉','菜','学','福','饭','人','百',
    '餐','茶','务','通','味','所','山','区','门','药',
    '银','农','龙','停','尚','安','广','鑫','一','容',
    '动','南','具','源','兴','鲜','记','时','机','烤',
    '文','康','信','果','阳','理','锅','宝','达','地',
    '儿','衣','特','产','西','批','坊','州','牛','佳',
    '化','五','米','修','爱','北','养','卖','建','材',
    '三','会','鸡','室','红','站','德','王','光','名',
    '丽','油','院','堂','烧','江','社','合','星','货',
    '型','村','自','科','快','便','日','民','营','和',
    '活','童','明','器','烟','育','宾','精','屋','经',
    '居','庄','石','顺','林','尔','县','手','厅','销',
    '用','好','客','火','雅','盛','体','旅','之','鞋',
    '辣','作','粉','包','楼','校','鱼','平','彩','上',
    '吧','保','永','万','物','教','吃','设','医','正',
    '造','丰','健','点','汤','网','庆','技','斯','洗',
    '料','配','汇','木','缘','加','麻','联','卫','川',
    '泰','色','世','方','寓','风','幼','羊','烫','来',
    '高','厂','兰','阿','贝','皮','全','女','拉','成',
    '云','维','贸','道','术','运','都','口','博','河',
    '瑞','宏','京','际','路','祥','青','镇','厨','培',
    '力','惠','连','马','鸿','钢','训','影','甲','助',
    '窗','布','富','牌','头','四','多','妆','吉','苑',
    '沙','恒','隆','春','干','饼','氏','里','二','管',
    '诚','制','售','嘉','长','轩','杂','副','清','计',
    '黄','讯','太','鸭','号','街','交','与','叉','附',
    '近','层','旁','对','巷','栋','环','省','桥','湖',
    '段','乡','厦','府','铺','内','侧','元','购','前',
    '幢','滨','处','向','座','下','県','凤','港','开',
    '关','景','泉','塘','放','昌','线','湾','政','步',
    '宁','解','白','田','町','溪','十','八','古','双',
    '胜','本','单','同','九','迎','第','台','玉','锦',
    '底','后','七','斜','期','武','岭','松','角','纪',
    '朝','峰','六','振','珠','局','岗','洲','横','边',
    '济','井','办','汉','代','临','弄','团','外','塔',
    '杨','铁','浦','字','年','岛','陵','原','梅','进',
    '荣','友','虹','央','桂','沿','事','津','凯','莲',
    '丁','秀','柳','集','紫','旗','张','谷','的','是',
    '不','了','很','还','个','也','这','我','就','在',
    '以','可','到','错','没','去','过','感','次','要',
    '比','觉','看','得','说','常','真','们','但','最',
    '喜','哈','么','别','位','能','较','境','非','为',
    '欢','然','他','挺','着','价','那','意','种','想',
    '出','员','两','推','做','排','实','分','间','甜',
    '度','起','满','给','热','完','格','荐','喝','等',
    '其','再','几','只','现','朋','候','样','直','而',
    '买','于','般','豆','量','选','奶','打','每','评',
    '少','算','又','因','情','找','些','份','置','适',
    '什','蛋','师','气','你','姐','棒','试','总','定',
    '啊','足','级','整','带','虾','如','态','且','尝',
    '主','话','强','当','更','板','知','己','无','酸',
    '让','入','啦','式','笑','赞','片','酱','差','像',
    '提','队','走','嫩','才','刚','午','接','重','串',
    '回','晚','微','周','值','费','性','桌','拍','跟',
    '块','调','糕'
    ]
    #然后我们创建一个font_name的字典，用来装字体编码和 --> 所对应的数字、汉字
    font_name = {}
    for index, value in enumerate(texts):
        #这就是大众点评乱码的结构：由前面的三个字符‘&#x’+后面是小写字母和数字+分号‘；’
        n = font_names[index].replace('uni', '&#x').lower() + ';'
        #下面生成的这个就是乱码，他就对应刚刚字体文件的对应数字，可以运行看看
        font_name[n] = value
        
    #此刻得到的就是解码的字典
    return font_name
        
if __name__ == '__main__':
    font_name = get_font()
    get_content(font_name)

