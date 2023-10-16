import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def download_etext_file_with_selenium(website_url, file_text, output_filename):
    driver = webdriver.Chrome()
    try:
        # Step 1: Create a new instance of the web driver (Firefox)

        # Step 2: Navigate to the website
        driver.get(website_url)

        # Step 3: Find the element with the specified link text
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, file_text))
        )
        # Step 4: Extract the download link (URL)
        download_url = element.get_attribute("href")

        # Step 5: Download the file using requests
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(output_filename, "wb") as f:
                f.write(response.content)
            return f"File downloaded successfully as {output_filename}"
        else:
            return "Failed to download the file."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        # Step 6: Close the browser
        driver.quit()


# Example usage:
if __name__ == "__main__":
    work_id = "W00EGS1016973"
    website_url = "http://purl.bdrc.io/resource/{work_id}"
    file_text = "Download"  # Modify to match your file's link text
    output_filename = "downloaded_file.pdf"
    result = download_etext_file_with_selenium(website_url, file_text, output_filename)
    print(result)
