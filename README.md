# Molecular fingerprint maps based on broadly learned knowledge-based representations

Molecular representation of small molecules via ingerprint-based molecular maps (images). Typically, the goal is to use these images as inputs for an image-based deep learning model such as a convolutional neural network. The authors have demonstrated high performance of MolMap out-of-the-box with a broad range of tasks from MoleculeNet.

## Identifiers

* EOS model ID: `eos59rr`
* Slug: `bidd-molmap-fps`

## Characteristics

* Input: `Compound`
* Input Shape: `Single`
* Task: `Representation`
* Output: `Image, Descriptor`
* Output Type: `Float`
* Output Shape: `Matrix`
* Interpretation: Image representation of a molecule. Each pixel represents a molecular feature

## References

* [Publication](https://www.nature.com/articles/s42256-021-00301-6)
* [Source Code](https://github.com/shenwanxiang/bidd-molmap)
* Ersilia contributor: [samuelmaina](https://github.com/samuelmaina)

## Ersilia model URLs
* [GitHub](https://github.com/ersilia-os/eos59rr)
* [AWS S3](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos59rr.zip)
* [DockerHub](https://hub.docker.com/r/ersiliaos/eos59rr) (AMD64)

## Citation

If you use this model, please cite the [original authors](https://www.nature.com/articles/s42256-021-00301-6) of the model and the [Ersilia Model Hub](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff).

## License

This package is licensed under a GPL-3.0 license. The model contained within this package is licensed under a GPL-3.0 license.

Notice: Ersilia grants access to these models 'as is' provided by the original authors, please refer to the original code repository and/or publication if you use the model in your research.

## About Us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission!