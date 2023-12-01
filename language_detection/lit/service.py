import logging

import bentoml
from detect_script import detect_script
from fasttext_runner import FastTextRunnable

indiclid_bert_runner = bentoml.models.get("indiclid-bert:latest").to_runner()
xlm_roberta_runner = bentoml.models.get(
    "xlm-roberta-base-language-detection:latest"
).to_runner()
indiclid_ftn = bentoml.Runner(
    FastTextRunnable,
    name="my_runner_1",
    runnable_init_params={
        "model_file": "./indiclid-ftn/model_baseline_roman.bin",
    },
)

svc = bentoml.Service(
    name="language-detection",
    runners=[indiclid_bert_runner, xlm_roberta_runner, indiclid_ftn],
)


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def latin_script_indic_lid(text: str) -> str:
    logging.info(f"SCRIPT = {detect_script(text)}")
    if detect_script(text) in ("Latin"):
        result = await indiclid_bert_runner.async_run(text)
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def indic_script_indic_lid(text: str) -> str:
    logging.info(f"SCRIPT = {detect_script(text)}")
    if detect_script(text) not in ("Latin", "Other"):
        result = await indiclid_ftn.async_run(text)
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def general_lid(text: str) -> str:
    logging.info(f"SCRIPT = {detect_script(text)}")
    if detect_script(text) in ("Latin", "Other"):
        result = await xlm_roberta_runner.async_run(text)
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}
