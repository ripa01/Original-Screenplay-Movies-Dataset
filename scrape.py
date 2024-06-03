import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

options = Options()

# Set the Brave browser executable path
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
options = Options()
options.add_argument("--headless")
options.binary_location = brave_path

# Initialize the Chrome WebDriver with specified options
driver = webdriver.Chrome(options=options)

def scrape_data(url):
    # Send a request to the search page 
    driver.get(url)

    try:
        # Wait for the page to load 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page_filling_chart"]/center/table/tbody')))
    except TimeoutException:
        # If no search results found, handle the case here
        print("Page elements not found within the timeout period")
        return []

    result_elements = driver.find_elements(By.XPATH, '//*[@id="page_filling_chart"]/center/table/tbody/tr')
    total_li = len(result_elements)
    print(total_li)
    data = []

    for i in range(2, total_li - 2):
        # Wait for elements on redirected page
        try:
            # Wait for the elements you want to scrape to be present on the redirected page 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]')))
        except TimeoutException:
            # If the elements are not found, handle the case here
            print(f"Elements not found on row {i}")
            continue

        try:
            movie_name = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[2]/b/a').text
        except NoSuchElementException:
            movie_name = "N/A"

        try:
            release_date = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[3]/a').text
        except NoSuchElementException:
            release_date = "N/A"

        try:
            genre = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[4]/a').text
        except NoSuchElementException:
            genre = "N/A"

        try:
            mpaa_rating = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[5]/a').text
        except NoSuchElementException:
            mpaa_rating = "N/A"

        try:
            gross_year = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[6]').text
        except NoSuchElementException:
            gross_year = "N/A"

        try:
            tickets_sold = driver.find_element(By.XPATH, f'//*[@id="page_filling_chart"]/center/table/tbody/tr[{i}]/td[7]').text
        except NoSuchElementException:
            tickets_sold = "N/A"

        # Append the scraped data to the list
        data.append({
            'Movie Name': movie_name,
            'Released Date': release_date,
            'Genre': genre,
            'MPAA Rating': mpaa_rating,
            'Year Gross': gross_year,
            'Tickets Sold': tickets_sold
        })

    return data

# URL pattern for the pages
base_url = "https://www.the-numbers.com/market/{}/source/Original-Screenplay"

# Create an empty list to store all data
all_data = []

# Iterate over multiple pages
for page_num in range(1995, 2025): 
    print(f"Scraping data from year {page_num}")
    url = base_url.format(page_num)

    # Scrape data from the current page and append it to the list
    page_data = scrape_data(url)
    all_data.extend(page_data)

# Create DataFrame from collected data
df = pd.DataFrame(all_data)

# Save DataFrame to a single Excel file after scraping all pages
df.to_excel('movie_data.xlsx', index=False)

# Close the WebDriver
driver.quit()
