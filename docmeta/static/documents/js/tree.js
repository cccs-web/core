// Adapted from http://jsfiddle.net/jhfrench/GpdgF/
$(function () {

    // Initialize title, appearance and set parent_li (assumes all collapsed)
    var expandables = $('.tree li:has(ul)');
    expandables.addClass('parent_li');
    expandables.find('> span').attr('title', 'Expand this branch');

    expandables.find('> span > i')
        .removeClass('fa-folder-open-o')
        .addClass('fa-folder');

    // Add open/close behaviour to all parent_li
    $('.tree li.parent_li > span').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        if (children.is(":visible")) {
            children.hide('fast');
            $(this).attr('title', 'Expand this branch').find(' > i').addClass('fa-folder').removeClass('fa-folder-open');
        } else {
            children.show('fast');
            $(this).attr('title', 'Collapse this branch').find(' > i').addClass('fa-folder-open').removeClass('fa-folder');
        }
        e.stopPropagation();
    });
    $.each($('.tree > ul').children(), function(idx, child){
        var $child = $(child);
        $child.show('fast');
    })
});