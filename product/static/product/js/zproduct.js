/* Set favorite state for the specified product */
function set_favorite(code, flag) {

    event.preventDefault();
    event.stopPropagation();

    let data = new FormData();
    // console.log(typeof code, code);
    // console.log(typeof flag, flag);

    data.append('code', code);
    data.append('favorite', flag);

    zajaxPost(parse_favorite_url, data, favorite_assert, ack, false);
}


/* Assert favorite setting */
async function favorite_assert(reply_json) {

    let data = JSON.parse(reply_json);
    // console.log(typeof data.code);
    // console.log(typeof data.favorite);

    /* Change favorite image state and callback flag */
    let cur_a = document.getElementById(data.code);

    /* [TODO]: DRY to optimize */

    if (data.favorite) {
        image_type = 'far';
    } else {
        image_type = 'fas';
    }

    cur_a.innerHTML = "<i class='" + image_type + " fa-1x fa-heart mb-4'></i>";

    // let s = arguments.callee.name + '(' + data.code + ', ' + data.favorite + ')';
    cur_a.setAttribute('data-state', data.favorite);
}

/* test */
const ack = () => {

    // console.log('Favorite setting Ack !');
    // console.log('function name:' + arguments.callee.name);
};