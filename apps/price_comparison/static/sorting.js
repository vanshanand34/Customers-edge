document.addEventListener("DOMContentLoaded", () => {
  window.onresize = (e) => {
    addWordTruncation();
  };

  addWordTruncation();

  function addWordTruncation() {
    const elements = document.getElementsByClassName("prod-name");
    for (const element of elements) {
      const currVal = element.dataset.value;
      element.innerHTML = truncateWords(currVal, 8);
    }
  }

  function compareByPrice(prod1, prod2) {
    return parseFloat(prod1.price) < parseFloat(prod2.price) ? -1 : 1;
  }

  function compareByRating(prod1, prod2) {
    return parseFloat(prod1.rating) < parseFloat(prod2.rating) ? -1 : 1;
  }

  function sortByPrice() {
    return searchResults.sort(compareByPrice);
  }

  function sortByRating() {
    return searchResults.sort(compareByRating);
  }

  function updateTableContent(searchResults) {
    const t = document.getElementById("search-table-body");
    const rows = t.rows;

    for (let i = 0; i < rows.length; i++) {
      const product = searchResults[i];
      rows[i].children[0].children[0].href = product.product_url;
      rows[i].children[0].children[0].children[0].src = product.image_src;
      rows[i].children[0].children[0].children[0].alt = product.product_name;
      rows[i].children[1].textContent = truncateWords(product.name, 8);
      rows[i].children[2].textContent = parseFloatCustom(product.price);
      rows[i].children[3].innerHTML = `
        <span class="rating-star">★</span>
        <span class="rating-value">${parseFloatCustom(product.rating)}</span>
        `;
      rows[i].children[4].innerHTML = `
        <span class="platform-badge">
            ${product.platform}
        </span>`;
      rows[i].children[5].children[0].href = product.product_url;
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

  document.getElementById("sort-price").addEventListener("click", () => {
    if (isPriceSorted(searchResults)) {
      updateTableContent(searchResults.reverse());
    } else {
      searchResults = sortByPrice();
      updateTableContent(searchResults);
    }
  });

  document.getElementById("sort-rating").addEventListener("click", () => {
    if (isRatingSorted(searchResults)) {
      updateTableContent(searchResults.reverse());
    } else {
      searchResults = sortByRating();
      console.log(searchResults);
      updateTableContent(searchResults);
    }
  });
});
