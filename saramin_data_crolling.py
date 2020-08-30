'''
(author) Jang HS
(version) 1.0, 초기 버전
(date) 20200830
'''

# ==========================================================
# 0. Package Load
# ==========================================================
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from tqdm import tqdm
import sys  
import time
import random
import csv
import pandas as pd

# ==========================================================
# 1. 필수 입력
# ==========================================================

# [지역 선택] 전국 / 서울, 경기, 인천, 부산, 대구, 광주, 대전, 울산, 세종, 강원, 경남, 경북, 전남, 전북, 충북, 제주
# 입력 예시 ['서울', '경기'] ['전국'] ['대구', '부산']
area_select = ['서울', '경기']

# [검색어] 코드 실행시 입력
search_word = input("검색어를 입력하세요 : ")
search_word = str(search_word)

# [채용 정보] 일반 채용정보 / 파견.대행 / 헤드헌팅 중 선택하는 경우를 리스트로 받음 (최소 1개 이상 선택)
# 일반 채용정보, 파견.대행 선택시 ['Y', 'Y', 'N']
cha = ['Y', 'Y', 'N']

# [정렬 순서] 1 관련도 / 2 정확도/ 3 등록일 / 4 수정일 / 5 마감일 / 6 지원자 / 7 사원수
orderby = 2

# ==========================================================
# 2. webdriver 실행, 검색어 입력
# ==========================================================
driver = webdriver.Chrome(executable_path=r'/Users/hyeseon/Documents/chromedriver')
driver.get("https://www.saramin.co.kr/zf_user/")

#검색창 clear
elem = driver.find_element_by_id('ipt_keyword_recruit')
elem.clear()

#검색어 입력
elem.send_keys(search_word)

# 검색클릭
elem = driver.find_element_by_id("btn_search_recruit")
elem.click()

time.sleep(random.randint(0, 1))

# ==== 정렬 순서
# 정렬 순서 열기
driver.implicitly_wait(5)
elem = driver.find_element_by_xpath('//*[@id="recruit_info"]/div[2]/div/div[2]/button')
elem.click()

# 정렬 순서
order_xpath = '//*[@id="recruit_info"]/div[2]/div/div[2]/div/ul/li[{}]/button'.format(str(orderby))

# 정렬 순서 클릭
elem = driver.find_element_by_xpath(order_xpath)
driver.execute_script("arguments[0].click();", elem)
# elem.click()




# ==========================================================
# 3. 게시물 100개 선택 / 지역 선택
# ==========================================================

# 채용정보 더보기 후 첫페이지로 이동
elem = driver.find_element_by_xpath('//*[@id="recruit_info_list"]/div[2]/div/a')
driver.execute_script("arguments[0].click();", elem)
# elem.click()

elem = driver.find_element_by_xpath('//*[@id="recruit_info_list"]/div[2]/div/a[1]')
driver.execute_script("arguments[0].click();", elem)
# elem.click()
driver.execute_script("window.scrollTo(0, 0);") # 오류 방지를 위한 페이지 상단으로 이동


# 처음 100개를 받아오기
time.sleep(random.randint(0, 1))
elem = driver.find_element_by_xpath("//*[@id='recruit_info']/div[2]/div/div[3]/button")
driver.execute_script("arguments[0].click();", elem)
# elem.click()

elem = driver.find_element_by_xpath("//*[contains(text(), '100개씩')]")
driver.execute_script("arguments[0].click();", elem)
# elem.click()

driver.implicitly_wait(3)
area_path_table = pd.read_csv('area_path_table.csv')
area_path_table['selected']  = area_path_table['area'].map(lambda x : 1 if '전국' in area_select else 1 if x in area_select else 0)
area_path_table

# 지역 선택 
driver.execute_script("window.scrollTo(0, 0);") # 오류 방지를 위한 페이지 상단으로 이동
elem = driver.find_element_by_xpath('//*[@id="sp_main_wrapper"]/div[2]/ul/li[2]/button')
elem.click()
driver.implicitly_wait(5)



# 선택된 지역 기준으로 채용 공고를 선택하게 만들기.
area_list = list(area_path_table[area_path_table['selected']==1]['xpath'])


if '전국' in area_select :
    print("선택 지역: 전국")

else :
    print("선택 지역: {}".format(str(area_select)))
    for area in area_list:

        driver.implicitly_wait(10)
        elem = driver.find_element_by_xpath(area+'/button')
        driver.execute_script("arguments[0].click();", elem)
        # elem.click()

# ==========================================================
# 4. 조건에 따른 채용 정보 선택
# ==========================================================
 
# 휴식 및 페이지 상단으로 이동    
driver.implicitly_wait(3)
driver.execute_script("window.scrollTo(0, 0);")

# 일반 채용정보 / 파견.대행 / 헤드헌팅 중 선택
# 전체 채용 정보일 경우 pass로
if cha == ['Y', 'Y', 'Y'] :
    pass
