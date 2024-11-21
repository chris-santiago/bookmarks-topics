import typing as T

import bs4
import hydra
import polars as pl

import bookmarks_topics._common as C


class BookmarkReader:
    def __init__(self, filepath: str):
        self.filename = filepath
        self.soup = None
        self.bookmarks = []

    def make_soup(self) -> "BookmarkReader":
        with open(self.filename, "r") as file:
            self.soup = bs4.BeautifulSoup(file, "lxml")
        return self

    def get_folder(self, folder_name: str):
        return [
            C.Bookmark(bookmark.text, bookmark.get("href"))
            for bookmark in self.soup.find("h3", string=folder_name)
            .find_next("dl")
            .find_all("a")
        ]

    def get_all(self):
        return [
            C.Bookmark(bookmark.text, bookmark.get("href"))
            for bookmark in self.soup.find_all("a")
        ]

    def get(self, folders: T.Optional[T.List[str]] = None) -> "BookmarkReader":
        if not self.soup:
            self.make_soup()
        if folders:
            for folder in folders:
                self.bookmarks.extend(self.get_folder(folder))
            return self
        self.bookmarks.extend(self.get_all())
        return self

    def to_polars(self) -> pl.DataFrame:
        return pl.from_records(self.bookmarks)


@hydra.main(config_path="../../conf", config_name="config", version_base="1.3")
def main(cfg):
    reader = BookmarkReader(cfg.bookmarks.input_path)
    reader.get(folders=cfg.bookmarks.folders)
    C.to_pickle(reader.bookmarks, cfg.bookmarks.output_path)


if __name__ == "__main__":
    main()
