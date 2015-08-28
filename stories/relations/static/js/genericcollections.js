function showGenericRelatedObjectLookupPopup(triggeringLink, ctArray) {

    var realName = triggeringLink.id.replace(/^lookup_/, '');
    var name = id_to_windowname(realName);
    realName = realName.replace(/object_id/, 'content_type');
    var select = document.getElementById(realName);
    if (select.selectedIndex === 0) {
        alert("Select a content type first.");
        return false;
    }
    var selectedItem = select.item(select.selectedIndex).value;
    var href = ctArray[selectedItem];
    if (href.search(/\?/) >= 0) {
        href = href + '&_popup=1&_to_field=id';
    } else {
        href = href + '?_popup=1&_to_field=id';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function showGenericRequiredModelLookupPopup(triggeringLink, ctItem) {
    ctItem = ctItem.replace('.', '/');
    var realName = triggeringLink.id.replace(/^lookup_/, '');
    var name = id_to_windowname(realName);
    return showRelObjectLookupPopup(name, triggeringLink, ctItem);
}

function showRelObjectLookupPopup(name, triggeringLink, ctItem) {
    var href = triggeringLink.href = '../../../' + ctItem + '/';

    if (href.search(/\?/) >= 0) {
        href = href + '&_popup=1&_to_field=id';
    } else {
        href = href + '?_popup=1&_to_field=id';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
