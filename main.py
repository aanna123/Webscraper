from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

CHROMEDRIVER_PATH = r"C:\AP\python\chromedriver-win64\chromedriver.exe"
PROJECT_LIST_URL = 'https://rera.odisha.gov.in/projects/project-list'

options = Options()
# options.add_argument("--headless")  # Uncomment if you want no browser window

driver = webdriver.Chrome(service=ChromeService(CHROMEDRIVER_PATH), options=options)
wait = WebDriverWait(driver, 20)

driver.get(PROJECT_LIST_URL)

def safe_get_text(by, locator):
    try:
        elem = wait.until(EC.presence_of_element_located((by, locator)))
        return elem.text.strip()
    except:
        return ""

def close_popup_if_any():
    try:
        popup = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-popup.swal2-modal"))
        )
        close_btn = popup.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        close_btn.click()
        time.sleep(1)
        print("Popup detected and closed.")
    except TimeoutException:
        pass
    except Exception as e:
        print(f"Error closing popup: {e}")

# Collect data here
project_data = []

for idx in range(6):
    print(f"Processing project #{idx+1}")

    try:
        # Reload main project list page fresh for stability
        driver.get(PROJECT_LIST_URL)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary")))
        time.sleep(1)

        buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-primary")

        if idx >= len(buttons):
            print(f"No button for project #{idx+1}, skipping.")
            continue

        btn = buttons[idx]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(1)
        btn.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-project-overview")))
        time.sleep(1)

        project_name = safe_get_text(By.XPATH, "//div[contains(@class,'details-project')][label[text()='Project Name']]/strong")
        rera_regd_no = safe_get_text(By.XPATH, "//div[contains(@class,'details-project')][label[text()='RERA Regd. No.']]/strong")

        close_popup_if_any()

        promoter_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Promoter Details')]")))
        promoter_tab.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "app-promoter-details")))
        time.sleep(1)

        promoter_container = driver.find_element(By.CSS_SELECTOR, "app-promoter-details")

        # Promoter name and address using fixed index approach
        strong_elements = promoter_container.find_elements(By.TAG_NAME, "strong")
        promoter_name = strong_elements[0].text.strip() if len(strong_elements) > 0 else ""
        promoter_address = strong_elements[3].text.strip() if len(strong_elements) > 3 else ""

        # Dynamic GST extraction
        gst_no = ""
        try:
            labels = promoter_container.find_elements(By.TAG_NAME, "label")
            for label in labels:
                if "gst" in label.text.strip().lower():
                    gst_no_elem = label.find_element(By.XPATH, "following-sibling::strong")
                    gst_no = gst_no_elem.text.strip()
                    break
        except Exception:
            gst_no = ""

        print(f"Rera Regd. No: {rera_regd_no}")
        print(f"Project Name: {project_name}")
        print(f"Promoter Name: {promoter_name}")
        print(f"Promoter Address: {promoter_address}")
        print(f"GST No: {gst_no}\n")

        project_data.append({
            "RERA Regd. No": rera_regd_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Promoter Address": promoter_address,
            "GST No": gst_no
        })

    except Exception as e:
        print(f"Error processing project #{idx+1}: {e}")

driver.quit()

# Save to CSV
csv_file = "rera_project_data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["RERA Regd. No", "Project Name", "Promoter Name", "Promoter Address", "GST No"])
    writer.writeheader()
    writer.writerows(project_data)

print(f"✅ Data saved to {csv_file}")
