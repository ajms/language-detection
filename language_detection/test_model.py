# Use a pipeline as a high-level helper
import fasttext
import torch
from indic_mapping import IndicLID_lang_code_dict_reverse
from transformers import AutoTokenizer, pipeline

device = torch.device(0 if torch.cuda.is_available() else -1)
input_texts = [
    "എന്റെ പേര് അലക്സ് സിബു",
    "Jürgen ist ein schräger Vogel",
    "എന്റെ പേര് അലക്സ് സിബു",
    "namaste! main plantix sahaayak hoon aur main yahaan aapake paudhon kee samasyaon mein aapakee madad karane ke lie hoon. kya aap adhik jaanakaaree pradaan kar sakate hain taaki main aapako behatar sujhaav de sakoon. jaise ki kya aap ke soybean me kuch kit ya aur pareshani hai",
]
# XLM-RoBERTa
pipe = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection",
    device=torch.device("cuda"),
)
print(pipe.predict(input_texts))

# IndicLID-BERT for latin letters Indian
IndicLID_BERT = torch.load(
    "data/indiclid-bert/basline_nn_simple.pt", map_location=device
)
IndicLID_BERT.id2label = IndicLID_lang_code_dict_reverse
IndicLID_BERT.eval()
IndicLID_BERT_tokenizer = AutoTokenizer.from_pretrained(
    "ai4bharat/IndicBERTv2-MLM-only", device=device
)
pipe2 = pipeline(
    "text-classification",
    model=IndicLID_BERT,
    tokenizer=IndicLID_BERT_tokenizer,
    device=device,
)

prediction = pipe2.predict(input_texts)
print(prediction)
# tokenized = IndicLID_BERT_tokenizer(
#     input_texts,
#     return_tensors="pt",
#     padding=True,
#     truncation=True,
#     max_length=512,
# ).to(torch.device("cuda"))
# output = IndicLID_BERT(**tokenized)
# _, prediction = torch.max(output.logits, 1)
# print(list(map(lambda x: IndicLID_lang_code_dict_reverse[x.item()], prediction)))


# IndicLID-FTN for Indian scripts
IndicLID_FTN = fasttext.load_model("data/indiclid-ftn/model_baseline_roman.bin")
prediction, score = IndicLID_FTN.predict(input_texts)
print(prediction)
