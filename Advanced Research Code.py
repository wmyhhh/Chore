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
from collections import Counter

# 1. 设置浏览器选项
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--no-proxy-server")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. 读取CSV文件
input_file = "D:\Study\PRP\乳制品\检索\马奶csv.csv"
data = pd.read_csv(input_file)

# 添加一个新列，用于记录符合条件的内容
data['Search_Result'] = ""
data['Activity'] = ""

driver.get("http://www.cqudfbp.net/commonPages/advancedResearchInput.jsp")
print("网页已成功打开")

# 点击“Specific sequence”按钮
specific_sequence_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/center/div/form/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[7]"))
)
specific_sequence_button.click()
print("成功点击 'Specific sequence' 按钮")

# 点击“Check All”按钮
check_all_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='checkAll']"))
)
check_all_button.click()
print("成功点击 'Check All' 按钮")

# 遍历表格的每一行
for index, row in data.iterrows():  
    search_value = row['Peptide']  # 替换为实际的列名称
    print(f"\n正在处理第 {index + 1} 行数据: {search_value}")

    try:
        # 尝试5次输入和获取搜索结果
        results = []  # 用于存储五次检索结果
        for attempt in range(5):
            # 找到“Search value:”输入框并输入搜索内容
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='enterValue']"))
            )
            search_box.clear()
            search_box.send_keys(search_value)
            print(f"尝试 {attempt + 1}: 成功找到并填写了 'Search value:' 输入框")

            # 点击“Submit”按钮
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/center/div/form/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/button"))
            )
            submit_button.click()
            print("成功点击 'Submit' 按钮")

            # 等待搜索结果
            try:
                search_results_text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="filterDiv"]/center/div/div/strong'))
                ).text
                
                # 获取结果计数
                result_count = int(search_results_text.split("Search Results:")[1].split()[0])
                print(f"尝试 {attempt + 1}: 搜索结果已加载，结果计数为: {result_count}")
                results.append(result_count)  # 将结果存储到列表中
            except StaleElementReferenceException:
                print("检测到过时元素引用，重试获取搜索结果...")
                time.sleep(1)  # 等待1秒后重试
            except TimeoutException:
                print("等待搜索结果超时，检查页面状态...")

        # 检查是否有至少3次检索结果相同
        result_counts = Counter(results)
        most_common_result, most_common_count = result_counts.most_common(1)[0]

        if most_common_count >= 3:  # 至少3次相同
            data.at[index, 'Search_Result'] = most_common_result  # 记录相同的结果到 DataFrame
            print(f"第 {index + 1} 行的搜索结果已成功记录: {most_common_result}")
            
            # 检查是否有活性结果
            if most_common_result != 0:
                cnt = 0
                activity = ''
                x = 2  # 从表格的第2行开始遍历

                while cnt < most_common_result:
                    # 格式化 XPATH 字符串并查找元素
                    for retry in range(3):  # 重试机制
                        try:
                            activity_number = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, f'//*[@id="filterDiv"]/center/div/table/tbody/tr[{x}]/td[3]'))
                            ).text
                            num = int(activity_number)
                            if num != 0:
                                activity_content = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, f'//*[@id="filterDiv"]/center/div/table/tbody/tr[{x}]/td[2]'))
                                ).text
                                activity += activity_content + ", "  # 将活性信息添加到字符串中
                                cnt += num
                            x += 1  # 移动到下一行
                            break
                        except StaleElementReferenceException:
                            print("检测到过时元素引用，重试活性信息获取...")
                            time.sleep(1)
                data.at[index, 'Activity'] = activity.strip(', ')  # 去掉末尾的逗号和空格
                print(f"已记录活性: {activity.strip(', ')}")  # 输出活性信息
        else:
            print(f"第 {index + 1} 行的搜索结果不一致，未记录结果。")

    except TimeoutException:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 未能成功找到元素，请检查元素选择器或网络状态。")
    except NoSuchElementException:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 找不到所需元素。")
    except Exception as e:
        print(f"第 {index + 1} 行的搜索内容 '{search_value}' 发生错误: {str(e)}")

# 关闭浏览器
driver.quit()


# 4. 将结果保存到新CSV文件
output_file = "D:\\Study\\PRP\\乳制品\\检索\\马奶csv_output.csv"
data.to_csv(output_file, index=False, encoding='utf-8-sig')

print("\n流程完成，结果已保存至:", output_file)
