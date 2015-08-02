$(function() {
    function showLinks(element, target){
        element.nextAll('ul.'+target).toggle();
        element.addClass('active');
    }

    function hideLinks(element){
        element.parent().find('ul').hide();
        element.parent().find('button').removeClass('active');
    }

    $(document).on('click', '[data-show-links="collapse"]', function (e) {
        var $this = $(this);
        var target = $this.attr('data-target');
        var show = $this.nextAll('ul.'+target).is(':visible');
        hideLinks($this);
        if (!show) {
            showLinks($this, target);
        }
    })
});