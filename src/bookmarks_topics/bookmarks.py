"""
>>> hydra.core.global_hydra.GlobalHydra.instance().clear()
>>> hydra.initialize(config_path='./conf', version_base="1.3")
>>> cfg = hydra.compose(config_name='config')
"""
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
            C.Bookmark(title=bookmark.text, url=bookmark.get("href"), folder=folder_name)
            for bookmark in self.soup.find("h3", string=folder_name)
            .find_next("dl")
            .find_all("a")
        ]

    def parse_folder(self, folder_name: str, n_parents: int = 2):
        folder = self.soup.find("h3", string=folder_name)
        results = []
        links = folder.find_next('dl').find_all('a')
        for link in links:
            folders_set = dict.fromkeys(
                [p.find_previous('h3').text for p in link.parents if p.find_previous('h3')])
            if n_parents is not None:
                folders = list(folders_set.keys())[:n_parents]
            else:
                folders = list(folders_set.keys())
            record = {
                "folders": folders,
                "title": link.text,
                "url": link.attrs["href"]
            }
            results.append(record)
        return results

    def get_all(self):
        return [
            C.Bookmark(bookmark.text, bookmark.get("href"))
            for bookmark in self.soup.find_all("a")
        ]

    def get(self, folders: T.Optional[T.List[str]] = None, keep_folder_hierarchy: bool = False, n_parents: int = 2) -> "BookmarkReader":
        if not self.soup:
            self.make_soup()
        if folders:
            if keep_folder_hierarchy:
                for folder in folders:
                    self.bookmarks.extend(self.parse_folder(folder, n_parents))
            else:
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
