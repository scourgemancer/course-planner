/*global $, document*/ //<- is to appease JSLint
$(document).ready(function ($) {
  "use strict";
  var terms, departments, keys;
  terms = ["Fall 2017", "Summer 2017", "Spring 2017"];
  terms.forEach(function (term) {
    $('#terms').append('<option>' + term + '</option>');
  });

  departments = {"AM": "American Studies", "AN": "Anthropology", "AR": "Art", "AH": "Art History", "AA": "Arts Administration", "AS": "Asian Studies", "BI": "Biology", "CH": "Chemistry", "CLA": "Classics", "CO": "Computer Science/MC", "DA": "Dance", "DS": "Documentary Studies", "EC": "Economics", "EDS": "Education Studies", "EN": "English", "ES": "Environmental Studies and Sci", "EX": "Exercise Science", "GW": "Gender Studies", "GS": "Geosciences", "HI": "History", "HF": "Honors Forum", "ID": "Interdisciplinary", "IGR": "Intergroup Relations", "IA": "International Affairs", "IN": "Internships", "LAS": "Latin American Studies", "LI": "Library", "JL": "London First Year Program", "MB": "Management and Business", "MA": "Mathematics/MC/MS", "MF": "Media and Film Studies", "MU": "Music", "NS": "Neuroscience", "HE": "Opportunity Programs", "PH": "Philosophy", "PA": "Physical Activity", "PY": "Physics", "PL": "Political Science", "PREO": "Pre-Orientation Program", "PS": "Psychology", "RE": "Religious Studies", "SSP": "Scribner Seminar", "SD": "Self Determined", "JSK": "Skidmore Shakespeare Program", "JC": "Skidmore in China", "JP": "Skidmore in Paris", "JS": "Skidmore in Spain", "SW": "Social Work", "SO": "Sociology", "TH": "Theater", "TX": "Travel Seminar", "WLL": "World Lang and Literature", "all": "All Departments"};
  keys = Object.keys(departments);
  keys.forEach(function (key) {
    if (key !== "all") {
      $('#departments').append('<h3 class="accordion-toggle" class="department" id="' + key + '">' + departments[key] + '</h3><div class="accordion-content" class="classes"></div>');
    }
  });

  $('#accordion').find('.accordion-toggle').click(function () {
    $(this).next().slideToggle('fast');
  });
});
