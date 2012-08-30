
# This file contains the js for the  quickedit
# functionality on the story admin change list.

(($) ->

  updateSel = (elem, selector) ->
    selId = $(elem).attr 'id'
    $("#{selector} ##{selId}").val $(elem).val()

  $(document).ready ->

    # Toggle the quick edit row
    $('.quickedit').each ->
      $(@).click ->
        id = $(@).attr('id').replace('quickedit-', '')
        target = $("#qe-form-#{id}")
        $(target).toggle()
        $('.qe-reset', target).click ->
          $(target).toggle()

    $('#result_list select').change ->
      updateSel @, '.quickedit-row'
      $(@).parent().parent().css 'background', '#FFC'

    $('.quickedit-row select').change ->
      updateSel @, '#result_list'

)(django.jQuery)
