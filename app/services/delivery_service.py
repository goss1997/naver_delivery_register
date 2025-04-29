from utils.driver import make_driver
from utils.utils import random_wait, element_typer, element_random_click, clear_cookies_contents
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def register_delivery(data):
    driver = None
    try:
        driver = make_driver()
        driver.get("https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback")
        random_wait()

        # 로그인
        element_typer(driver, "input[placeholder='아이디 또는 이메일 주소']", data.login_id)
        random_wait()
        element_typer(driver, "input[placeholder='비밀번호']", data.login_pw)
        login_button = driver.find_element(By.CSS_SELECTOR, "div.Login_btn_box__fgb5v button")
        element_random_click(driver, login_button)
        random_wait()

        # 모달 닫기
        modal_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[uib-modal-window='modal-window'] button.term-agreement-modal-close"))
        )
        element_random_click(driver, modal_close_button)
        random_wait()

        # 판매자 정보 탭 클릭
        seller_info_tab = driver.find_element(By.XPATH, "//ul[@role='menu']//li//a[normalize-space(text())='판매자 정보']")
        element_random_click(driver, seller_info_tab)
        random_wait()

        # 판매자 정보 클릭
        seller_info_link = driver.find_element(By.XPATH, "//ul//a[@href='#/seller/info']")
        element_random_click(driver, seller_info_link)
        random_wait()

        # 택배사 계약정보 확인 버튼 클릭
        delivery_check_button = driver.find_element(By.XPATH, "//button[contains(text(), '택배사 계약정보 확인')]")
        element_random_click(driver, delivery_check_button)
        random_wait()

        # 새 창 전환
        first_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        for handle in driver.window_handles:
            if handle != first_window:
                driver.switch_to.window(handle)
                break

        # 택배사 등록 버튼 클릭
        register_delivery_link = driver.find_element(By.XPATH, "//a[@href='#' and contains(text(), '택배사 등록')]")
        element_random_click(driver, register_delivery_link)
        random_wait()

        # 다시 새 창 전환
        second_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 2)
        for handle in driver.window_handles:
            if handle != first_window and handle != second_window:
                driver.switch_to.window(handle)
                break

        def clear_and_input(selector, value):
            element = driver.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(value)

        random_wait()

        # 기본정보 입력
        clear_and_input("input[name='mallName']", data.mall_name)
        clear_and_input("input[name='mallUserName']", data.manager_name)
        clear_and_input("input[name='mallUserTel1']", data.phone_number)

        random_wait()

        # 배송사 계약정보 입력
        delivery_company_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='transCode']"))
        )
        Select(delivery_company_select).select_by_visible_text(data.delivery_company)
        clear_and_input("input[name='bizNo']", data.biz_number)
        clear_and_input("input[name='contractNo']", data.contract_number)

        random_wait()

        # 계약코드 확인 버튼 클릭
        check_btn = driver.find_element(By.XPATH, "//button[text()='확인' and @type='button']")
        element_random_click(driver, check_btn)
        random_wait()

        # 계약 코드 결과 확인
        modal_selector = driver.find_element(By.TAG_NAME, "ngb-modal-window")
        if any(text in modal_selector.text for text in ["계약코드에 실패", "사용불가 계약코드"]):
            return False, "계약확인 실패"
        if any(text in modal_selector.text for text in ["계약코드 확인이 완료", "사용가능 계약코드"]):
            print("계약확인 성공")

        # 모달 닫기
        modal_check_btn = modal_selector.find_element(By.XPATH, "//button[text()='확인' and @type='button']")
        element_random_click(driver, modal_check_btn)
        random_wait()

        # 발송지 정보 입력
        clear_and_input("input[name='name']", data.origin_name)
        clear_and_input("input[name='centerZipCode']", data.origin_zipcode)
        clear_and_input("input[name='centerAddr1']", data.origin_address1)
        clear_and_input("input[name='centerAddr2']", data.origin_address2)
        clear_and_input("input[name='centerTel1']", data.origin_phone)

        random_wait()

        # 계약요금 정보 입력
        settlement_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='transFareViewStatus']"))
        )
        Select(settlement_select).select_by_visible_text(" 신용(월정산) ")

        s_div = driver.find_element(By.XPATH, "//div[@class='row box-fare-grid-outline mb-2 py-1' and contains(text(), 'S')]")
        inputs = s_div.find_elements(By.TAG_NAME, "input")
        if len(inputs) >= 3:
            inputs[0].clear()
            inputs[0].send_keys("2200")
            inputs[1].clear()
            inputs[1].send_keys("2200")
            inputs[2].clear()
            inputs[2].send_keys("2500")

        random_wait()

        # 저장 버튼 클릭
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), '저장')]")
        element_random_click(driver, submit_button)
        random_wait()

        return True, "택배사 등록 완료"

    except Exception as e:
        print(f"에러 발생: {e}")
        return False, f"택배사 등록 실패: {str(e)}"

    finally:
        if driver:
            driver.quit()
        time.sleep(3)    
        clear_cookies_contents()