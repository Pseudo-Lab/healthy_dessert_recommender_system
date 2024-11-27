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

        # 추가 디저트 키워드
        '파운드', '키토 머핀', '냥빵', '단호박빵', '단호박 파운드', 
        '비스코티', '미니 치즈케이크', '휘낭시에', '크럼블', 
        '초코', '무화과 바게트', '떠먹는 케이크'

        # 건강 관련 키워드
        '저탄수', '대체당', '글루텐프리', '건강빵', '비건', 
        '저탄고지', '무설탕', '에리스리톨', '유기농', '고단백', 
        '저당', '키토식', '무밀가루', '다이어트', '콜레스테롤', 
        '충치 예방', '자일리톨', '당류 제한'       

        # 맛 관련 키워드
        '달콤한', '달달한', '꿀맛', '설탕', '초콜릿', 
        '카라멜', '크림', '고소한', '버터', '고소함', 
        '치즈맛', '상큼한', '산뜻한', '레몬맛', '라즈베리', 
        '베리', '유자', '무화과', '부드러운', '촉촉한', 
        '쫄깃한', '바삭한', '부드러움', '진한', 
        '풍부한 맛', '크림치즈', '레몬', '카카오', '단호박', 
        '병아리콩', '쑥', '얼그레이', '말차', '바나나', 
        '피칸', '코코넛', '한라봉', '헤이즐넛', '초코', 
        '복숭아', '샤인머스켓', '페퍼민트', '오렌지', 
        '블루베리', '딸기', '체리', '아몬드',


        # 보충 키워드
        '수능', '야채'
        
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


        