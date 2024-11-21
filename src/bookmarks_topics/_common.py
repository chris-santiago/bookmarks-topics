import pickle
from collections import namedtuple
import json


Bookmark = namedtuple("Bookmark", ["title", "url"])
Website = namedtuple("Website", ["title", "url", "content"])
Topic = namedtuple("BookmarkTopic", ["title", "url", "content", "topic"])


def to_pickle(obj: object, file_path: str):
    with open(file_path, "wb") as fp:
        pickle.dump(obj, fp)


def from_pickle(file_path: str):
    with open(file_path, "rb") as fp:
        return pickle.load(fp)


def to_json(obj: object, file_path: str):
    with open(file_path, "w") as fp:
        json.dump(obj, fp)


def to_txt(text: str, file_path: str):
    with open(file_path, "w") as fp:
        fp.write(text)
