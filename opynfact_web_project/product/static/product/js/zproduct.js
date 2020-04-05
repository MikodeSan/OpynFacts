function set_favorite(code, flag) {

    event.preventDefault();
    event.stopPropagation();

    let data = new FormData();
    data.append('code', code);
    data.append('favorite', flag);

    zajaxPost(parse_favorite_url, data, favorite_assert, test, false);

    console.log("Date:", Date.now());

}


/* Assert favorite setting */
async function favorite_assert(reply_json) {
    console.log('favorite_assert !');

    console.log(reply_json);
    let data = JSON.parse(reply_json);
}

/* test */
const test = () => {

    console.log('test !');
};