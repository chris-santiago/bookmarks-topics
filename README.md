# bookmarks-topics

This project is a continuation of the stale [bookmarks_clustering](https://github.com/chris-santiago/bookmarks_clustering) project. It's updated to use newer embedding and generative models, mostly via [BERTopic](https://maartengr.github.io/BERTopic/index.html) library.

# Usage

## Prerequisites

1. This project uses [Task](https://taskfile.dev/) to run and manage tasks, so you'll need to first install that on your machine.
2. This project uses OpenAI's API. You'll need an API key from OpenAI; place it in a `.env` file within this project's root directory. The key should be `OPENAI_KEY` and the value is your API key. For example:

```toml
OPENAI_KEY=sk-proj-_mySuperSecretOpenAIkey
```

3. Export your bookmarks to an HTML file. *Note: this project used Google Chrome bookmarks.*

## Setup

Clone this repo and install the project and dependencies:

```bash
git clone https://github.com/chris-santiago/bookmarks-topics.git
cd bookmarks-topics
conda env create -f environment.yaml
pip install .
```

## Quick Start

Once you've completed the prerequisites and setup the project environment, you can run the entire pipeline using the command:

```bash
task cluster-bookmarks -- "bookmarks.input_path=your/path/to/bookmarks.html"
```

This will parse your bookmarks file and fetch content from all the bookmarked URLs, before running the clustering algorithm. **You may not want to organize ALL of your bookmarks, but rather a subset.** In this case, you can pass a comma-separated list of specific folders:

```bash
task cluster-bookmarks -- "bookmarks.input_path=your/path/to/bookmarks.html" "bookmarks.folders=My first folder,My second folder"
```

Once complete, your re-organized bookmarks are placed within a newly-created `ouputs/topics/` directory, within this project's root directory. That directory is organized by date and time; find the folder that corresponds with your most recent run and import the `new_bookmarks.html` file back into your browser. You can also view a breakdown of bookmarks and topics in the `bookmarks_topics.json` file, within that same directory.

### Example Output

#### HTML

```html
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
<DT><H3>JavaScript D3.js</H3>
<DL><p>
    <DT><A HREF="https://stackoverflow.com/questions/32205507/moving-the-axes-in-d3-js">javascript - Moving the axes in d3.js - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/25158688/d3-csv-accessor-function-for-loop">javascript - D3.csv accessor function for loop - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/33482812/javascript-take-every-nth-element-of-array">Javascript: take every nth Element of Array - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/23227991/how-to-add-in-zero-values-into-a-time-series-in-d3-js-javascript">How to add in zero values into a time series in d3.js / JavaScript - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/1187518/how-to-get-the-difference-between-two-arrays-in-javascript">How to get the difference between two arrays in JavaScript? - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/16179021/d3-js-specify-text-for-x-axis">javascript - d3.js Specify text for x-axis - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/43646573/d3-get-attributes-from-element/43646752">javascript - D3 get attributes from element - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/28572015/how-to-select-unique-values-in-d3-js-from-data/28572315">javascript - How to select unique values in d3.js from data - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/10644778/targeting-nested-elements-with-css">html - Targeting nested elements with CSS - Stack Overflow</A>
    <DT><A HREF="https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference/5044#5044">MathJax basic tutorial and quick reference - Mathematics Meta Stack Exchange</A>
    <DT><A HREF="https://stackoverflow.com/questions/46945784/how-to-debug-javascript-in-visual-studio-code-with-live-server-running">How to Debug JavaScript in Visual Studio Code with live-server Running - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/52788743/intellij-error-java-release-version-10-not-supported/54963753">jetbrains ide - IntelliJ: Error: java: release version 10 not supported - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/20197961/reversed-y-axis-d3">javascript - reversed Y-axis D3 - Stack Overflow</A>
    <DT><A HREF="https://stackoverflow.com/questions/49281258/plot-multiple-lines-in-a-for-loop-in-d3">d3.js - Plot multiple lines in a for loop in d3 - Stack Overflow</A>
</DL><p>
```

#### JSON

```json
[
  {
    "url": "https://appliedcausalinference.github.io/aci_book",
    "title": "Applied Causal Inference",
    "topic": "Bayesian Causal Inference"
  },
  {
    "url": "https://astral.sh/blog/u",
    "title": "uv: Python packaging in Rust",
    "topic": "Python Development Tools"
  },
  {
    "url": "https://bayesiancomputationbook.com/markdown/chp_01.htm",
    "title": "1. Bayesian Inference \u2014 Bayesian Modeling and Computation in Python",
    "topic": "Bayesian Causal Inference"
  }
]
```

# Tinkering

This project is configured using [Hydra](https://hydra.cc/docs/intro/), and current configs are found in the `conf` directory. You can modify behavior by changing these configs, directly, or by overriding on the command line.

| Config | Use                                                       | Path                      |
|--------|-----------------------------------------------------------|---------------------------|
| Main   | Main configuration file. Use this to tune the topic model | `conf/config.yaml`        |
| Prompt | Configure LLM prompts.                                    | `conf/prompt/*`           |
| Paths  | Configure your local paths.                               | `conf/paths/default.yaml` |
| Hydra  | Configure hydra.                                          | `conf/hydra/default.yaml` |

## CLI Override

You can [override](https://hydra.cc/docs/advanced/override_grammar/basic/) much of the configuration directly from the command line by passing Hydra overrides after `--` in the command. For example:

```bash
task cluster-bookmarks -- "topics.topic_model.top_n_words=5"
```

## Tasks

You can, of course, also run individual tasks that will execute corresponding Python modules. This is useful when tuning the topic model (`task: topics`) and want to avoid fetching and parsing HTML from your bookmarked URLs.

```bash
task: Available tasks for this project:
* bookmarks:               Read bookmarks file
* check-config:            Check Hydra configuration
* cluster-bookmarks:       Run entire bookmarks clustering pipeline.
* fetch-html:              Get bookmarks raw html
* lint:                    Check source code for errors (will run before tasks)
* parse-html:              Parse bookmarks raw html
* topics:                  Get topics
```
