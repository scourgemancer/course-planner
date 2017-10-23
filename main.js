/*global $, document*/ //<- is to appease JSLint
$(document).ready(function ($) {
  "use strict";
  $('#accordion').find('.accordion-toggle').click(function () {
    $(this).next().slideToggle('fast');
  });
});
