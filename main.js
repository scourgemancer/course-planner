/*global $, document, getDepartments, getRatings, getClasses*/
/* eslint-env es6 */
$(document).ready(function ($) {
  "use strict";
  var terms, departments, ratings, classes;

  //Set all of the term options in the navbar
  terms = ["Fall 2017", "Summer 2017", "Spring 2017"];
  terms.forEach(function (term) {
    $('#terms').append('<option>' + term + '</option>');
  });

  //Sets an accordion for each department
  departments = getDepartments();
  Object.keys(departments).forEach(function (key) {
    if (key !== "all") {
      $('#departments').append(
        '<div class="department ' + key + '" id="accordion">' +
        '<h3 class="accordion-toggle">' + departments[key] + '</h3>' +
        '<div class="accordion-content courses"></div>' +
        '</div>');
    }
  });

  //Populates each department with the classes they're composed of
  ratings = getRatings();
  classes = getClasses();
  classes.forEach(function (eachClass) {
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
    Object.keys(eachClass).forEach(function (key) {
      if (key === 'Instructor' && eachClass[key] in ratings && ratings[eachClass[key]][0] !== 'n/a') {
        $("#" + sanitizedCRN).append(
          '<tr class="' + key + '">' +
          '<th>' + key + '</th>' +
          '<td>' + eachClass[key] + ' <a target="_blank" href="' + ratings[eachClass[key]][1] + '">' +
          '(' + ratings[eachClass[key]][0] + '/5.0)' +
          '</a></td>' +
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

  //Adds functionality to the search bar
  $("#searchBar").keydown(function () {
    //Only shows courses that have the search in their names
    let search = document.getElementById("searchBar").value;
    $('.course').each(function () {
      if ($(this).children('h3:contains("' + search + '")').length > 0) {
        $(this).css('display', 'block');
      } else {
        $(this).css('display', 'none');
      }
    });
    //Only shows departments that have the search in their name or have courses still visible
    $('.department').each(function () {
      if ($(this).children('h3:contains("' + search + '")').length > 0 || $(this).has('.course:visible').length > 0) {
        $(this).css('display', 'block');
      } else {
        $(this).css('display', 'none');
      }
    });
  });

  //Adds the expected functionality for the accordions w/o needing the large jQuery file
  $('#accordion').find('.accordion-toggle').click(function () {
    $(this).next().slideToggle('fast');
  });
});
