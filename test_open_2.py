from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# ====== 啟動 Chrome ======
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("http://172.17.21.19:8050/new")
print("成功打開瀏覽器！")
time.sleep(5)  # 等網頁先載入

# ====== 登入 ======
username_input = driver.find_element(By.ID, "usernameBox")
password_input = driver.find_element(By.ID, "passwordBox")
username_input.send_keys("Ann.Tseng")
password_input.send_keys("Ann861208!")

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "loginButton"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
try:
    login_button.click()
except:
    print("登入按鈕點擊被攔截，可能已經登入。")

# 等待頁面渲染完成（可改成特定元素確認）
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
print("登入後網頁已載入！")


# ====== Mantine 下拉選單函式 ======
# ===== Mantine 下拉選單固定版本 =====
def select_mantine_dropdown(driver, input_id, value):
    print(f"準備選 {value} 在 {input_id} ...")

    # 1️⃣ 點擊 input 展開下拉
    input_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, input_id))
    )
    input_box.click()
    time.sleep(1)  # 等下拉選單渲染

    # 2️⃣ 找 listbox container
    listbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']"))
    )

    # 3️⃣ 找目標選項
    options = listbox.find_elements(By.XPATH, ".//div[@role='option']")
    target_option = None
    for opt in options:
        if opt.text.strip() == value:
            target_option = opt
            break

    if target_option:
        # 4️⃣ 只滾動下拉框本身，而不滾動整個頁面
        driver.execute_script("""
            arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;
        """, listbox, target_option)

        # 5️⃣ 點選目標
        ActionChains(driver).move_to_element(target_option).click().perform()
        print(f"✅ 成功選擇 {value}")
        time.sleep(0.5)
    else:
        print(f"❌ 找不到選項 {value}")

# ====== 使用函式選擇兩個下拉選單 ======
select_mantine_dropdown(driver, "system_name_input", "DQA")
select_mantine_dropdown(driver, "model_name_input", "BIOS自動化專案")
select_mantine_dropdown(driver, "stage_input", "Plan")
select_mantine_dropdown(driver, "task_input", "Plan")

# 找到輸入框
work_hours_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "work_hours_input"))
)

work_hours_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "work_hours_input"))
)

# 改值並觸發 input 事件
# 找到加號按鈕
increase_button = driver.find_element(By.CSS_SELECTOR, "#work_hours_input ~ div button.mantine-NumberInput-controlUp")
decrease_button = driver.find_element(By.CSS_SELECTOR, "#work_hours_input ~ div button.mantine-NumberInput-controlDown")
work_hours = 1
if work_hours * 1.0 > 1.0:
    work_hours -= 1
    for _ in range(int(work_hours * 2)):
        increase_button.click()
elif work_hours < 1.0:
    work_hours = 1 - work_hours
    for _ in range(int(work_hours * 2)):
        decrease_button.click()

# 假設目前值是 1.0，想增加

# for _ in range(4):
#     increase_button.click()
# # 減少
# for _ in range(2):
#     decrease_button.click()
# 等前端更新
print("所有選單選擇完成！")
time.sleep(60)  # 保持瀏覽器開啟