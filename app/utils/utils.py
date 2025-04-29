import os
import random
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

def scroll_down(driver, scroll_pause=0.5, max_scrolls=10):
    """
    페이지를 아래로 여러 번 스크롤하여 동적 콘텐츠 로드를 유도합니다.
    
    :param driver: Selenium WebDriver
    :param scroll_pause: 스크롤 간 대기 시간 (초)
    :param max_scrolls: 최대 스크롤 횟수
    """
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(scroll_pause)

def normalize_price(raw_text) -> int:
    """
    가격 문자열을 정수형으로 정규화합니다.
    - "할인 전 판매가45,000원" → 45000
    - 쉼표(,) 및 원 등 문자 제거
    - 숫자형(int/float) 입력도 처리
    """
    if isinstance(raw_text, (int, float)):
        return int(raw_text)

    if isinstance(raw_text, str):
        # 문자열에서 첫 번째 숫자 그룹 추출 (예: 45,000)
        match = re.search(r"(\d[\d,]*)", raw_text)
        if match:
            numeric = match.group(1).replace(",", "")
            return int(numeric)
        else:
            raise ValueError(f"가격 문자열에서 숫자를 추출할 수 없습니다: {raw_text}")

    raise ValueError(f"지원하지 않는 가격 타입: {type(raw_text)}")

def random_wait():
    t = random.uniform(1,3)
    time.sleep(t)
def element_typer(driver, selector,sentence):
    element = driver.find_element(By.CSS_SELECTOR,selector)
    for i in range(len(sentence)):
        element.send_keys(sentence[i])
        t = random.uniform(0.15,0.25)
        time.sleep(t)

# 1. UI의 정 가운데 부분을 클릭함
# 2. 현재 화면에 안 보이는 요소도 클릭할수있음.
def element_random_click(driver,element):
    el_width, el_height = element.size['width'], element.size['height']
    targetX = random.randint( -int(el_width * 0.4), int(el_width*0.4) )
    targetY = random.randint( -int(el_height *0.4), int(el_height*0.4))

    ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX,targetY).click().perform()

def random_click(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
     
    el_width, el_height = element.size['width'], element.size['height']
    targetX = random.randint( -int(el_width * 0.4), int(el_width*0.4) )
    targetY = random.randint( -int(el_height *0.4), int(el_height*0.4))

    ActionChains(driver).move_to_element(element).pause(2).move_by_offset(targetX,targetY).click().perform()


# 엘리먼트가 스크린 안에 있는지 확인하는 함수 
# return Bool [ True, False ] 

def is_element_in_screen_bound(driver, element_selector="",element=None):

    cur_window = driver.get_window_size()
    
    screen_height = int(cur_window['height'])
    cur_scrollY = driver.execute_script("return window.scrollY")
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height= int(element.size['height'])

    # print(f"cur_scrollY : {cur_scrollY} , element_y : {element_y}, element_height : {element_height}")
    
    if cur_scrollY + screen_height < element_y + element_height + 150:
        return False
    if cur_scrollY > element_y - 120:
        return False
    return True


# 랜덤 패턴 가지고오기
def get_random_pattern():
    ret_pattern = []
    # PC 패턴 
    with open("./pc_scroll.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            ret_pattern.append(line.rstrip())
    pc_scroll_px = 114 # 100, 114    
    selected_pattern = random.choice(ret_pattern)
    _,dx,dy,delay = selected_pattern.split("#")
    if float(delay) < 0.25:
        return get_random_pattern()
    return int(dx),int(pc_scroll_px), float(delay)

# 스크린 화면 안으로 Element를 위치시키는 함수
def move_to_bottom(driver):
    sx = random.randrange(100,270)
    sy = random.randrange(250,500)
    randY = random.randrange(13000,15000)
    ActionChains(driver).scroll_by_amount(0, randY).perform()
def random_move(driver,direction="down",count=1):
    for _ in range(count):
        # [O] 사람패턴 ~ 사람이 얼마나 스크롤을 움직였는지
        # randY = random.randrange(200,300)
        randX,randY,_delay = get_random_pattern()
        sx = random.randrange(100,270)
        sy = random.randrange(250,500)

        if direction == "up":
            randY = -randY

        if random.random()  > 0.9 : #10%의 확률로
            randY = -randY

        print(f"Scroll 한다 {randY}")
        ActionChains(driver).scroll_by_amount(0, randY).perform()

        # [O] 사람패턴 ~ 스크롤 하는 텀
        prob = random.random()
        if prob < 0.5:
            dt  = random.uniform(_delay*0.1, _delay*0.3)
        elif prob < 0.8:
            dt = random.uniform(_delay*0.2, _delay*0.6)
        else:
            dt = random.uniform(_delay*0.5, _delay*1.2)

        time.sleep(dt)
        time.sleep( 0.5)
def scroll_to_element(driver, element_selector="",element=None):
    if element == None:
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
    element_y = int(element.location['y'])
    element_height = int(element.size['height'])

    while not is_element_in_screen_bound(driver, element_selector,element):        
        cur_window = driver.get_window_size()
        screen_height = int(cur_window['height'])
        cur_scrollY = int(driver.execute_script('return window.scrollY'))

        if cur_scrollY + screen_height < element_y + element_height + 150:
            random_move(driver, direction="up")
        elif cur_scrollY > element_y - 120:
            random_move(driver, direction="down")
def part_int(n,k):
    def _part(n, k, pre):
        if n <= 0:
            return []
        if k == 1:
            if n <= pre:
                return [[n]]
            return []
        ret = []
        for i in range(min(pre,n), 0 , -1):
            ret += [[i]+sub for sub in _part(n-i,k-1,i)]
        return ret
    return _part(n,k,n)
def random_scroll_with_wait(driver,minutes=3):
    for _ in range(minutes):
        print(_, ' 분째 대기중')
        wait_times = random.choice(part_int(60,6))
        print(wait_times)
        # wait_times : [10,9,11,10,9,11]
        for wait_second in wait_times:
            if random.random() < 0.85:
                randY = random.randrange(400,750)
            else:
                randY = random.randrange(1000,1400)
            
            if random.random() < 0.06:
                randY = - randY

            sx = random.randrange(100,270)
            sy = random.randrange(250,500)
            ActionChains(driver).scroll_by_amount(0, randY).perform()

            print(f"     - {wait_second} 초 대기중 // {randY}")
            time.sleep(wait_second)
            
def clear_cookies_contents(path="cookies"):
    """
    지정된 cookies 디렉토리 내부의 모든 파일과 서브 디렉토리를 삭제합니다.
    단, cookies 디렉토리 자체는 삭제하지 않습니다.
    :param path: 기본값은 'cookies' 폴더
    """
    if not os.path.exists(path):
        print(f"❗ 경로가 존재하지 않습니다: {path}")
        return

    # 하위 디렉토리부터 탐색하여 파일 및 디렉토리 삭제
    for root, dirs, files in os.walk(path, topdown=False):
        # 파일 삭제
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"⚠️ 삭제 실패: {file_path} | {e}")
        # 빈 디렉토리 삭제
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
            except Exception as e:
                print(f"⚠️ 삭제 실패: {dir_path} | {e}")
