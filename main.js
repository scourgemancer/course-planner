/*global $, document, getTerms, getDepartments, getRatings, getClasses*/
/* eslint-env es6 */
$(document).ready(function addContent($) {
  "use strict";

  //Set all of the term options in the navbar
  getTerms().forEach(function addTerms(term) {
    $('#terms').append('<option>' + term + '</option>');
  });
  $('#terms').change(populateWithTermData(getDepartments(), getClasses(), getRatings()));

  populateWithTermData(getDepartments(), getClasses(), getRatings());

  //Adds functionality to the search bar
  $("#searchBar").keydown(function searchContent() {
    let search = document.getElementById("searchBar").value;
    if (search !== '') {
      $('.course').each(function searchCourses() {
        if ($(this).children('h3').text().toLowerCase().indexOf(search.toLowerCase()) !== -1) {
          $(this).css('display', 'block');
        } else {
          $(this).css('display', 'none');
        }
      });
      $('.department').each(function searchDepartments() {
        if ($(this).has('.course:visible').length > 0) {
          $(this).css('display', 'block');
        } else {
          $(this).css('display', 'none');
        }
      });
    } else {
      $('.course').css('display', 'none');
      $('.department').css('display', 'none');
      $('.department').has('.course').css('display', 'block');
    }
  });

  //Adds the expected functionality for the accordions w/o needing the large jQuery file
  $('#accordion').find('.accordion-toggle').click(function toggle() {
    $(this).next().slideToggle('fast');
  });
});


//Takes in a term's departments, classes, and ratings then populates the page with it
function populateWithTermData(departments, classes, ratings) {
  "use strict";

  clearTermData();

  //Sets an accordion for each department
  Object.keys(departments).forEach(function addDepartments(key) {
    if (key !== "all") {
      $('#departments').append(
        '<div class="department ' + key + '" id="accordion">' +
        '<h3 class="accordion-toggle">' + departments[key] + '</h3>' +
        '<div class="accordion-content courses"></div>' +
        '</div>');
    }
  });

  //Populates each department with the classes they're composed of
  classes.forEach(function addClasses(eachClass) {
    let sanitizeName = new RegExp(/[ .:#()\/\-&]/, 'g');
    let sanitizedName = eachClass.Title.replace(sanitizeName, '_');
    let sanitizedCRN = eachClass.CRN.replace(sanitizeName, '_');

    //Makes a course accordion if the course hasn't been added yet
    if ($(".course > h3:contains(" + eachClass.Title + ")").length === 0) {
      departments = eachClass.Course.substring(0, eachClass.Course.indexOf('-'));
      $('.' + departments + ' > .accordion-content').append(
        '<div class="course" id="accordion">' +
        '<h3 class="accordion-toggle">' + eachClass.Title + '</h3>' +
        '<div class="accordion-content classes ' + sanitizedName + '"></div>' +
        '</div>');
    }
    //Adds this specific class to its course accordion
    $("." + sanitizedName).append('<table class="class" id="' + sanitizedCRN + '"></table>');
    Object.keys(eachClass).forEach(function addClass(key) {
      if (key === 'Instructor' && eachClass[key] in ratings && ratings[eachClass[key]][0] !== 'n/a') {
        $("#" + sanitizedCRN).append(
          '<tr class="' + key + '">' +
          '<th>' + key + '</th>' +
          '<td>' + eachClass[key] + ' (<a target="_blank" href="' + ratings[eachClass[key]][1] + '">' +
          '' + ratings[eachClass[key]][0] + '/5.0' +
          '</a>)</td>' +
          '</tr>');
      } else {
        $("#" + sanitizedCRN).append(
          '<tr class="' + key + '">' +
          '<th>' + key + "</th><td>" + eachClass[key] + '</td>' +
          '</tr>');
      }
    });
  });

  //Hides any departments that don't have any classes for the selected term
  $('.department').css('display', 'none');
  $('.department').has('.course').css('display', 'block');
}

function clearTermData() {
  "use strict";

  $('#departments').empty();
}
