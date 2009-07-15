wmd_options = { autostart: false };
var Editor = function(){
    // Private
    var instances = {};

    //Public
    return {
        init: function(){},
        add_gui: function(id) {
            /***** Make sure WMD has finished loading *****/
            if (!Attacklab || !Attacklab.wmd) {
                alert("WMD hasn't finished loading!");
                return;
            }
            
            var textarea = document.getElementById(id);
            var editor = new Attacklab.wmd.editor(textarea);
            
            // save everything so we can destroy it all later
            instances[id] = {ta:textarea, ed:editor};
        },

        remove_gui: function(id) {
            var inst = instances[id];

            if (inst) {

                /***** destroy the editor and preview manager *****/
                inst.ed.destroy();
                instances[id] = null;
            }
        }
    };
}();