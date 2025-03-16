import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. 设置浏览器选项
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--no-proxy-server")
#options.add_argument("incognito")  # 隐私模式
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. 读取CSV文件
input_file = "D:\Study\PRP\乳制品\检索\马奶csv.csv"
data = pd.read_csv(input_file)

# 添加新列，用于记录符合条件的内容
data['Search_Result'] = ""
data['Activity'] = ""
driver.get("https://biochemia.uwm.edu.pl/en/biopep-uwm-2/")
print("网页已成功打开")

# 等待页面完全加载
WebDriverWait(driver, 30).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)
print('页面已完全加载')

# 等待 iframe 加载完成
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "biopep"))
)

# 切换到 iframe
driver.switch_to.frame("biopep")

# 查找并点击按钮
peptide_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[4]/td/button"))
)
peptide_button.click()

# 遍历表格的每一行
for index, row in data.iterrows():
    search_value = row['Peptide']  # 替换为实际的列名称
    print(f"\n正在处理第 {index + 1} 行数据: {search_value}")

    try:
        # 输入搜索内容
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form[3]/table/tbody/tr/td[2]/input"))
        )
        search_box.clear()
        search_box.send_keys(search_value)
        print("成功找到并填写了 'Search value:' 输入框")

        # 选择“Sequence”
        sequence_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form[3]/table/tbody/tr/td[4]/select/option[5]"))
        )
        sequence_button.click()

        # 选择“Exact”
        exact_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form[3]/table/tbody/tr/td[6]/input"))
        )
        exact_button.click()

        # 点击“Go”按钮
        go_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form[3]/table/tbody/tr/td[5]/input"))
        )
        go_button.click()
        print("成功点击 'Go' 按钮")

        # 获取搜索结果
        try:
            search_results_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[1]/td/span'))
            ).text
            result_count = int(search_results_text)
            print(f"搜索结果已加载，结果计数为: {result_count}")

            # 将结果记录到 DataFrame
            data.at[index, 'Search_Result'] = result_count
            if result_count > 0:
                activity = ''
                for i in range(result_count):
                    # 获取每个搜索结果的详细信息
                    result_details = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'/html/body/table/tbody/tr[{i + 3}]/td[7]'))
                    )
                    activity += str(result_details.text) + ", "  # 使用 result_details.text 获取文本内容

                data.at[index, 'Activity'] = activity.strip(', ')  # 去掉末尾的逗号和空格
                print(f"已记录活性: {activity.strip(', ')}")  # 输出活性信息

        except (StaleElementReferenceException, TimeoutException):
            print("元素可能过期或页面未加载，无法获取搜索结果")

        print(f"第 {index + 1} 行的搜索结果已成功记录: {result_count}")

        # 点击“Back”按钮，返回主页面
        back_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/a"))
        )
        back_button.click()

    except TimeoutException:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 超时，请检查元素选择器或网络状态。")
    except NoSuchElementException:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 找不到元素。")
    except Exception as e:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 发生错误: {str(e)}")

# 关闭浏览器
driver.quit()


# 4. 将结果保存到新CSV文件
output_file = "D:\\Study\\PRP\\乳制品\\检索\\马奶csv_output02.csv"
data.to_csv(output_file, index=False, encoding='utf-8-sig')

print("\n流程完成，结果已保存至:", output_file)
