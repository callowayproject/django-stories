/*
This file contains the js for the  quickedit
functionality on the story admin change list.
*/

(function($){
  $(document).ready(function(){
    $('.quickedit').each(function(){
      $(this).click(function(){
        var target = $("#qe-form-" + $(this).attr("id").replace("quickedit-", ""));
        $(target).toggle();
        $(".qe-reset", target).click(function(){
          $(target).toggle();
        });
      });
    });
  });
})(django.jQuery);