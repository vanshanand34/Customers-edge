function truncateWords(text, truncateLength) {
  const words = text.split(" ");
  if (words.length <= truncateLength) return text;
  let truncatedStr = "";
  for (let i = 0; i < truncateLength; i++) {
    truncatedStr += words[i] + " ";
  }
  return truncatedStr + "...";
}

function parseSearchResults() {
  let searchResultsCollections = [];
  const search_text = searchText;
  const searchTable = document.getElementById("search-table-body");
  const websocketUrl = "ws://" + window.location.host + "/ws/search-results/";
  const searchResultSocket = new WebSocket(websocketUrl);

  searchResultSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data);
    if (data?.message?.includes("No results found")) {
      const tableRow = document.createElement("tr");
      tableRow.innerHTML = `
          <td class="prod-name" data-value="${data.name}">
            No results found
          </td>
        `;
      searchTable.appendChild(tableRow);
      return;
    }
    // console.log(data);
    data.price = parseFloatCustom(data.price);
    data.rating = parseFloatCustom(data.rating);
    searchResultsCollections.push(data);
    const tableRow = document.createElement("tr");
    const truncatedText = truncateWords(data.name, 8);

    tableRow.innerHTML = `
        <td class="prod-name" data-value="${data.name}" title="${data.name}">
          ${truncatedText}
        </td>
        <td>${data.price}</td>
        <td>${data.rating}</td>
        <td>${data.platform}</td>
        <td>
        <a href="${data.product_url}">
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="18" height="18" viewBox="0 0 128 128">
            <path d="M 84 11 C 82.3 11 81 12.3 81 14 C 81 15.7 82.3 17 84 17 L 106.80078 17 L 60.400391 63.400391 C 59.200391 64.600391 59.200391 66.499609 60.400391 67.599609 C 61.000391 68.199609 61.8 68.5 62.5 68.5 C 63.2 68.5 63.999609 68.199609 64.599609 67.599609 L 111 21.199219 L 111 44 C 111 45.7 112.3 47 114 47 C 115.7 47 117 45.7 117 44 L 117 14 C 117 12.3 115.7 11 114 11 L 84 11 z M 24 31 C 16.8 31 11 36.8 11 44 L 11 104 C 11 111.2 16.8 117 24 117 L 84 117 C 91.2 117 97 111.2 97 104 L 97 59 C 97 57.3 95.7 56 94 56 C 92.3 56 91 57.3 91 59 L 91 104 C 91 107.9 87.9 111 84 111 L 24 111 C 20.1 111 17 107.9 17 104 L 17 44 C 17 40.1 20.1 37 24 37 L 69 37 C 70.7 37 72 35.7 72 34 C 72 32.3 70.7 31 69 31 L 24 31 z"></path>
          </svg>
        </a>
      </td>`;

    searchTable.appendChild(tableRow);
    const rowIndex = searchTable.children.length - 1;
    const delay = rowIndex * 60;
    addAnimationClass(tableRow, delay);
  };

  function addAnimationClass(tableRow, delay) {
    setTimeout(() => {
      tableRow.classList.add("fade-in");
    }, delay);
  }

  searchResultSocket.onopen = function () {
    searchResultSocket.send(
      JSON.stringify({
        search_text: search_text,
      }),
    );
  };
}

function parseFloatCustom(num) {
  if (!num) {
    return 0.0;
  }

  if (typeof num === "string") {
    num = num.replace(",", "");
  }
  return parseFloat(num);
}

parseSearchResults();
