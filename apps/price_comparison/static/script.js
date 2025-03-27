
document.addEventListener('DOMContentLoaded', () => {

    window.onresize = (e) => {
        addWordTruncation();
    };

    addWordTruncation();

    function addWordTruncation(){
        const elements = document.getElementsByClassName("prod-name");
            for(const element of elements) {
                const currVal = element.dataset.value;
                if(window.innerWidth <= 760){
                    element.innerHTML = truncateWords(currVal, 8);
                }else{
                    element.innerHTML = currVal;
                }
            };
    }

    function truncateWords(text, truncateLength){
        const words = text.split(" ");
        if (words.length <= truncateLength) return text;
        let truncatedStr = "";
        for(let i = 0; i < truncateLength; i++){
            truncatedStr += words[i] + " ";
        }
        return truncatedStr + "..."
    }

    function compareByPrice(prod1, prod2) {
        return (parseFloat(prod1.price) < parseFloat(prod2.price) ? -1 : 1);
    }

    function compareByRating(prod1, prod2) {
        return (parseFloat(prod1.rating) < parseFloat(prod2.rating) ? -1 : 1);
    }

    function sortByPrice() {
        return data.sort(compareByPrice)
    }

    function sortByRating() {
        return data.sort(compareByRating)
    }

    function updateTableContent(data) {
        const t = document.getElementById("sortable-table");

        for (let i = 1; i < t.rows.length; i++) {
            t.rows[i].children[0].innerHTML = data[i - 1].name;
            t.rows[i].children[1].innerHTML = data[i - 1].price;
            t.rows[i].children[2].innerHTML = data[i - 1].rating;
            t.rows[i].children[3].innerHTML = data[i - 1].platform;
            t.rows[i].children[4].children[0].href = data[i - 1].product_url;
        }
    }

    function isPriceSorted(prodArray) {

        for (let i = 1; i < prodArray.length; i++) {
            if (prodArray[i].price < prodArray[i - 1].price) return false;
        }
        return true;
    }

    function isRatingSorted(prodArray) {

        for (let i = 1; i < prodArray.length; i++) {
            if (prodArray[i].rating < prodArray[i - 1].rating) return false;
        }
        return true;
    }

    document.getElementById("sort-price").addEventListener('click', () => {

        if (isPriceSorted(data)) {
            updateTableContent(data.reverse());
        } else {
            data = sortByPrice();
            updateTableContent(data);
        }

    });

    document.getElementById("sort-rating").addEventListener('click', () => {

        if (isRatingSorted(data)) {
            updateTableContent(data.reverse());
        } else {
            data = sortByRating();
            console.log(data);
            updateTableContent(data);
        }

    });
})       