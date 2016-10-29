 function photoLike(photoPk, likeType){
        $.ajax({
            method: 'POST',
            url: '/album/ajax/like/' + photoPk + '/' + likeType + '/',
        })
            .done(function(response){
                var likeCount = response.like_count;
                var dislikeCount = response.dislike_count;
                var spanLikeCount = $('#photo-' + photoPk + '-like-count');
                var userLike = response.user_like;
                var userDislike = response.user_dislike;
                spanLikeCount.text(likeCount);
                var spanDisLikeCount = $('#photo-' + photoPk + '-dislike-count');
                spanDisLikeCount.text(dislikeCount);

                var btnLike = $('#btn-photo-')
            })
            .fail(function(response){
                console.log(response);
            });
    }