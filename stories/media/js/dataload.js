var markupTypes = {
    txt: ['/static/js/nogui.js'],
    htm: ['/static/js/htm.js'], //'/static/tiny_mce/tiny_mce.js',
    crl: ['/static/js/nogui.js'],
    rst: ['/static/js/nogui.js'],
    txl: ['/static/js/nogui.js'],
    mrk: ['/static/js/mrk.js','/static/wmd/wmd.js']
};

function loadInitialMarkup(){
    var markup = document.getElementById('id_markup').value;
    LazyLoad.load(markupTypes[markup], loadComplete);
};

function changeMarkup(markupMenu){
    Editor.remove_gui('id_body');
    Editor.remove_gui('id_teaser');
    var markup = markupMenu.value;
    if (markupTypes[markup].length > 0){
        LazyLoad.load(markupTypes[markup], loadComplete);
    }
};

function loadComplete(){
    Editor.init();
    Editor.add_gui('id_body');
    Editor.add_gui('id_teaser');
};

//This uses Django's core.js function to add events
addEvent(window, 'load', loadInitialMarkup);
tinyMCE.init({
    mode: "none",
    relative_urls : false,
    convert_urls : false,
    theme: "advanced",
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    plugins : "xhtmlxtras,contextmenu,searchreplace,advlink,safari,paste,inline,advimage",
    paste_create_paragraphs : false,
    paste_create_linebreaks : false,
    paste_use_dialog : true,
    paste_auto_cleanup_on_paste : true,
    extended_valid_elements : "iframe[src|width|height|name|align],embed[src|bgcolor|flashVars|base|name|width|height|seamlesstabbing|type|swLiveConnect|pluginspage],inline[type|id|align|moremessage|startdate|enddate|title|longitude|latitude|label],story",
    paste_convert_middot_lists : false,
    paste_unindented_list_class : "unindentedList",
    paste_convert_headers_to_strong : true,
    theme_advanced_buttons1: "pastetext,pasteword,selectall,|,search,replace,|,bold,italic,underline,blockquote,removeformat,|,bullist,numlist,|,undo,redo,|,cite,abbr,acronym,charmap,link,unlink,image,inline,code,|,fullscreen",
    theme_advanced_buttons2: "",
    theme_advanced_buttons3: ""
});
