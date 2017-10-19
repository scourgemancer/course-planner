#! python3
# courseParsing.py - Parses data from the Skidmore schedule search website
#                      and saves it all in a JSON format

import sys
import bs4
import os
import errno
import json
from selenium import webdriver


def parse_all():  # calls parse_term() for each term it finds available
    driver = webdriver.Firefox()  # opens Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:  # get all of the available terms
        terms_container = driver.find_element_by_id('term_code')
        terms = terms_container.find_elements_by_tag_name('option')
        for term in terms:
            parse_term(term.text)  # parses each term one-by-one
    except:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return


def parse_term(term):  # parses all available course data from Skidmore for the given term
    driver = webdriver.Firefox()  # opens Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:  # selects the term
        term_selector = driver.find_element_by_xpath("//option[text()='" + term + "']")
        term_selector.click()
    except:
        print('Was unable to find the option for: ' + term)
        return
    try:  # navigates to the page with all of the term data
        button = driver.find_element_by_id('Submit')
        button.click()
        all_departments = driver.find_element_by_xpath("//option[text()='All Departments']")
        all_departments.click()
        button = driver.find_element_by_id('Submit')
        button.click()
    except:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return

    # finished navigating to the desired page; now scrape the html with Beautiful Soup
    html = driver.page_source
    driver.quit()
    coarse_soup = bs4.BeautifulSoup(html)
    course_table_rows = coarse_soup.select('.msTableGeneralTop tbody tr')
    if len(course_table_rows) == 0:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return
    save(term, course_table_rows)


def save(term_name,  table_rows):  # saves data from the scraped table rows in a JSON format
    path = 'data/' + term_name + '.txt'

    try:  # makes the file to write to
        os.remove(path)  # delete the file if it exists, before saving
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise  # re-raise the exception if a different error occurred
    os.makedirs(path)

    # encodes data into JSON format
    data = 'JSON'  # TODO

    with open(path, 'w') as f:  # writes the data to the file
        json.dump(data, f)


def main():
    print('Gathering data...')
    if len(sys.argv) > 0:  # then only parse a specific term
        term = sys.argv[0]
        parse_term(term)
    else:  # we parse all available terms
        parse_all()


main()
