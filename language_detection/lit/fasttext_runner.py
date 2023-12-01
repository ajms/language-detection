import bentoml
import fasttext


class FastTextRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self, model_file):
        self.model = fasttext.load_model(model_file)

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    def predict(self, input_text: str | list[str]) -> dict[str, any]:
        predictions, scores = self.model.predict(input_text)
        print(input_text)
        print({"label": predictions, "score": scores})
        if isinstance(input_text, list):
            return [
                {"label": prediction[0], "score": score}
                for prediction, score in zip(predictions, scores)
            ]
        else:
            return {"label": predictions[0], "score": scores}
