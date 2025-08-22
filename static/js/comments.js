$(document).ready(function () {

    function bindReplyButtons() {
        $(document).off("click", ".reply-btn");
        $(document).on("click", ".reply-btn", function () {
            const commentDiv = $(this).closest(".comment");
            const commentId = commentDiv.data("id");
            const username = commentDiv.data("username");

            $("#parentId").val(commentId);
            $("#commentText").attr("placeholder", `Replying to ${username}...`);
            $("#commentText").focus();

            $('html, body').animate({
                scrollTop: $("#commentText").offset().top - 100
            }, 500);
        });
    }

    bindReplyButtons();

    $("#postCommentBtn").on("click", function () {
        const text = $("#commentText").val().trim();
        const parentId = $("#parentId").val();

        if (!text) return;

        const slug = $(this).data("slug");
        const token = $(this).data("token");

        $.post(`/post/detail/${slug}`, {
            csrfmiddlewaretoken: token,
            text: text,
            parent_id: parentId || null
        }).then(response => {
            if (response.success) {
                const newComment = `<div class="comment ${parentId ? 'reply' : ''}" 
                                        id="comment-${response.comment_id}" 
                                        data-id="${response.comment_id}" 
                                        data-username="${response.username}">
                                        <div class="comment-header">
                                            <strong>${response.username}</strong> · just now
                                        </div>
                                        <div class="comment-body">${response.text}</div>
                                        ${parentId ? '' : `
                                        <div class="comment-actions">
                                            <button class="btn btn-sm btn-outline-primary reply-btn">Reply</button>
                                        </div>
                                        <div class="replies"></div>
                                        `}
                                    </div>`;

                if (parentId) {
                    let parentComment = $(`#comment-${parentId}`);
                    parentComment.find('.replies').append(newComment);
                } else {
                    $(".comments-section .add-comment").before(newComment);
                }

                bindReplyButtons();

                $("#commentText").val("");
                $("#commentText").attr("placeholder", "Write a comment...");
                $("#parentId").val("");
            }
        });
    });

});
