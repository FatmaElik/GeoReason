Data
Raw data is not committed to this repository.
Datasets used
SAR–Optical Earthquake Damage Dataset (mine)
İslahiye, 2023 Kahramanmaraş earthquakes. Capella SAR + Maxar
optical, ~7,000 buildings, four damage classes, field-validated
ground truth. Pilot 01 uses a small optical subset (`satdemo/`):
256×256 RGB patches + pixel-level damage masks +
`image_label_pairs.csv`.
Turkish Disaster News GeoNLP Dataset (mine)
https://huggingface.co/datasets/FatmaElik/turkish-disaster-news-geonlp
~591 geocoded Turkish disaster news articles, CC BY-NC 4.0.
Labels are machine-generated and not yet human-verified, so in
this repository the dataset is used only as a style reference for
news-like prompt templates — never as ground truth.
Expected local layout
```text
experiments/pilot01-evidence-conflict/
└── satdemo/
    ├── images/            256×256 RGB .tif patches
    ├── labels/            damage masks (0 = background, 3, 4 = classes)
    └── image_label_pairs.csv
```
