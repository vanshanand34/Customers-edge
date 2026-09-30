from typing import TypedDict

from django.contrib.sessions.backends.base import SessionBase


class SearchHistory(TypedDict):
    text: str
    url: str


class SearchHistoryHelper:
    """
    A helper class for managing search history in the session.
    """

    DEFAULT_IMAGE_URL = "https://t4.ftcdn.net/jpg/05/97/47/95/360_F_597479556_7bbQ7t4Z8k3xbAloHFHVdZIizWK1PdOo.jpg"

    @staticmethod
    def get_search_history(session: SessionBase) -> list[SearchHistory]:
        return session.get("search_history", [])

    @staticmethod
    def add_search_history(
        session: SessionBase,
        search_text: str,
        url: str = DEFAULT_IMAGE_URL,
    ):
        search_history: list[SearchHistory] = session.get("search_history", [])
        if not any(entry["text"] == search_text for entry in search_history):
            search_history.append({"text": search_text, "url": url})
        session["search_history"] = search_history

    @staticmethod
    def update_search_url(session: SessionBase, search_text: str, url: str):
        """
        Update the URL for a specific search text in the session's search history.
        If the search text is found, its URL will be updated with the provided URL.
        """
        search_history: list[SearchHistory] = session.get("search_history", [])
        for i, entry in enumerate(search_history):
            if entry["text"] == search_text:
                search_history[i]["url"] = url
                break
        print(
            f"Updated search history for '{search_text}' with URL: {url}: {search_history}"
        )
        session["search_history"] = search_history

    @staticmethod
    def update_search_url_if_url_empty(
        session: SessionBase, search_text: str, url: str
    ):
        """
        Update the URL for a specific search text in the session's search history only if the URL is currently empty.
        """
        search_history: list[SearchHistory] = session.get("search_history", [])
        for i, entry in enumerate(search_history):
            if entry["text"] == search_text and (
                not entry["url"]
                or entry["url"] == SearchHistoryHelper.DEFAULT_IMAGE_URL
            ):
                search_history[i]["url"] = url
                break

        session["search_history"] = search_history

        print(f"Updated search history: {search_history}")
