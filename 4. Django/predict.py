import pandas as pd
import numpy as np
from math import log
from numpy import dot
from numpy.linalg import norm
from nltk.tokenize import WordPunctTokenizer

def title_num(code): #원하는 웹툰의 순서를 알아내는 함수
    detail_data = pd.read_csv("static/csv_data/webtoon_detail.csv",names =['웹툰제목','점수','작가','장르','추가정보','링크'])#웹툰의 기본 정보 호출
    add_num = list(range(344))# names를 작성하였기 때문에 별도로 인덱스로 nums 작성
    detail_data["num"] = add_num
    select_data = detail_data[detail_data.index == code]
    num = int(select_data['num'])
    return num

def tf(term, document): # tf-idf vectorizer 함수
    return document.count(term)

def idf(term):
    vec_data = pd.read_csv("static/csv_data/vec_data.csv",names =['댓글'])#웹툰 별 댓글들의 키워드 호출
    vec_data= vec_data.fillna('')# 결측치 제거
    vec_array_data = np.array(vec_data['댓글'])
    vec_array_list = []
    for i in range(len(vec_array_data)): # 웹툰 별 키워드 들을 하나의 리스트로 변경
        vec_array_list.append(vec_array_data[i])
    df = 0
    for doc in vec_array_list:
        if term in doc:
            df = df + 1
    return log(len(vec_array_list)/(df+1))+1

def tfidf(term, document):
    return tf(term, document)*idf(term)

def tfidf_list(text, keywords_list):
    tfidf_list = []
    for doc in text:
        tfidf_list.append([])
        for token in keywords_list:
            tfidf_list[-1].append(tfidf(token, doc))

    tfidf_pd = pd.DataFrame(tfidf_list, columns=keywords_list)# 각 키워드가 문장에 들어있는지 데이터 베이스화
    return tfidf_list, tfidf_pd

def cos_sim(A, B): #코사인 유사도를 구하는 함수
       return dot(A, B)/(norm(A)*norm(B))

def cos_sim_index(tfidf_list, tfidf_pd, num): #요청한 웹툰과 코사인 유사도가 가장 높은 순서를 찾아내는 함수입니다.
    cos_sim_list = []
    for i in range(len(tfidf_list)):
        if i == num:
            cos_sim_list.append(0)
        else:
            cos_sim_list.append(cos_sim(tfidf_pd.values[num], tfidf_pd.values[i]))
    remove_nan_list = np.nan_to_num(cos_sim_list)
    sort_list = sorted(remove_nan_list,reverse=True)
    first_num = cos_sim_list.index(max(remove_nan_list))
    second_num = cos_sim_list.index(sort_list[1])
    third_num = cos_sim_list.index(sort_list[2])
    res_list = [i for i, value in enumerate(remove_nan_list) if value == max(remove_nan_list)]
    if max(remove_nan_list)  == 0 :
        return -1
    else:
        if len(res_list) >= 3:
            return res_list
        elif len(res_list) == 2:
            res_list.append(third_num)
            return res_list
        else:
            res_list.append(second_num)
            res_list.append(third_num)
            return res_list

def main(wt_id):
    detail_data = pd.read_csv("static/csv_data/webtoon_detail.csv",names =['웹툰제목','점수','작가','장르','추가정보','링크'])#웹툰의 기본 정보 호출
    add_num = list(range(344))# names를 작성하였기 때문에 별도로 인덱스로 nums 작성
    detail_data["num"] = add_num
    vec_data = pd.read_csv("static/csv_data/vec_data.csv",names =['댓글'])#웹툰 별 댓글들의 키워드 호출
    vec_data= vec_data.fillna('')# 결측치 제거
    vec_array_data = np.array(vec_data['댓글'])
    vec_array_list = []
    for i in range(len(vec_array_data)): # 웹툰 별 키워드 들을 하나의 리스트로 변경
        vec_array_list.append(vec_array_data[i])
    input_code = wt_id# 웹툰의 코드 입력
    num = (title_num(input_code) - 1) # 웹툰 nums가 1부터 시작하는데 댓글 키워드는 0번부터 시작하기 때문에 맞춰줌
    token_list = WordPunctTokenizer().tokenize(vec_array_list[num]) # 댓글 키워드에서 특정 문자를 제거하기 위해 토크나이저
    sw = ['.', ',', "'"]# 특수 문자 삭제
    sw_removed = []
    for i in token_list:
        if i.lower() not in sw:
            sw_removed.append(i)
    vector_list, vector_pd = tfidf_list(vec_array_list, sw_removed) # 선택한 웹툰과 웹툰 전체의 키워드를 tfidf 리스트화
    find_num = cos_sim_index(vector_list, vector_pd, num) # 위에서 만든 tfidf 리스트를 통해 코사인 유사도를 측정.
    find_web_code = []
    if find_num == -1: # 유사도가 완전히 없는 웹툰의 경우 cos_sim 에서 -1을 return 하기로 했으므로 이렇게 작성. 
        return [] # 빈리스트 반환
    else: #그 외에는 멀쩡하므로 본래 리스트 제출
        for i in range(3):
            find_web_code += detail_data[detail_data['num'] == (find_num[i] + 1)].index.tolist()#알아낸 index로 웹툰 번호 확인.
    return find_web_code #웹툰 코드번호 반환



# res = main('739411')
# print(res)

def predict_func(wt_id):

    result = main(wt_id)

    return result