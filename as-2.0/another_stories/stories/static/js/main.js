$(document).on('click', '.like-story', like_story);
//$(document).on('click', '.remove-stories', remove_story);

//$(document).ready(function () {
//	$('.settings').bind('click', function() {
//		set_story_filter($(this).attr('id'));
//	});
//})

function like_story () {
	var story_id = $(this).attr('id');
    var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
	$.ajax({
		type: 'POST',
		url: '/stories/' + story_id + '/like/',
        data : { 'csrfmiddlewaretoken': token },
		success: function (result) {
			if (result['result'] === 'OK') {
				$('#likes_for_' + story_id).html(result['likes']);
			} else if (result['result'] === 'FAILED') {
				console.log('Like stories request FAILED!')
			} else {
				console.log('Something gone wrong..')
			}
		},
		error: function (result) {
			console.log('Connection error')
		}
	});
}

//function set_story_filter (filter) {
//	console.log(filter);
//	$.ajax({
//		type: 'POST',
//		url: '/settings/story_filter/' + filter,
//		success: function (result) {
//			console.log('The stories filter was changed to a : ' + filter);
//			location.reload();
//		},
//		error: function (result) {
//			console.log('Something gona wrong.. with filter');
//		}
//	});
//}