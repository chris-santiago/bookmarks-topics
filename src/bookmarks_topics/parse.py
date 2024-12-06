import bs4
import hydra

import bookmarks_topics._common as C


def get_text_content(raw_html):
    try:
        soup = bs4.BeautifulSoup(raw_html, "lxml")
        text = [x.text for x in soup.find_all("p")]
        text.insert(0, soup.title.text)
        return " ".join(text)
    except Exception:
        return None


@hydra.main(config_path="../../conf", config_name="config", version_base="1.3")
def main(cfg):
    bookmarks_data = C.from_pickle(cfg.bookmarks.output_path)
    raw_html = C.from_pickle(cfg.parse.input_path)
    text_content = [get_text_content(doc) for doc in raw_html]
    C.to_pickle(text_content, cfg.parse.output_path)
    websites = [
        C.Website(
            title=x[0].title,
            url=x[0].url,
            content=x[1],
            folders=[f for f in x[0].folders if f not in cfg.parse.drop_folders],
        )
        for x in zip(bookmarks_data, text_content)
    ]
    C.to_pickle(websites, cfg.parse.websites_path)


if __name__ == "__main__":
    main()
