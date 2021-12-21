"""
1. 동적 크롤링을 이용해 매일의 코로나 확진자 수, 날씨,강수 확률, 초미세/미세먼지, 기온, 자외선
    등의 데이터를 가져오기
2. 자체 외출에 대한 판단 알고리즘을 이용해서 그날의 외출 판단하기: [최종판단]
3. 카카오 API를 이용하여 매일 그날의 외출 보고서 올라오도록 하기
"""


"""
***1. selenium 이용한 동적 크롤링***
"""
## selenium 없는 경우에는 kernel에서 설치
#pip install selenium


from selenium import webdriver

driver = webdriver.Chrome() # 웹 드라이버 연결
driver.implicitly_wait(1)  #wait time


driver.get('https:\\naver.com') # 웹사이트 이동
driver.implicitly_wait(1)
driver.maximize_window()

#코로나 확진자 수 가져오기
driver.find_element_by_id('query').send_keys("오늘 코로나 확진자 수")
driver.find_element_by_id('search_btn').click()
driver.implicitly_wait(3)

recent_day=[]   #최근 7일의 날짜
recent_confirmed_case=[] #최근 7일의 확진자 수
for i in range (1,8):
    year_path='//*[@id="target2"]/dl/div['+str(i)+']/dt'
    number_path='//*[@id="target2"]/dl/div['+str(i)+']/dd[1]/span'

    recent_day.append(driver.find_element_by_xpath(year_path).text)
    recent_confirmed_case.append(int(driver.find_element_by_xpath(number_path).text.replace(',','')))

## 오늘 날씨 데이터 가져오기(위치, 기온, 초미세먼지/미세먼지, 자외선)
driver.find_element_by_id('nx_query').clear()
driver.find_element_by_id('nx_query').send_keys("오늘의 날씨")
driver.find_element_by_class_name('bt_search').click()
driver.implicitly_wait(3)

# 현재 검색 위치
location=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[1]/div[1]/h2[2]').text

#현재 날씨
weather=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/p/span[2]').text

# 현재 기온
present_temp=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[2]/strong').text
present_temp[-2:]  

temp_arr=[]
for i in range(1,10):
    temp_path='//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/ul/li['+str(i)+']/dl/dd[2]/div/div/span'
    temp_arr.append(int(driver.find_element_by_xpath(temp_path).text.replace('\n°','')))

#강수 확률
rainfall_p=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/dl/dd[1]').text

# 초미세먼지/미세먼지 상태
fine_particle_status=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[3]/ul/li[1]/a/span').text
ultra_fine_particle_status=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[3]/ul/li[2]/a/span').text

# 자외선 상태
ultraviolet_status=driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div[3]/ul/li[3]/a/span').text


#브라우저 (드라이버) 종료
driver.close()

"""
***2. 오늘의 외출을 판단할 알고리즘 생성***
        -status_message (객관적인 메세지)
        -report_message (판단 메세지)
"""
#외출 관련 객관적인 데이터 보여주는 메세지
status_message=f"""[{location}]
오늘의 코로나 확진자 수는 {recent_confirmed_case[6]} 명 입니다.
오늘의 미세먼지/초미세먼지의 상태는 각각 {fine_particle_status}/{ultra_fine_particle_status} 입니다.
현재의 날씨는 {weather} 입니다.
현재의 강수 확률은 {rainfall_p} 입니다.
현재 기온은 {present_temp[-2:]}이고 외출기간 중 최고 기온은 {max(temp_arr)}°이고 최저 기온은 {min(temp_arr)}°입니다.
현재 자외선 상태는 {ultraviolet_status} 입니다."""
print(status_message)



##외출 관련 알고리즘 
report_message=""

#확진자 수 증감폭 & 미세먼지 상태로 추세 결정
dsum=0
for i in range(6):
    dsum+=recent_confirmed_case[i+1]-recent_confirmed_case[i]


if fine_particle_status=='좋음' or fine_particle_status=='보통':
    if dsum<0:
        report_message+="코로나 확진자 수는 감소추세이며 미세먼지도 좋은 편입니다.\n길게 외출하셔도 될 것 같습니다.\n"
    else:
        report_message+="코로나 확진자 수는 증가추세이지만 미세먼지는 좋은 편입니다.\n적당히 외출하셔야 할 것 같습니다.\n"
else:
    if dsum<0:
        report_message+="코로나 확진자 수는 감소추세이나 미세먼지는 나쁜 편입니다.\n적당히 외출하셔야 할 것 같습니다.\n"
    else:
        report_message+="코로나 확진자 수는 증가추세이고 미세먼지도 나쁜 편입니다.\n돌아다니지 않는 것을 추천 드립니다.\n"

