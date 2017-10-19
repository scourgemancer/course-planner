#! python3
# courseParsing.py - Parses data from the Skidmore schedule search website
#                      and saves it all in a JSON format

import sys
import bs4
from selenium import webdriver


def parse_all():  # calls parse_term() for each term it finds available
    driver = webdriver.Firefox()  # get to the page with all the available terms on it with Selenium, through Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:
        terms_container = driver.find_element_by_id('term_code')
        terms = terms_container.find_elements_by_tag_name('option')
        for term in terms:
            parse_term(term.text)
    except:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return


def parse_term(term):  # parses all available course data from Skidmore for the given term
    driver = webdriver.Firefox()  # navigate to the page with all course info on it with Selenium, through Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:
        term_selector = driver.find_element_by_xpath("//option[text()='" + term + "']")
    except:
        print('Was unable to find the option for: ' + term)
        return
    term_selector.click()
    button = driver.find_element_by_id('Submit')
    button.click()
    all_departments = driver.find_element_by_xpath("//option[text()='All Departments']")
    all_departments.click()
    button = driver.find_element_by_id('Submit')
    button.click()

    # navigated to the page, now pull the html with Beautiful Soup
    html = driver.page_source
    driver.quit()
    coarse_soup = bs4.BeautifulSoup(html)
    course_table_rows = coarse_soup.select('.msTableGeneralTop tbody tr')
    if len(course_table_rows) == 0:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return
    save(term, course_table_rows)


def save(term_name,  table_rows):  # saves data from the scraped table rows in a JSON format
    return


def main():
    print('Gathering data...')
    if len(sys.argv) > 0:  # then only parse a specific term
        term = sys.argv[1:]
        parse_term(term)
    else:  # we parse all available terms
        parse_all()


main()
