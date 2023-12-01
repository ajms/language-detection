# language-detection
A repo to containerize a language detection model


# Initialise project
Install python 3.11 and poetry and run

```bash
make prj-init
```

Download models from [AI4Bharat](https://github.com/AI4Bharat/IndicLID)
```bash
wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-ftn.zip
wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-bert.zip
mkdir -p data
unzip indiclid-ftn.zip -d data/
unzip indiclid-bert.zip -d data/
rm indiclid-ftn.zip indiclid-bert.zip
```
