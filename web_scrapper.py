import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of website URLs containing government tenders
website_urls = [
  "https://www.govt.lc/tenders",
  "https://www.govt.lc/consultancies",
  "https://www.finance.gov.lc/tenders/",
  "https://www.fao.org/unfao/procurement/bidding-opportunities/user-form/en/",
  #"https://www.ungm.org/Public/Notice",
  #"https://www.finance.gov.lc/tenders/",  
  "https://www.oecs.org/en/work-with-us/procurements/current-tenders",  
  "https://cppnb.caricom.org/epps/home.do", 
  "https://www.finance.gov.tt/divisions/central-tenders-board/tenders-notices/",
  #"https://www.gojep.gov.jm/epps/quickSearchAction.do?isCurrentCompetitions=true&captcha=f8qvrp&d-3680175-p=1&searchSelect=8",
  "https://www.npta.gov.gy/procurement-opportunities/"
]

# Create a CSV file to store the scraped data
csv_file = open('scraped_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
# Write headers to the CSV file
csv_writer.writerow(["Tender Title", "Tender Posted On", "Closing On", "Description", "Ministry/Agency","Location", "PDF Link", "More Information"])

# Set up Chrome WebDriver
chrome_service = ChromeService(executable_path=r"C:\Users\nysap\chromedriver-win64\chromedriver.exe")  # Use raw string to avoid escape characters
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run browser in headless mode (no GUI)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

for url in website_urls:
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    if url == website_urls[0] or url == website_urls[1]:
        try:
            tender_elements = driver.find_elements(By.CLASS_NAME, "rc-title.font-bold")
            tender_dates=driver.find_elements(By.CLASS_NAME, "rc-date.font-normal")

            for element,element2 in zip(tender_elements, tender_dates):
                try:
                    tender_title = element.find_element(By.TAG_NAME, "span").text.strip()
                    tender_posting_date = element2.find_element(By.TAG_NAME, "span").text.strip()
                    
                    print("Tender Title:", tender_title)
                    print("Tender Posted On:", tender_posting_date)
                    # Append the title to the end of the base URL with hyphens between words
                     # Remove non-letter characters and convert to lowercase
                    title_slug = "-".join(re.findall(r'[a-zA-Z]+', tender_title.lower()))

                    new_url = url + "/" + title_slug
                    print("More information can be found at:", new_url)
                    print("=" * 50)
                    # Write the scraped data to the CSV file
                    csv_writer.writerow([tender_title, tender_posting_date, "", "", "","St Lucia","",new_url])
                except Exception as e:
                    print("Error:", e)
        except Exception as e:
            print("Error:", e)
    
    if url==website_urls[2]:
        try:
            # Find the table body containing the tender information
            table_body = driver.find_element(By.TAG_NAME, "tbody")
            rows = table_body.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 6:
                    tender_title = columns[0].find_element(By.TAG_NAME, "a").text
                    closing_date = columns[3].text
                    ministry = columns[4].text.title()
                    posted_on = columns[5].text
                    
                    print("Tender Title:", tender_title)
                    print("Tender Posted On:", posted_on)
                    print("Closing On:", closing_date)
                    print("Ministry associated with:", ministry)
                    print("More information can be found at:", url)
                    print("=" * 50)
                    csv_writer.writerow([tender_title, posted_on, closing_date, "", ministry,"St Lucia","",url])
                    
        except Exception as e:
            print("Error:", e)

    if url==website_urls[3]:
        try:
            # Find the table body containing the tender information
            table_body = driver.find_element(By.TAG_NAME, "tbody")
            rows = table_body.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 6:
                    tender_title = columns[0].find_element(By.TAG_NAME, "a").text
                    closing_date = columns[3].text
                    ministry = columns[4].text.title()
                    posted_on = columns[5].text
                    
                    print("Tender Title:", tender_title)
                    print("Tender Posted On:", posted_on)
                    print("Closing On:", closing_date)
                    print("Ministry associated with:", ministry)
                    print("More information can be found at:", url)
                    print("=" * 50)
                    csv_writer.writerow([tender_title, posted_on, closing_date, "", ministry,"","",url])
        except Exception as e:
            print("Error:", e)

    if url==website_urls[4]:
        try:
            # Find all elements with class "edocman-document"
            documents = driver.find_elements(By.CLASS_NAME, 'edocman-document')

            # Loop through the documents and extract information
            for document in documents:
            # Extract document title
                title_element = document.find_element(By.CLASS_NAME, 'edocman-document-title-link')
                title = title_element.text

                # Extract date
                date_element = document.find_element(By.CLASS_NAME, 'dateinformation')
                post_date = date_element.text.strip().split('&nbsp;')[0]

                # Extract description
                description_element = document.find_element(By.CLASS_NAME, 'edocman-description-details')
                description = description_element.text.strip()

                # Print or store the extracted information
                print("Title:", title)
                print("Tender Posted On:", post_date)
                print("Description:", description)
                print("More information can be found at:", url)
                print("=" * 50)
                csv_writer.writerow([title, post_date, "",description, "","","",url])
                
        except Exception as e:
            # Handle general exceptions, like WebDriverException
            print("Error:", e)
    
    if url==website_urls[5]:
        table = driver.find_element(By.TAG_NAME, 'tbody')

        # Find all rows in the table
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Loop through the rows and extract information
        for row in rows:
            try:
                # Extract data from each cell in the row
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) >= 9:
                    # Extract relevant data from the cells
                    project_name = cells[1].find_element(By.TAG_NAME, 'a').text
                    agency = cells[2].text.title()
                    closing_date = cells[4].text
                    location = cells[6].text.title()
                    pdf_link = cells[8].find_element(By.TAG_NAME, 'a').get_attribute('href')

                    # Print or store the extracted information
                    print("Tender Title:", project_name)
                    print("Agency:", agency)
                    print("Closing Date:", closing_date)
                    print("Location:", location)
                    print("PDF Link:", pdf_link)
                    print("More information can be found at:", url)
                    print("\n")
                    csv_writer.writerow([project_name, "", closing_date, "", agency,location, pdf_link, url])
            except Exception as e:
                # Handle general exceptions, like WebDriverException
                print("Error:", e)
    
    if url==website_urls[6]:
        try:
            # Find all the <a> elements with class "post-block"
            post_blocks = driver.find_elements(By.CLASS_NAME, 'post-block')

            # Iterate through each post block and extract the information
            for post_block in post_blocks:
                # Extract the title, date, and link
                tt_title = post_block.find_element(By.CLASS_NAME, 'post_block_title').text.strip()
                tt_date = post_block.find_element(By.CLASS_NAME, 'post_block_date').text.strip()
                link = post_block.get_attribute('href')

                # Print or process the extracted information
                print("Title:", tt_title)
                print("Date:", tt_date)
                print("PDF Link:", link)
                print("More information can be found at:", url)
                print("\n")
                csv_writer.writerow([tt_title, tt_date, "", "","" ,"", link, url])
        except Exception as e:
            print("An error occurred:", str(e))

    if url == website_urls[7]:
        # Wait for a few seconds to ensure the page loads completely (you may need to adjust the wait time)
        driver.implicitly_wait(100)
        try:
            # Find all elements with class names matching the pattern
            rows = driver.find_elements(By.CSS_SELECTOR, '[class^="ninja_table_row_"]')

            # Loop through each row and extract data
            for row in rows:
                title = row.find_element(By.CLASS_NAME, "ninja_column_0").text
                procuring_entity = row.find_element(By.CLASS_NAME, "ninja_column_1").text
                bids_submission_deadline = row.find_element(By.CLASS_NAME, "ninja_column_2").text
            
                print("Title:", title)
                print("Procuring Entity:", procuring_entity)
                print("Bids Submission Deadline:", bids_submission_deadline)
                print("More information can be found at:", url)
                print("\n")
                csv_writer.writerow([title, "", bids_submission_deadline, "",procuring_entity,"", "", url])
            
        except Exception as e:
            print("An error occurred:", str(e))
    
# Close the CSV file
csv_file.close()

# Quit the browser
driver.quit()
