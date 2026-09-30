const recentSearchesElement = document.getElementById("recent-searches");

document.addEventListener("DOMContentLoaded", function () {
  if (!recentSearchesElement) return;

  let recentSearchesHTML = `
    <div class="recent-search-header">
      <span>Recent searches</span>
    </div>
  `;

  if (!recentSearches || recentSearches.length === 0) {
    recentSearchesHTML += `
      <div class="recent-search-empty">
        <span class="recent-search-empty-icon">⌕</span>
        No recent searches
      </div>
    `;
  } else {
    for (let i = 0; i < recentSearches.length; i++) {
      const searchText = recentSearches[i].text;

      recentSearchesHTML += `
        <div
          class="recent-search-item"
          id="recent-search-item-${i}"
          data-index="${i}"
          data-value="${searchText}"
          tabindex="0"
          onClick="document.getElementById('search-text').value='${searchText}'; toggleRecentSearchesDisplay(); document.getElementById('search-form').submit();"
        >
          <svg
            class="recent-search-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              d="M12 8v4l2.5 1.5"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <path
              d="M12 21a9 9 0 1 0-8.2-5.3"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />
          </svg>

          <span class="recent-search-text">
            ${searchText}
          </span>
        </div>
      `;
    }
  }

  recentSearchesElement.innerHTML = recentSearchesHTML;
});

function toggleRecentSearchesDisplay() {
  if (recentSearchesElement.style.display === "block") {
    recentSearchesElement.style.display = "none";
  } else {
    recentSearchesElement.style.display = "block";
  }
}

document.getElementById("search-text").addEventListener("click", function () {
  toggleRecentSearchesDisplay();
});

document.addEventListener("click", function (event) {
  const searchInput = document.getElementById("search-text");
  if (
    !recentSearchesElement.contains(event.target) &&
    event.target !== searchInput
  ) {
    recentSearchesElement.style.display = "none";
  }
});

document
  .getElementById("search-text")
  .addEventListener("keydown", function (event) {
    if (event.key === "Escape" || event.key === "Esc") {
      recentSearchesElement.style.display = "none";
    }
  });
