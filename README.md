# ML_Final_Project
Final Group Project for Machine Learning, Fall 2020

## Proposal: NLP Methods to Characterize and Classify Fake News Using Linguistic Patterns 

### The LIAR Dataset:
The [LIAR Dataset](https://arxiv.org/pdf/1705.00648.pdf) was compiled by Yang Wang , 12.8K manually labeled short statements in various contexts from POLITIFACT.COM, and is primarily used for automatic fake news detection based on surface-level linguistic patterns. It is pre-broken down in the following way and delivered with some metadata on [Github](https://github.com/thiagorainmaker77/liar_dataset):
- Training set size 10,269
- Validation set size 1,284
- Testing set size 1,283
- Avg. statement length (tokens) 17.9

### Alternate Datasets:
- [Fact Extraction and VERification (FEVER)](https://www.aclweb.org/anthology/N18-1074/): short claim dataset of 185,445 claims, 3 labels 
- [The Mafiascum Dataset] (https://web.stanford.edu/class/cs224n/reports/custom/15722645.pdf)

### Proposed Methodologies:
- Topic modelling
    - Characterize the content of the data
    - Dynamic topic modelling to look at changing patterns over time. Does the topic model define the metadata categories better?
    - Clustering of topics to see what statements are related to one another
- TF-IDF vs N-gram Count vs. BOW Vectorization of statements prior to classification
    - Impacts of articles that often are considered stopwords
- Classification: Classic models vs. Neural networks (namely CNNs according to literature review)
- Possible expansion comparing sentiment polarity of text to whether it is considered a [lie](https://arxiv.org/pdf/2009.01047.pdf) 
- The original paper did some trade studies by classifying using both the statement and metadata (might be a redundant investigation but possibly interesting)

## Structure
- code: all code implementation for the project and Jupyter notebooks for exploratory analysis/debugging
- data: training, test, and validation data for models
- papers: any literature for sharing or of interest for research and final report
