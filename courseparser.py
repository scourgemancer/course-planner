#!/usr/bin/env python
"""courseparser.py - Parses data from the Skidmore Master Schedule and saves it as JSON strings"""
import sys
import bs4
import time
import os
import json
from selenium import webdriver
from pathlib import Path


def parse_all():
    """Calls parse_term() for each term it finds available."""
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
        print('Contact1 a developer: The course website has changed and this program needs to be updated')
    finally:
        driver.quit()  # just to make sure that all opened browsers get closed


def parse_term(term):
    """Parses all available course data from Skidmore for the given term and then saves it."""
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
    time.sleep(60 * 5)
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
    save(term, cleaned_departments, cleaned_classes)


def save(term_name, departments, classes):
    """Encodes provided data to a JSON format and then saves it to a file."""
    print('Saving data...')
    path = Path('data/' + term_name)
    if not path.is_dir():  # makes the folder to hold the term data in
        os.makedirs(str(path))

    with open(str(path) + '/departments.json', 'w') as file:
        json.dump(departments, file)

    with open(str(path) + '/classes.json', 'w') as file:
        json.dump(classes, file)


def main():
    if len(sys.argv) > 1:  # then only parse a specific term
        term = sys.argv[-1]
        parse_term(term)
    else:  # we parse all available terms
        parse_all()


if __name__ == "__main__":
    main()