else :
    # 최소한 하나 이상의 채용 조건을 선택해야 함
    if cha[0] + cha[1] + cha[2] == 'NNN' : 
        print('error')

    # 일반 채용정보 선택 해제 
    elem = driver.execute_script("window.scrollTo(0, 0);")
    if cha[0] != 'Y' :
        elem = driver.find_element_by_xpath('//*[@id="recruit_info"]/div[1]/div/div[1]')
        driver.execute_script("arguments[0].click();", elem)

    elem = driver.execute_script("window.scrollTo(0, 0);")
    if cha[1] != 'Y' :
        elem = driver.find_element_by_xpath('//*[@id="recruit_info"]/div[1]/div/div[2]')
        driver.execute_script("arguments[0].click();", elem)

    elem = driver.execute_script("window.scrollTo(0, 0);")
    if cha[2] != 'Y' :
        elem = driver.find_element_by_xpath('//*[@id="recruit_info"]/div[1]/div/div[3]')
        driver.execute_script("arguments[0].click();", elem)



# ==========================================================
# 5. 채용 공고 크롤링
# ==========================================================
 


full_dataset = pd.DataFrame(columns = ['title', 'title_link', 'end_date', 'text_info','work_keyword','office_name'])

time.sleep(7)

# 채용공고 수집 시작
for item_num in tqdm(range(1,101)):
    try : 
        # 공고 제목 데이터 선택
        path_ = '//*[@id="recruit_info_list"]/div[1]/div[{}]'.format(str(item_num))
        
        # 공고명
        title = driver.find_element_by_xpath(path_ +'/div[1]/h2/a').get_attribute("title")

        # 공고링크
        title_link = driver.find_element_by_xpath(path_ +'/div[1]/h2/a').get_attribute("href")

        driver.implicitly_wait(10)
        # 공고 마감일
        end_date = driver.find_element_by_xpath(path_+'/div[1]/div[2]/span').text
        
        # 공고 지역\n경력\n학력\n직업 종류 + 연봉 있는경우
        text_info = driver.find_element_by_xpath(path_+'/div[1]/div[3]').text

        # 업종 ' 전까지는 업종 키워드
        work_keyword = driver.find_element_by_xpath(path_+'/div[1]/div[4]')
        work_keyword = work_keyword.text

        # 기업명 text
        office_name = driver.find_element_by_xpath(path_+'/div[2]/strong/a').get_attribute("title")
        if len(office_name) == 0 :
            office_name = driver.find_element_by_xpath(path_+'/div[2]/strong/a/span').text

        temp_dataset = pd.DataFrame({'title':[title], 'title_link':[title_link], 'end_date':[end_date], 'text_info':[text_info],'work_keyword':[work_keyword],'office_name':[office_name]})
        
        full_dataset = pd.concat([full_dataset, temp_dataset], axis = 0)
    
    except : print("no content in item no {}".str(item_num)) 

time.sleep(random.randint(0, 1))
full_dataset = full_dataset.reset_index(drop=True)
full_dataset.head()

# webdriver 닫기
driver.quit()

# ==========================================================
# 6. 수집 데이터 전처리 및 저장
# ==========================================================
 
# 날짜 포맷을 맞추기
from datetime import datetime,timedelta

end_date_after = []
for row_num in range(len(full_dataset)):
    end_date_before = full_dataset['end_date'][row_num]
    
    # 오늘
    if '오늘' in end_date_before:
        end_date_after.append(datetime.today().strftime("%Y/%m/%d"))
    elif '내일' in end_date_before:
        end_date_after.append((datetime.today() + timedelta(1)).strftime("%Y/%m/%d"))
    elif '상시' in end_date_before:
        end_date_after.append('상시')
    elif '채용시'  in end_date_before:
        end_date_after.append('채용시')

    elif '~' in end_date_before:
        year = datetime.today().year
        month = full_dataset['end_date'][row_num][2:4]
        day = full_dataset['end_date'][row_num][5:7]
        date_after = str(year)+str(month)+str(day)
        end_date_after.append(pd.to_datetime(date_after).strftime("%Y/%m/%d"))
    
    else : end_date_after.append(str(end_date_before))
        

full_dataset['end_date'] = end_date_after
full_dataset.head()

# 지역 / 경력 / 학력 / 검색 키워드 column 생성
area =[]
level = []
school = []
keyword = []
for row_num in range(len(full_dataset)):
    area_ = full_dataset['text_info'][row_num].split(sep='\n')[0]
    level_ = full_dataset['text_info'][row_num].split(sep='\n')[1]
    school_ =full_dataset['text_info'][row_num].split(sep='\n')[2]
    keyword_ = full_dataset['work_keyword'][row_num].split(sep="'")[0].strip()
    
    area.append(area_)
    level.append(level_)
    school.append(school_)
    keyword.append(keyword_)


full_dataset['area']= area
full_dataset['level']= level
full_dataset['school']= school
full_dataset['keyword']= keyword

full_dataset = full_dataset.drop(['text_info','work_keyword'],axis=1)



# csv형태로 저장
full_dataset = full_dataset[['title','title_link','area','level','school','end_date','office_name','keyword']]
full_dataset.to_csv('saramin_crolling.csv',encoding='euckr')
