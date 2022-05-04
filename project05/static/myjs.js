function toggle_like(post_id, type) {
    // console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='${type}']`)
    let $i_like = $a_like.find("i")
    let a_box = {"heart":"fa-heart", "star":"fa-star", "thumbs-up":"fa-thumbs-up"}
    let b_box = {"heart":"fa-heart-o", "star":"fa-star-o", "thumbs-up":"fa-thumbs-o-up"}
    if ($i_like.hasClass(a_box[type])) {
        console.log("실행1")
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")

                $i_like.addClass(b_box[type]).removeClass(a_box[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        console.log("실행2")
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")

                // if(type == 'heart'){
                //     $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                // }else if(type == 'star'){
                //     $i_like.addClass("fa-star").removeClass("fa-star-o")
                // }else if(type == 'thumbs-up'){
                //     $i_like.addClass("fa-thumbs-up").removeClass("fa-thumbs-o-up")
                // }
                $i_like.addClass(a_box[type]).removeClass(b_box[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    }
}

function post() { //포스팅 함수
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }
    })
}

// 포스팅 시간 나타내기
function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

// 좋아요 개수 양식
function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"  //소수 첫째 자리까지 표시
    }
    if (count == 0) {
        return ""
    }
    return count
}

// 포스팅 카드 만들기
function get_posts(username) {
    if (username==undefined) {
        username=""
    }
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                console.log(posts[0]['count_thumb'])
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post) // 포스팅된 시간 계산
                    let class_heart = post['heart_by_me'] ? "fa-heart" : "fa-heart-o" // 내가 좋아요 했는지 여부
                    let class_star = post['star_by_me'] ? "fa-star" : "fa-star-o" // 내가 star 했는지 여부
                    let class_thumb = post['thumb_by_me'] ? "fa-thumbs-up" : "fa-thumbs-o-up" // 내가 thumb 했는지 여부

                    let html_temp = `<div class="box" id="${post["_id"]}">
                                                    <article class="media">
                                                        <div class="media-left">
                                                            <a class="image is-64x64" href="/user/${post['username']}">
                                                                <img class="is-rounded" src="/static/${post['profile_pic_real']}" alt="Image">
                                                            </a>
                                                        </div>
                                                        <div class="media-content">
                                                            <div class="content">
                                                                <p>
                                                                    <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                                                    <br>
                                                                    ${post['comment']}
                                                                </p>
                                                            </div>
                                                            <nav class="level is-mobile">
                                                                <div class="level-left">
                                                                    <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                                                        <span class="icon is-small">
                                                                            <i class="fa ${class_heart}"aria-hidden="true"></i>
                                                                        </span>&nbsp;
                                                                        <span class="like-num">${num2str(post['count_heart'])}</span>
                                                                    </a>
                                                                    <a class="level-item is-sparta" aria-label="star" onclick="toggle_like('${post['_id']}', 'star')">
                                                                        <span class="icon is-small">
                                                                            <i class="fa ${class_star}"aria-hidden="true"></i>
                                                                        </span>&nbsp;
                                                                        <span class="like-num">${num2str(post['count_star'])}</span>
                                                                    </a>
                                                                    <a class="level-item is-sparta" aria-label="thumbs-up" onclick="toggle_like('${post['_id']}', 'thumbs-up')">
                                                                        <span class="icon is-small">
                                                                            <i class="fa ${class_thumb}"aria-hidden="true"></i>
                                                                        </span>&nbsp;
                                                                        <span class="like-num">${num2str(post['count_thumb'])}</span>
                                                                    </a>
                                                                </div>
                                                            </nav>
                                                        </div>
                                                    </article>
                                                </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}
