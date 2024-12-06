
import dataclasses
import pickle
from collections import namedtuple
import json
import typing as T


@dataclasses.dataclass
class Bookmark:
    title: str
    url: str
    folders: T.List[str]


@dataclasses.dataclass
class Website:
    title: str
    url: str
    content: str
    folders: T.List[str]


@dataclasses.dataclass
class Topic:
    title: str
    url: str
    content: str
    topic: str
    folders: T.List[str]


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