# 강수 확률로 report 메세지
if int(rainfall_p.replace('%',''))<30:
    report_message+="비는 거의 안올테니 우산은 필요없습니다.\n"
elif int(rainfall_p.replace('%',''))<70:
    report_message+="비가 올 가능성이 있으니 우산을 챙겨주세요.\n"
else:
    report_message+="비가 올 가능성이 높으니 우산을 반드시 챙기길 바랍니다.\n"

# 평균온도로 report 메세지
avg_temp=0
for i in temp_arr:
    avg_temp+=i/len(temp_arr)

if avg_temp<0:
    report_message+="외출 기간 중 평균온도가 영하입니다.\n단단히 입고 가시는 것을 추천드립니다.\n"
elif avg_temp<10:
    report_message+="날씨가 상당히 추운 편입니다.\n따뜻하게 입고 나가시는 것을 추천드립니다.\n"
elif avg_temp<20:
    report_message+="선선한 날씨입니다! 즐거운 외출 되세요!\n"
else:
    report_message+="날씨가 상당히 추운 편입니다.\n따뜻하게 입고 나가시는 것을 추천드립니다.\n"
    
# 자외선 상태로 report 메세지
if ultraviolet_status=='좋음' or ultraviolet_status=='보통':
    report_message+="자외선이 약한 편입니다. 선크림은 필요 없을 것 같습니다.\n"
else:
    report_message+="자외선이 강한 편입니다. 선크림을 필수적으로 발라야 합니다.\n"

report_message+="즐거운 하루 되세요 ^-^"

print(report_message)




"""
***3. 카카오 API를 이용해서 메세지 보내기***
        - 로그인을 통해서 인가코드 얻기 (※로그인 시 2단계 인증 없어야 한다※)
        - 인가 코드를 통해서 토큰 얻기
        - 토큰을 이용해서 메세지 보내는 API
"""

## 카카오 서버로부터 인가 코드를 프로그램 돌릴 때마다 얻기
driver = webdriver.Chrome() 
driver.implicitly_wait(1)  

driver.get('https://kauth.kakao.com/oauth/authorize?client_id=a7bfc0bff193c398af55def6baab9011&redirect_uri=https://example.com/oauth&response_type=code&scope=talk_message') 
driver.implicitly_wait(2)
driver.maximize_window()

#카카오 계정 로그인(단, 로그인 하는 계정이 2단계 인증을 하지 않아야 한다)
driver.find_element_by_xpath('//*[@id="id_email_2"]').send_keys("")
driver.find_element_by_xpath('//*[@id="id_password_3"]').send_keys("")

driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()


# 처음 접근한 경우에는 try구문 이용 / 두 번째 이상 접근할 때는 예외처리
try:
    driver.find_element_by_xpath('//*[@id="line_ctr"]/label/span[1]').click()
    driver.find_element_by_xpath('//*[@id="acceptButton"]').click()
    text=driver.find_element_by_xpath('/html/body/div/h1').text
    print(text)

    current_url=driver.current_url
    i=current_url.index('=')
    CODE=current_url[i+1:]

    print(CODE)

    driver.close()
except :
    text=driver.find_element_by_xpath('/html/body/div/h1').text
    print(text)

    current_url=driver.current_url
    i=current_url.index('=')
    CODE=current_url[i+1:]
    print(CODE)

    driver.close()
    
    
# 라이브러리 호출
import requests
import json

## 인가 코드를 이용해서 토큰 얻기
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "a7bfc0bff193c398af55def6baab9011",
    "redirect_url" : "https://example.com/oauth",
    "code" : CODE
}
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)


## 토큰 이용해서 '나'에게 메세지 보내기(메시지 2개)
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers = {
    "Authorization": "Bearer " + tokens["access_token"]
}



data1 = {
    "template_object" : json.dumps({ "object_type" : "text",
                                      "text" : status_message,
                                      "link" : {
                                                  "web_url" : "https://www.naver.com",
                                                  "mobile_web_url" : "https://www.naver.com"
                                              },
                                      "button_title" :"추가 검색"
    })
}

response1 = requests.post(url, headers=headers, data=data1)
if response1.json().get('result_code') == 0:
    print('첫번째 메시지를 성공적으로 보냈습니다.')
else:
    print('두번째 메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response1.json()))

data2 = {
    "template_object" : json.dumps({ "object_type" : "text",
                                      "text" : report_message,
                                      "link" : {
                                                  "web_url" : "https://www.naver.com",
                                                  "mobile_web_url" : "https://www.naver.com"
                                              },
                                      "button_title" :"추가 검색"
    })
}

response2 = requests.post(url, headers=headers, data=data2)
if response2.json().get('result_code') == 0:
    print('두번째 메시지를 성공적으로 보냈습니다.')
else:
    print('두번째 메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response2.json()))










