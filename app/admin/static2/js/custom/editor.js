/*
 * This is the javascript that is specific to the the editor
 * page
 */

$(document).ready(function () {
    // Launch the editor on page load
    $(".editor").ghostDown();


    // Make an ajax call back to the server if
    // the save button is pressed
    $('#save-button').on('click', function() {
        $.ajax({
            type: "POST",
            url: "/editor/save",
            data: {
                'markdown': window.theEditor.getValue(),
                'html': $('.rendered-markdown').html(),
                'post_id': window.location.pathname.split('/')[2],
                'title': $('#entry-title').val(),
            },
            success: function(data) {
                // New posts should be routed to the 
                // 'edit' page instead of staying on the 
                // new post page
                if (data.new_post == true) {
                    alert('Post Saved')
                    redirect_url = 'http://' + window.location.host + window.location.pathname + '/' + data.post_id;
                    window.location.href = redirect_url;
                } else {
                    alert('Post Saved')
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){  
                alert('There functional error trying to save your post. You may be trying to edit a post that doesnt exist.');
            }
        });
    });
    
    // Mark the active post with active class
    var paths = location.pathname.split('/');
    var post_number = paths[paths.length-1];
    $('#post-' + post_number).addClass("active-post");
});



function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
