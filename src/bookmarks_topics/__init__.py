import pathlib

HERE = pathlib.Path(__file__).parent
REPO = HERE.parents[1]
TMP = REPO.joinpath("tmp")
TMP.mkdir(exist_ok=True)
