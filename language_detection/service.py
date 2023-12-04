import asyncio
import logging

import bentoml
from detect_script import detect_script
from fasttext_runner import FastTextRunnable

indiclid_bert_runner = bentoml.models.get("indiclid-bert:latest").to_runner(
    name="indiclid_bert"
)
xlm_roberta_runner = bentoml.models.get(
    "xlm-roberta-base-language-detection:latest"
).to_runner(name="xlm_roberta_base_language_detection")
indiclid_ftn = bentoml.Runner(
    FastTextRunnable,
    name="indiclid_ftn",
    runnable_init_params={
        "model_file": str("./data/indiclid-ftn/model_baseline_roman.bin"),
    },
)

svc = bentoml.Service(
    name="language-detection",
    runners=[indiclid_bert_runner, xlm_roberta_runner, indiclid_ftn],
)


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def latin_script_indic_lid(text: str) -> dict[str, any]:
    script = detect_script(text)
    logging.info(f"INPUT = {text}")
    logging.info(f"SCRIPT = {script}")
    if script in ("Latin"):
        result = await indiclid_bert_runner.async_run([text])
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def indic_script_indic_lid(text: str) -> dict[str, any]:
    script = detect_script(text)
    logging.info(f"INPUT = {text}")
    logging.info(f"SCRIPT = {script}")
    if script not in ("Latin", "Other"):
        result = await indiclid_ftn.async_run([text])
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def general_lid(text: str) -> dict[str, any]:
    script = detect_script(text)
    logging.info(f"INPUT = {text}")
    logging.info(f"SCRIPT = {script}")
    if script in ("Latin", "Other"):
        result = await xlm_roberta_runner.async_run([text])
        return result
    else:
        return {"label": "UNKNOWN", "score": 0}


@svc.api(input=bentoml.io.Text(), output=bentoml.io.JSON())
async def combined_lid(text: str) -> dict[str, any]:
    script = detect_script(text)
    logging.info(f"INPUT = {text}")
    logging.info(f"SCRIPT = {script}")
    with bentoml.monitor("combined_lid_monitor") as mon:
        mon.log(text, name="text", role="input", data_type="string")
        mon.log(script, name="script", role="property", data_type="string")
        if script in ("Latin", "Other"):
            prediction_coroutines = [
                xlm_roberta_runner.async_run([text]),
                indiclid_bert_runner.async_run([text]),
            ]
            predictions = await asyncio.gather(*prediction_coroutines)
            mon.log(
                predictions[0][0],
                name="prediction_general_lid",
                role="output",
                data_type="json",
            )
            mon.log(
                predictions[1][0],
                name="prediction_latin_script_indic_lid",
                role="output",
                data_type="json",
            )
            if predictions[1][0]["label"] != "hi":
                return predictions[0]
            else:
                return predictions[1]
        elif script not in ("Latin", "Other"):
            result = await indiclid_ftn.async_run([text])
            mon.log(
                result[0],
                name="prediction_indic_script_indic_lid",
                role="output",
                data_type="json",
            )
            return result
        else:
            return {"label": "UNKNOWN", "score": 0}
