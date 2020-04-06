/* Set favorite state for the specified product */
function set_favorite(code, flag) {

    event.preventDefault();
    event.stopPropagation();

    let data = new FormData();
    console.log(typeof code, code);
    console.log(typeof flag, flag);

    data.append('code', code);
    data.append('favorite', flag);

    zajaxPost(parse_favorite_url, data, favorite_assert, ack, false);
    // console.log("Date:", Date.now());
}


/* Assert favorite setting */
async function favorite_assert(reply_json) {
    console.log('favorite_assert !');

    console.log(reply_json);
    let data = JSON.parse(reply_json);
    console.log(typeof data.code);
    console.log(typeof data.favorite);

    /* Change favorite image state and callback flag */
    let cur_a = document.getElementById(data.code);

    /* [TODO]: DRY to optimize */

    console.log(data.favorite);
    if (data.favorite) {
        image_type = 'far';
    } else {
        image_type = 'fas';
    }
    console.log(image_type);

    let new_a = document.createElement('a');

    // cur_a.innerHTML = "<i class='" + image_type + "fa-1x fa-heart text-primary mb-4'></i>";
    cur_a.innerHTML = "<i class='" + image_type + " fa-1x fa-heart text-primary mb-4'></i>";

    let s = arguments.callee.name + '(' + data.code + ', ' + data.favorite + ')';
    console.log(s);
    // cur_a.id = parseInt(data.code);
    // cur_a.onclick = s;
    cur_a.setAttribute('data-state', data.favorite);

    // cur_a.parentNode.replaceChild(new_a, cur_a);
    console.log(cur_a);

}

/* test */
const ack = () => {

    console.log('Favorite setting Ack !');
    // console.log('function name:' + arguments.callee.name);
};