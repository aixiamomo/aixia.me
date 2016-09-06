/*! Copyright (c) 2011 Piotr Rochala (http://rocha.la)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 *
 * Version: 1.3.7
 *
 */

 $('#scroll, #scrollh').slimScroll({
        height: $(window).height() - ($('#InputTitle').height() + 75),
		alwaysVisible: true,
		disableFaeOut: true,
		position: 'left'
    });
	
	window.onresize = function(){
	$('.slimScrollDiv, #scroll').each(function(){
		$(this).css( 'height', $(window).height() - ($('#InputTitle').height() + 75) );
		console.log($(this).height());
	});
	}
	$('.inputtitle').focusout(function(){
		if($(this).val().trim() == ""){
			$(this).val("(Untitled)");
		}
	});
	/*$('#button1').click(function(){
		editor = CodeMirror.fromTextArea(document.getElementById('entry-markdown'), {
				mode: 'markdown',
				tabMode: 'indent',
				lineWrapping: true
			});
	});*/