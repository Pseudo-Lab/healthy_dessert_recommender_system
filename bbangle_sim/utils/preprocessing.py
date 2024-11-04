from konlpy.tag import Okt
import pandas as pd


def create_title(x):
    return str(x['option']) + ' ' + str(x['title']) + ' ' + str(x['content'])


def add_spaces(text):
    # 빵 및 디저트 관련 키워드
    keywords = [
        # 종류별 빵 키워드
        '식빵', '바게트', '크루아상', '치아바타', '베이글', 
        '브리오슈', '포카치아', '롤케이크', '파운드케이크', 
        '머핀', '스콘', '도넛', '번', '팥빵', 
        '소보로빵', '밤빵',
        
        # 케이크 종류
        '치즈케이크', '쇼트케이크', '초코케이크', 
        '생크림케이크', '딸기케이크', '타르트',
        
        # 페이스트리 종류
        '에클레어', '슈크림', '마카롱', '밀푀유', '애플파이',
        
        # 기타 디저트 종류
        '쿠키', '초콜릿', '푸딩', '젤리', 
        '마들렌', '카스텔라', '와플', '브라우니', '티라미수', '롤',
        
        # 맛 관련 키워드
        '달콤한', '달달한', '꿀맛', '설탕', 
        '초콜릿', '카라멜', '크림', '고소한', 
        '버터', '고소함', '치즈맛', '상큼한', 
        '산뜻한', '레몬맛', '라즈베리', '베리', '유자', '무화과'
        '부드러운', '촉촉한', '쫄깃한', '바삭한', 
        '부드러움', '진한', '풍부한 맛', '크림치즈'
    ]
    okt = Okt()
    tokens = okt.nouns(text)  # 명사로 분리

    extracted = [word for word in tokens if word in keywords]
    
    return [' '.join(set(extracted)), list(set(extracted))]  # ' '.join(set(tokens))

def add_spaces_(text):
    # 빵 및 디저트 관련 키워드
    keywords = [
        # 종류별 빵 키워드
        '식빵', '바게트', '크루아상', '치아바타', '베이글', 
        '브리오슈', '포카치아', '롤케이크', '파운드케이크', 
        '머핀', '스콘', '도넛', '번', '팥빵', 
        '소보로빵', '밤빵',
        
        # 케이크 종류
        '치즈케이크', '쇼트케이크', '초코케이크', 
        '생크림케이크', '딸기케이크', '타르트',
        
        # 페이스트리 종류
        '에클레어', '슈크림', '마카롱', '밀푀유', '애플파이',
        
        # 기타 디저트 종류
        '쿠키', '초콜릿', '푸딩', '젤리', 
        '마들렌', '카스텔라', '와플', '브라우니', '티라미수', '롤',
        
        # 맛 관련 키워드
        '달콤한', '달달한', '꿀맛', '설탕', 
        '초콜릿', '카라멜', '크림', '고소한', 
        '버터', '고소함', '치즈맛', '상큼한', 
        '산뜻한', '레몬맛', '라즈베리', '베리', '유자',
        '부드러운', '촉촉한', '쫄깃한', '바삭한', 
        '부드러움', '진한', '풍부한 맛', '크림치즈'
    ]
    okt = Okt()
    tokens = okt.morphs(text)  # 형태소로 분리
    return ' '.join(tokens)  # 공백으로 결합


# Removes spaces and converts to lowercase
def sanitize(x):
    if isinstance(x, list):
        # Strip spaces and convert to lowercase
        return [str.lower(i.replace(" ","")) for i in x]
    else:
        # Check if an item exists. If not, return empty string
        if isinstance (x, str):
            return str.lower(x.replace(" ",""))
        else:
            return ''


def create_soup(x):
    return str(x['option_price']) + ' ' + str(x['category']) + ' ' + x['gluten_free_tag'] + ' ' + x['high_protein_tag'] + ' ' + x['sugar_free_tag'] + ' ' + x['vegan_tag'] + ' ' + x['ketogenic_tag']    


        