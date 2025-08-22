function like(slug, token) {
    var likeBtn = document.getElementById('likeBtn');
    var likeIcon = document.getElementById('likeIcon');
    var likeCount = document.getElementById('likeCount');

    $.post(`/post/${slug}/like`, {csrfmiddlewaretoken: token}).then((response) => {
        if (response.liked) {
            likeBtn.className = 'btn btn-outline-danger like-btn liked';
            likeIcon.className = 'fas fa-heart';
            likeCount.innerText = Number(likeCount.innerText) + 1;
        } else {
            likeBtn.className = 'btn btn-outline-danger like-btn';
            likeIcon.className = 'far fa-heart';
            likeCount.innerText = Number(likeCount.innerText) - 1;
        }
    })
}