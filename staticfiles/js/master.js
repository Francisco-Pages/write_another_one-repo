function authorClick(authorClicked){
    console.log("click registered")
    const author = authorClicked
    $.ajax({
        type: 'POST',
        url: '{% url "author:follow_author" %}',
        data: {
            authorpk: authorClicked,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json) {
            document.getElementById(`${author}-follower-count`).innerHTML = json['result'];
            document.getElementById(`${author}-following-icon`).innerHTML = json['followed']
            console.log('success')
        },
        error: function(xhr, errmsg, err) {
            
        }
    });
}
function followTag(tagClicked){
    const tag = tagClicked
    $.ajax({
        type: 'POST',
        url: '{% url "story:follow_tag" %}',
        data: {
            tagpk: tagClicked,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json) {
            document.getElementById(`${tag}-follower-count`).innerHTML = json['result'];
            document.getElementById(`${tag}-followed`).innerHTML = json['followed']
            console.log('success')
        },
        error: function(xhr, errmsg, err) {
            
        }
    });
}

function pinList(listClicked){
    const list = listClicked
    
    $.ajax({
        type: 'POST',
        url: '{% url "story:pin_list" %}',
        data: {
            listpk: listClicked,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json) {
            document.getElementById(`${list}-pin-count`).innerHTML = json['result'];
            document.getElementById(`${list}-pinned`).src = json['pinned']
            console.log('success')
        },
        error: function(xhr, errmsg, err) {
            
        }
    });
}

function addStoryToList(objectClicked){
    const separator = objectClicked.indexOf('|')
    const story = objectClicked.slice(0,separator);
    const list = objectClicked.slice(separator+1);
    console.log(story)
    console.log(list)
    $.ajax({
        type: 'POST',
        url: '{% url "story:add_story_to_list" %}',
        data: {
            storypk: story,
            listpk: list,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json){
            document.getElementById(`${story}-in-${list}`).src = json['added']
            console.log('success')
        },
        error: function(xhr, errmsg, err){
            console.log(`${xhr} | ${errmsg} | ${err}`)
        }
    })
}

function addStoryToThisList(objectClicked){
    const separator = objectClicked.indexOf('|')
    const story = objectClicked.slice(0,separator);
    const list = objectClicked.slice(separator+1);
    console.log(story)
    console.log(list)
    console.log(separator)
    $.ajax({
        type: 'POST',
        url: '{% url "story:add_story_to_list" %}',
        data: {
            storypk: story,
            listpk: list,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json){
            document.getElementById(`${story}-in-this-${list}`).src = json['added_in_list']
            console.log('success')
        },
        error: function(xhr, errmsg, err){
            console.log(`${xhr} | ${errmsg} | ${err}`)
        }
    })
}

function storyClick(storyClicked){
    const story = storyClicked
    console.log(story)
    $.ajax({
        type: 'POST',
        url: '{% url "story:like_story_ajax" %}',
        data: {
            storypk: storyClicked,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        cache: false,
        success: function(json) {
            document.getElementById(`${story}-like-count`).innerHTML = json['result'];
            document.getElementById(`${story}-like-story-icon`).src = json['liked']
            console.log('success')
        },
        error: function(xhr, errmsg, err) {
            
        }
    });
}




