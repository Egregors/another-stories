$(document).on('click', '.like-story', like_story);
$(document).on('click', '.remove-story', remove_story);

$(document).ready(function () {

})

function like_story () {
	var story_id = $(this).attr('id');
	$.ajax({
		type: 'POST',
		url: '/story/like/' + story_id,
		success: function (result) {
			if (result['result'] === 'OK') {
				$('#likes_for_' + story_id).html(result['likes']);
			} else if (result['result'] === 'FAILED') {
				console.log('Like story request FAILED!')
			} else {
				console.log('Something gona wrong..')
			}
		},
		error: function (result) {
			console.log('Connection error')
		}
	});
}

function remove_story () {
	var story_id = $(this).attr('id');
	$.ajax({
		type: 'POST',
		url: '/story/remove/' + story_id,
		success: function (result) {
			if (result['result'] === 'OK') {
				console.log('remove_story: OK')
				$('#main_' + story_id).fadeOut('slow');
			} else if (result['result'] === 'FAILED') {
				console.log('remove_story: FAILED!')
			} else {
				console.log('Something gona wrong..')
			}
		},
		error: function (result) {
			console.log('Connection error')
		}
	});
}