#! python3
# courseParsing.py - Parses data from the Skidmore schedule search website
#                      and saves it all in a JSON format

import sys
import bs4
import os
import json
from selenium import webdriver
from pathlib import Path


def parse_all():  # calls parse_term() for each term it finds available
    driver = webdriver.Firefox()  # opens Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:  # get all of the available terms
        terms_container = driver.find_element_by_id('term_code')
        terms = terms_container.find_elements_by_tag_name('option')
        terms = [term.text for term in terms]
        driver.quit()
        for term in terms:
            parse_term(term)  # parses each term one-by-one
    except:
        driver.quit()
        print('Contact1 a developer: The course website has changed and this program needs to be updated')
        return


def parse_term(term):  # parses all available course data from Skidmore for the given term
    print('Parsing data for ' + term + ':')
    driver = webdriver.Firefox()  # opens Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:  # selects the term
        term_selector = driver.find_element_by_xpath("//option[text()='" + term + "']")
        term_selector.click()
    except:
        driver.quit()
        print('Was unable to find the option for: ' + term)
        return

    # navigates to the page with all of the term data
    button = driver.find_element_by_id('Submit')
    button.click()
    print('Getting departments...')
    all_departments = driver.find_element_by_xpath("//option[text()='All Departments']")
    all_departments.click()
    button = driver.find_element_by_id('Submit')
    button.click()

    # finished navigating to the desired page; now scrape the html with Beautiful Soup
    print('Loading all class data for ' + term + '...')
    html = driver.page_source
    driver.quit()
    coarse_soup = bs4.BeautifulSoup(html, "html.parser")
    course_table_rows = coarse_soup.select('.msTableGeneralTop tbody tr')
    if len(course_table_rows) == 0:
        print('Contact3 a developer: The course website has changed and this program needs to be updated')
        return
    departments = coarse_soup.select('#subj_code option')

    # now clean the scraped data before saving it
    print('Cleaning all parsed data...')
    cleaned_departments = {}
    for dep in departments:
        cleaned_departments[dep['value']] = str(dep.string)
    del course_table_rows[0]  # deletes an unwanted row from the top that gets scraped as well
    class_attributes = [attr for attr in course_table_rows[0].contents if str(attr) != '\n']
    for x in range(len(class_attributes)):
        class_attributes[x] = str(class_attributes[x].string)
    del course_table_rows[0]  # now we're done with the row that lists the column names
    cleaned_classes = []
    for soupy_class in course_table_rows:
        attributes = [attr.string.strip() for attr in soupy_class.select('div')]
        if len(class_attributes) != len(attributes):
            raise Exception('Table rows are of inconsistent length')
        cleaned_class = {}
        for x in range(len(class_attributes)):
            cleaned_class[class_attributes[x]] = attributes[x]
        cleaned_classes.append(cleaned_class)
    save(term, cleaned_departments, cleaned_class_attributes, cleaned_classes)


def save(term_name, departments, classes):  # saves data from the scraped table rows in a JSON format
        print('Saving data...')
        path = Path('data/' + term_name)
        if not path.is_dir():  # makes the folder to hold the term data in
            os.makedirs(path)

        with open(path + '/departments.json', 'w') as file:
            json.dump(departments, file)

        with open(path + '/classes.json', 'w') as file:
            json.dump(classes, file)


def main():
    print('Gathering data...')
    if len(sys.argv) > 0:  # then only parse a specific term
        term = sys.argv[0]
        parse_term(term)
    else:  # we parse all available terms
        parse_all()


main()
