$(document).ready(function($){
  $('#accordion').find('.accordion-toggle').click(function(){
    $(this).next().slideToggle('fast');
  })
});
