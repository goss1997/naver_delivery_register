import os
import random
from user_agents import parse
import undetected_chromedriver as uc


def make_user_agent(ua,is_mobile):
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    print(platform)
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture= ""
    else: # Window
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion" : ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform" : f"{platform_info}",
        "acceptLanguage" : "ko-KR, kr, en-US, en",
        "userAgentData":{
            "brands" : [
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not A;Brand", "version":"99"},
            ],
            "fullVersionList":[
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not:A-Brand", "version":"99"},
            ],
            "fullVersion":f"{ua_full_version}",
            "platform" :platform,
            "platformVersion":platform_version,
            "architecture":architecture,
            "model" : model,
            "mobile":is_mobile #True, False
        }
    }
    return RET_USER_AGENT

def make_driver():
    try:
        pc_device = ["1920,1440","1920,1200","1920,1080","1600,1200","1600,900",
                        "1536,864", "1440,1080","1440,900","1360,768"
                ]

        mo_device = [
                    "360,640", "360,740", "375,667", "375,812", "412,732", "412,846",
                    "412,869", "412,892", "412,915"
                ]

        width,height = random.choice(pc_device).split(",")

        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
     
        options = uc.ChromeOptions()

        # 랜덤쿠키 생성하기 undetected_chromedriver 버전
        # 1, 100의 숫자이름 폴더 밑에 쿠키를 생성해서 저장하겠다.
        rand_user_folder = random.randrange(1,100)
        if os.path.exists("./cookies/") == False:
            os.mkdir("./cookies/")
        userCookieDir = os.path.abspath(f"./cookies/{rand_user_folder}")
        if os.path.exists(userCookieDir) == False:
                print(f'Create {rand_user_folder} Cookie Folder')
                os.mkdir(userCookieDir)

        # User Agent 속이기
        options.add_argument(f'--user-agent={UA}')
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        options.add_argument('--disable-logging')
        options.add_argument("--start-maximized")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors=yes')
        
        driver = uc.Chrome(user_data_dir=userCookieDir,options=options)

        UA_Data = make_user_agent(UA,False)
        driver.execute_cdp_cmd("Network.setUserAgentOverride",UA_Data)

        # User Agent 적용
        driver.execute_cdp_cmd("Emulation.setUserAgentOverride",UA_Data)
        print(width,height)
        driver.set_window_size(int(width),int(height))
        
        return driver
    except Exception as e:
        print(e)
        driver = None
        return driver