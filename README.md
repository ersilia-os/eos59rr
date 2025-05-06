# Molecular fingerprint maps based on broadly learned knowledge-based representations

Molecular representation of small molecules via ingerprint-based molecular maps (images). Typically, the goal is to use these images as inputs for an image-based deep learning model such as a convolutional neural network. The authors have demonstrated high performance of MolMap out-of-the-box with a broad range of tasks from MoleculeNet.

This model was incorporated on 2023-07-03.

## Information
### Identifiers
- **Ersilia Identifier:** `eos59rr`
- **Slug:** `bidd-molmap-fingerprint`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Not Applicable`
- **Tags:** `Fingerprint`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `1332`
- **Output Consistency:** `Fixed`
- **Interpretation:** Image representation of a molecule. Each pixel represents a molecular feature (37 rows, 36 columns, flattened with reshape)

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| row_00_col_00 | integer |  | Row index 0 and column index 0 from the BIDD MolMap fingerprint |
| row_00_col_01 | integer |  | Row index 0 and column index 1 from the BIDD MolMap fingerprint |
| row_00_col_02 | integer |  | Row index 0 and column index 2 from the BIDD MolMap fingerprint |
| row_00_col_03 | integer |  | Row index 0 and column index 3 from the BIDD MolMap fingerprint |
| row_00_col_04 | integer |  | Row index 0 and column index 4 from the BIDD MolMap fingerprint |
| row_00_col_05 | integer |  | Row index 0 and column index 5 from the BIDD MolMap fingerprint |
| row_00_col_06 | integer |  | Row index 0 and column index 6 from the BIDD MolMap fingerprint |
| row_00_col_07 | integer |  | Row index 0 and column index 7 from the BIDD MolMap fingerprint |
| row_00_col_08 | integer |  | Row index 0 and column index 8 from the BIDD MolMap fingerprint |
| row_00_col_09 | integer |  | Row index 0 and column index 9 from the BIDD MolMap fingerprint |

_10 of 1332 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos59rr](https://hub.docker.com/r/ersiliaos/eos59rr)
- **Docker Architecture:** `AMD64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos59rr.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos59rr.zip)

### Resource Consumption


### References
- **Source Code**: [https://github.com/shenwanxiang/bidd-molmap](https://github.com/shenwanxiang/bidd-molmap)
- **Publication**: [https://www.nature.com/articles/s42256-021-00301-6](https://www.nature.com/articles/s42256-021-00301-6)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2021`
- **Ersilia Contributor:** [samuelmaina](https://github.com/samuelmaina)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [GPL-3.0-or-later](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos59rr
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos59rr
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
