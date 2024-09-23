from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

def select_season(driver, index):
    try:
        season_dropdown = WebDriverWait(driver, 13).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "nice-select"))
        )
        driver.execute_script("arguments[0].click();", season_dropdown)

        # Wait for options to become visible
        WebDriverWait(driver, 13).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".nice-select ul li"))
        )

        # Get all <li> options in the dropdown
        li_elements = driver.find_elements(By.CSS_SELECTOR, ".nice-select ul li")

        # Select the season based on index
        if index < len(li_elements):
            driver.execute_script("arguments[0].click();", li_elements[index])

            # Wait for the score table to be available
            score_table = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, 'results'))
            )
            return score_table  # Return the score table

        else:
            print("Index out of range for the available seasons.")

    except Exception as e:
        print(f"An error occurred during the season selection: {e}")

def extract_matches(number):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_driver_path = r"C:\Users\hp\Desktop\chromedriver_win32\chromedriver.exe"
        os.environ['PATH'] += os.pathsep + chrome_driver_path
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.footballdatabase.eu/en/competition/overall/18337-premier_league/2023-2024")

        
        for index in range(1, number+1):  
            season_year = 2024 - index 
            season_text = f"{season_year}-{season_year + 1}"
            print(f"Collecting data for season: {season_text}")

            try:
                # Remove overlay if present
                overlay = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'nadzUoverlay'))
                )
                driver.execute_script("arguments[0].remove();", overlay)
            except TimeoutException:
                print("Overlay not found, skipping removal step")

            # Select the season and get the score table
            score_table = select_season(driver, index)
            print('dropdown_clicked')

            epl = []

            for i in range(38):  # Number of rounds in EPL
                try:
                    journee = score_table.find_element(By.CLASS_NAME, 'dday').text
                    liste = score_table.find_element(By.CLASS_NAME, 'list')
                    date = liste.find_element(By.CLASS_NAME, 'date.line.all').text
                    matches = liste.find_elements(By.CLASS_NAME, 'line.all')

                    for match in matches:
                        if 'date' not in match.get_attribute('class'):
                            home_team = match.find_element(By.CLASS_NAME, 'club.left').text
                            visitor = match.find_element(By.CLASS_NAME, 'club.right').text
                            score = match.find_element(By.CLASS_NAME, 'score').text.replace(' ', '-')
                            match_time = match.find_element(By.CLASS_NAME, 'hour').text

                            if score:
                                home_score, visitor_score = map(int, score.split('-'))

                                result = 'W' if home_score > visitor_score else 'L' if home_score < visitor_score else 'D'

                                epl.append({
                                    "competition": 'Premier League',
                                    "round": journee,
                                    "day": date,
                                    "home_team": home_team,
                                    "visitor": visitor,
                                    "score": score,
                                    "home_team_result": result,
                                    "time": match_time
                                })

                    # Navigate to the previous round
                    try :
                        day_before = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'daybefore'))
                        )
                        day_before.click()
                    except Exception as e :
                        print(f"here is the pro : {e} ")
                except TimeoutException:
                    print(f"Error occurred in round {i + 1}: Couldn't click on 'Previous round' button")
                    break

            # Save data for each season separately
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"EPL_{season_text}.csv")
            pd.DataFrame(epl).to_csv(output_path, index=False)

            print(f"Collected {len(epl)} matches for season {season_text}")

        driver.quit()

    except Exception as e:
        print(f"An error occurred during the execution: {e}")

extract_matches(6)