# Project: Commercial Real Estate

## Overview
This project explores GHG emission prediction using timeseries models including _ARIMa_, _LSTM_ and _PROPHET_, and portfolio optimization using the _Markowitz_ model.

## Project Structure
- `data/` → Raw & processed datasets.
- `notebooks/` → Jupyter notebooks (main).
- `src/` → Mainly utility function used in the notebooks.

>[!IMPORTANT]
>Before running the jupyter notebook:
>1. Ensure that you have the two datasets in a directory `data\`[^1] as follows:
>- `data\raw\dpe-tertiaire.csv`
>- `data\raw\dpe-v2-tertiaire-2.csv`
>- `data\raw\mapping_secteur_activite - filtered.csv`
>- `data\raw\markowitz_dataset.csv`
>
> If the generation of the imputed data takes too long, please contact us to provide you with the processed and imputed data directly.

## Installation
```bash
git clone https://github.com/mouad-leachouri/commercial-real-estate/
cd commercial-real-estate
```

## Links
**Link for the presentatoion:** [Project: Commercial Real Estate](https://docs.google.com/presentation/d/1cXeATyDPBea_HoZfHvkXEK8rSgYQsnIs82DDm8zaG5w/edit?usp=sharing)

[^1]: Create it if it doesn't already exist.
