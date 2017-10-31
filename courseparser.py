#!/usr/bin/env python
"""courseparser.py - Parses data from the Skidmore Master Schedule and saves it as JSON strings"""
import sys
import bs4
import requests
import os
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def parse_all():
    """Calls parse_term() for each term it finds available."""
    print('Getting available terms to parse:')
    driver = webdriver.Firefox()  # opens Firefox
    driver.get('https://www2.skidmore.edu/studentsystem/masterSchedule/index.cfm')
    try:  # get all of the available terms
        terms_container = driver.find_element_by_id('s2id_txt_term')
        terms = []
        current_term = ''
        while current_term not in terms:
            if current_term != '':
                terms.append(current_term)
            terms_container.click()
            terms_container.send_keys(Keys.ENTER)
            for i in range(len(terms)):
                terms_container.send_keys(Keys.DOWN)
            current_term = driver.find_element_by_id('select2-chosen-1')
        driver.quit()
        with open('data/terms.json', 'w') as file:
            json.dump(terms, file)
        print('Parsing terms:')
        for term in terms:
            #parse_term(term)  # parses each term one-by-one
            print(term)
        print('Finished parsing all available terms!')
    except:
        print('Contact a developer: The course website has changed and this program needs to be updated')
    finally:
        driver.quit()  # just to make sure that all opened browsers get closed


def parse_term(term):
    """Parses all available course data from Skidmore for the given term and then saves it."""
    print('Parsing data for ' + term + ':')
    html = get_master_schedule_html(term)
    coarse_soup = bs4.BeautifulSoup(html, "html.parser")
    course_table_rows = coarse_soup.select('.msTableGeneralTop tbody tr')
    if len(course_table_rows) == 0:
        print('Contact a developer: The course website has changed and this program needs to be updated')
        return
    departments = coarse_soup.select('#subj_code option')

    # now clean the scraped data before saving it
    print('Cleaning all parsed data...')
    cleaned_departments = {}
    for dep in departments:
        cleaned_departments[dep['value']] = str(dep.string).strip()
    del course_table_rows[0]  # deletes an unwanted row from the top that gets scraped as well
    class_attributes = [attr for attr in course_table_rows[0].contents if str(attr) != '\n']
    for x in range(len(class_attributes)):
        class_attributes[x] = str(class_attributes[x].string).strip()
    del course_table_rows[0]  # now we're done with the row that lists the column names
    cleaned_classes = []
    for soupy_class in course_table_rows:
        attributes = [attr.string.strip() for attr in soupy_class.select('div')]
        if len(class_attributes) != len(attributes):
            raise Exception('Table rows are of inconsistent length')
        cleaned_class = {}
        for x in range(len(class_attributes)):
            cleaned_class[class_attributes[x]] = attributes[x]
        if cleaned_class['Course'] == '':
            cleaned_classes[-1]['next lines'] = cleaned_class
        else:
            cleaned_class['next lines'] = []
            cleaned_classes.append(cleaned_class)

    # get the teacher ratings from ratemyprofessors.com
    print('Getting ratings for professors...')
    ratings = {}
    for cleaned_class in cleaned_classes:
      teacher = cleaned_class['Instructor']
      rating = getRating(teacher)
      ratings[teacher] = rating
    print('Finished getting all available professor ratings!')
    save(term, cleaned_departments, cleaned_classes, ratings)
    print('Finished parsing: ' + term + '!')


def get_master_schedule_html(term):
    """Gets the HTML containing all classes in the given term from the Master Schedule."""
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
    old = driver.page_source
    button = driver.find_element_by_id('Submit')
    button.click()
    print('Getting departments...')
    while old == driver.page_source:  # wait for the page to load
        time.sleep(1)
    all_departments = driver.find_element_by_xpath("//option[text()='All Departments']")
    all_departments.click()
    button = driver.find_element_by_id('Submit')
    button.click()

    # finished navigating to the desired page; now scrape the html with Beautiful Soup
    print('Loading all class data for ' + term + '...')
    time.sleep(60*5)
    html = driver.page_source
    driver.quit()
    return html


def getRating(teacher):
  """Navigates to the ratemyprofessos.com page for the given teacher and returns their rating"""
  names = teacher.split(', ')
  url = 'http://www.ratemyprofessors.com/search.jsp?query=' + names[0] + '%2C+' + names[-1]
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.text, "html.parser")
  professors = soup.select('.PROFESSOR')
  if len(professors) > 0:
    right_one = professors[0]
    found_them = False
    for professor in professors:
      school = str(professor.select('.sub')[0].string)
      if ', ' in school:
        school = school.split(', ')[0]
      if school == 'Skidmore College':
        right_one = professor
        found_them = True
    if found_them:
      link = 'http://www.ratemyprofessors.com' + right_one.select('a')[0].attrs['href']
      response = requests.get(link)
      soup = bs4.BeautifulSoup(response.text, "html.parser")
      return [str(soup.select('.grade')[0].string), link]
    else:
      return ['n/a']
  else:
    return ['n/a']


def save(term_name, departments, classes, ratings):
    """Encodes provided data to a JSON format and then saves it to a file."""
    print('Saving data...')
    path = Path('data/' + term_name)
    if not path.is_dir():  # makes the folder to hold the term data in
        os.makedirs(str(path))

    with open(str(path) + '/departments.json', 'w') as file:
        json.dump(departments, file)

    with open(str(path) + '/classes.json', 'w') as file:
        json.dump(classes, file)

    with open(str(path) + '/ratings.json', 'w') as file:
        json.dump(ratings, file)
    print('Data saved!')


def main():
    if len(sys.argv) > 1:  # then only parse a specific term
        term = sys.argv[-1]
        parse_term(term)
    else:  # we parse all available terms
        parse_all()


if __name__ == "__main__":
    main()
