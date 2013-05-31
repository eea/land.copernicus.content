jQuery(document).ready(function() {
    jQuery('#siteaction-news').addClass("frozenEntry");
    jQuery('.frozenEntry a').bind('click', function(event){
        return false;
    });
});
