import os

import bertopic as bt
import dotenv
import hydra
import openai
from sentence_transformers import SentenceTransformer

import bookmarks_topics._common as C

dotenv.load_dotenv()


def truncate_doc(doc: C.Website, n: int):
    try:
        return " ".join(doc.content.split())[:n]
    except AttributeError:
        return ""


def to_html(bookmarks, output_file="new_bookmarks.html"):
    # Start HTML structure for bookmarks file
    html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
    <DL><p>\n"""

    # Organize bookmarks by folder (topic)
    folders = {}
    for bookmark in bookmarks:
        folder = bookmark.get("topic", "Miscellaneous")
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(bookmark)

    # Convert folders and bookmarks to HTML format
    for folder, bookmarks in folders.items():
        html_content += f"<DT><H3>{folder}</H3>\n<DL><p>\n"
        for bookmark in bookmarks:
            url = bookmark["url"]
            title = bookmark["title"]
            html_content += f'    <DT><A HREF="{url}">{title}</A>\n'
        html_content += "</DL><p>\n"

    html_content += "</DL><p>"

    # Write HTML content to output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)


@hydra.main(config_path="../../conf", config_name="config", version_base="1.3")
def main(cfg):
    websites = C.from_pickle(cfg.topics.input_path)
    titles = [w.title for w in websites]
    content = [truncate_doc(x, cfg.topics.truncate) for x in websites]
    docs = [a + b for a, b in zip(titles, content)]

    openai_client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])

    embedding_model = hydra.utils.instantiate(cfg.topics.embedding_model)
    umap_model = hydra.utils.instantiate(cfg.topics.umap_model)
    ctfidf_model = hydra.utils.instantiate(cfg.topics.ctfidf_model)
    keybert_model = hydra.utils.instantiate(cfg.topics.keybert_model)
    openai_model = hydra.utils.instantiate(
        cfg.topics.openai_model,
        client=openai_client,
        prompt=cfg.prompt.openai
    )

    topic_model = hydra.utils.instantiate(
        cfg.topics.topic_model,
        embedding_model=embedding_model,
        umap_model=umap_model,
        ctfidf_model=ctfidf_model,
        representation_model=keybert_model,
    )
    topic_model.fit(docs)
    # For some reason passing representation_model as list doesn't run openai_model:
    # representation_model = [
    #     keybert_model,
    #     openai_model,
    # ]
    # Updating manually
    topic_model.update_topics(docs, representation_model=openai_model)
    topics = topic_model.get_topics()

    topic_names = [topics[t][0][0] for t in topic_model.topics_]
    bookmark_topics = [
        C.Topic(*a, b) for a, b in zip(websites, topic_names)
    ]
    records = [
        {
            "url": t.url,
            "title": t.title,
            "topic": t.topic,
        }
        for t in bookmark_topics
    ]

    C.to_json(records, cfg.topics.bookmark_topics_path)
    to_html(records, cfg.topics.bookmark_html_path)

    topic_info = topic_model.get_topic_info()
    topic_info.to_csv(cfg.topics.topic_info_path, index=False)

    try:
        topic_model.save(cfg.topics.model_pkl_path)
    except TypeError:
        topic_model.save(
            path=cfg.topics.model_pt_path,
            serialization="pytorch",
            save_embedding_model=True,
            save_ctfidf=True,
        )


if __name__ == "__main__":
    main()
