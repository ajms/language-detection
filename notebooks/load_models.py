# %%
import bentoml  # noqa F401
import fasttext
import torch
from transformers import AutoTokenizer, pipeline

from language_detection.indic_mapping import IndicLID_lang_code_dict_reverse
from language_detection.utils.path_helpers import get_project_root

device = torch.device(0 if torch.cuda.is_available() else "cpu")
input_texts = [
    "എന്റെ പേര് അലക്സ് സിബു",
    "Jürgen ist ein schräger Vogel",
    "namaste! main plantix sahaayak hoon aur main yahaan aapake paudhon kee samasyaon mein aapakee madad karane ke lie hoon. kya aap adhik jaanakaaree pradaan kar sakate hain taaki main aapako behatar sujhaav de sakoon. jaise ki kya aap ke soybean me kuch kit ya aur pareshani hai",
]
# %%
# XLM-RoBERTa
pipe = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection",
    device=device,
)
print(pipe.predict(input_texts))
# %%
# IndicLID-BERT for latin letters Indian
IndicLID_BERT = torch.load(
    get_project_root() / "data/indiclid-bert/basline_nn_simple.pt",
    map_location=device,
)
IndicLID_BERT.config.update(
    {
        "id2label": IndicLID_lang_code_dict_reverse,
        "label2id": {v: k for k, v in IndicLID_lang_code_dict_reverse.items()},
    },
)
IndicLID_BERT.eval()
IndicLID_BERT_tokenizer = AutoTokenizer.from_pretrained(
    "ai4bharat/IndicBERTv2-MLM-only",
)
pipe2 = pipeline(
    "text-classification",
    model=IndicLID_BERT,
    tokenizer=IndicLID_BERT_tokenizer,
    device=device,
)

prediction = pipe2.predict(input_texts)
print(prediction)
pipe2.save_pretrained(get_project_root() / "data/indiclid-bert/pipeline")
# %%
# IndicLID-FTN for Indian scripts
IndicLID_FTN = fasttext.load_model(
    str(get_project_root() / "data/indiclid-ftn/model_baseline_roman.bin")
)
prediction, score = IndicLID_FTN.predict(input_texts)
print(prediction)
print(score)

# %%
bentoml.transformers.save_model(
    name="xlm-roberta-base-language-detection",
    pipeline=pipe,
    task_name="text-classification",
    signatures={  # model signatures for runner inference
        "predict": {
            "batchable": True,
            "batch_dim": 0,
        }
    },
)
bentoml.transformers.save_model(
    name="indiclid-bert",
    pipeline=pipe2,
    task_name="text-classification",
    signatures={  # model signatures for runner inference
        "predict": {
            "batchable": True,
            "batch_dim": 0,
        }
    },
)
# bentoml.transformers.import_model(
#     name="indiclid-bert",
#     model_name_or_path=get_project_root() / "data/indiclid-bert/pipeline",
#     task_name="text-classification",
# )

# %%
