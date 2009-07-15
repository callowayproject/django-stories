var Editor = function(){
    // Private
    function toggleHTMLEditor(id) {
        if (!tinyMCE.get(id)){
            tinyMCE.execCommand('mceAddControl', false, id);
        } else {
            tinyMCE.execCommand('mceRemoveControl', false, id);
        }
    };
    //Public
    return {
        markup: "HTML",
        init: function(){ },
        add_gui: function(id){ toggleHTMLEditor(id); },
        remove_gui: function(id){ toggleHTMLEditor(id); }
    };
}();