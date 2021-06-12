# Benchmark Results in Fake News Detection

We provide the benchmark result using CHECKED data and the following methods in predicting: (1) [FastText](https://arxiv.org/pdf/1607.01759.pdf), [TextCNN](https://arxiv.org/pdf/1408.5882.pdf), (2) [TextRNN](https://arxiv.org/pdf/1605.05101.pdf), (3) [Att-TextRNN](https://www.aclweb.org/anthology/P16-2034.pdf), and (4) [Transformer](https://arxiv.org/pdf/1706.03762.pdf).

There are two folders *data* and *code*:
* *data*: This folder provides the CHECKED data divided for training, testing, and validation.
* *code*: This folder contains the source code to generate benchmark results.

**Note:** For all the methods, only the content representation of microblogs (not including the corresponding reposts and comments) is learned for classification. In other words, all the methods are content-based. We encourage more and more benchmark results using various methods.

## How was the data divided

We divided the data, based on their posting time order, for training, validation, and testing with a proportion of 70%:10%:20%.

## How to use

**1. Embedding words:** We use [Sogou News Word + Character Pre-Trained Chinese Word Vector](https://github.com/Embedding/Chinese-Word-Vectors). 
* Download and unzip the file [char_embeddings.embeddings.pkl.zip]((https://drive.google.com/drive/folders/1ZyQa76PCDm80afwnTqYMwOxlqrPHxP8Y?usp=sharing)) to folder `./baseline/code`.
* Download and unzip the file [sgns.sogou.char.zip](https://drive.google.com/drive/folders/1ZyQa76PCDm80afwnTqYMwOxlqrPHxP8Y?usp=sharing) to folder `./baseline/code/embeddings`

**2. Running codes**
```
# FastText
python run.py --model FastText

# TextCNN
python run.py --model TextCNN

# TextRNN
python run.py --model TextRNN

# Att-TextRNN
python run.py --model Att_TextRNN

# Transformer
python run.py --model Transformer
```


## Results
|              | FastText | TextCNN  | TextRNN  | Att-TextRNN | Transformer |
|:------------:|---------:|---------:|---------:|------------:|------------:|
| **Macro F1** |    0.839 |    0.938 |    0.700 |       0.871 |       0.927 |


## Acknowledgment
We appreciate [Chinese-Text-Classification-Pytorch](https://github.com/649453932/Chinese-Text-Classification-Pytorch).
