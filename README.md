# CHECKED
The first Chinese COVID-19 fake news dataset based on the Weibo platform. Please check out our paper [here](https://arxiv.org/pdf/2010.09029.pdf).

## Notice
We care about users' privacy and made (will keep making) efforts to protecting it.
* For microblogs: We released the **hashed** `id` instead of the original `id` of microblogs.
* For users: We did not make the `user_name` public, which enables to identify Weibo users. In addition, we released the **hashed** `user_id` instead of the original `user_id`. 
* Please use the CHECKED data only for academic research.

**Update:** 
We add `analysis` as a new keyword for each microblog labeled as *fake*. `analysis` contains the expert analysis and justification, which details the news falseness. Please check out the [*dataset*](https://github.com/cyang03/CHECKED/tree/master/dataset) folder for details. We also provide benchmark results of [FastText](https://arxiv.org/pdf/1607.01759.pdf), [TextCNN](https://arxiv.org/pdf/1408.5882.pdf), [TextRNN](https://arxiv.org/pdf/1605.05101.pdf), [Att-TextRNN](https://www.aclweb.org/anthology/P16-2034.pdf), and [Transformer](https://arxiv.org/pdf/1706.03762.pdf) using the CHECKED data in predicting fake news. Please check out the [*baseline*](https://github.com/cyang03/CHECKED/tree/master/baseline) folder for details. (June 9, 2021)

## Overiew
This repository includes three folders, named as (1) dataset, (2) code, (3) baseline, respectively.

* *dataset*: This folder contains the CHECKED data in both `json` and `csv` format and the list of keywords used to determine whether a microblog is relevant to COVID-19 or not. Specifically,
    * *fake_news*: This folder includes 344 fake microblogs (in `json` format). 
    * *real_news*: This folder includes 1760 real microblogs (in `json` format).
    * **.csv*: These `csv` files are converted from `json` files in the *fake_news* and *real_news* folder.
    * *keyword_list.txt*: This file includes all the keywords that we use to determine if the microblog is about COVID-19.

    A more detailed README regarding *dataset* is available [here](https://github.com/cyang03/CHECKED/tree/master/dataset).

* *code*: This folder contains the code used for collecting and analyzing the CHECKED data. 

* *baseline*: This folder contains the data and code to get benchmark results. A more detailed README is available [here](https://github.com/cyang03/CHECKED/tree/master/baseline).

**Microblog Components:**
For each microblog, we collect its following components:
* `id`: The microblog's ID. (**hashed**) 
* `label`: The microblog's label (*real* or *fake*).
* `date`: The date that the microblog is posted.
* `user_id`: The user's ID who posts the microblog. (**hashed**)
* `text`, `pic_url`, and `video_url`: Textual and visual information of microblogs.
* `comment_num`, `repost_num`, and `like_num`: The number of comments, forwards, and likes of the microblog.
* `comments` and `reposts`: The detailed information of user comments and forwards for the microblog.
* `analysis`: The analysis and justification of experts. (only for fake microblogs)

**File Structure:** 
```
├── README.md
├── dataset
│   ├── README.md
│   ├── fake_news.csv
│   ├── real_news.csv
│   ├── keyword_list.txt
│   ├── fake_news_comment.csv
│   ├── fake_news_repost.csv
│   ├── real_news_comment.csv
│   ├── real_news_repost.csv
│   ├── fake_news
│   │   ├── 0023fbc0cb2119235e6482ca221e34fb.json
│   │   ├── 0031ff8f6d0f6502fde093a640ae836a.json
│   │   └── ....        
│   └── real_news
│       ├── 00970e529583ba55bc3bb2c4eff889df.json
│       ├── 022012c3a40b424a85a6b0a2f9bf9726.json
│       └── ....                    
├── baseline
│   ├── README.md
│   ├── data
│   │   ├── vocab.pkl
│   │   ├── embedding_SougouNews.npz
│   │   ├── new_dev.txt
│   │   ├── new_test.txt
│   │   └── new_train.txt 
│   └── code
│       ├── saved_dict
│       ├── embeddings
│       │    └── sgns.sogou.char
│       ├── models
│       │    ├── Att_TextRNN.py
│       │    ├── FastText.py
│       │    ├── TextCNN.py
│       │    ├── TextRNN.py
│       │    └── Transformer.py
│       ├── char_embeddings.embeddings.pkl
│       ├── char_embeddings.word2id.pkl
│       ├── run.py
│       ├── train_eval.py
│       ├── utils.py
│       └── utils_fasttext.py
└── code
    ├── analysis.ipynb
    ├── jsonToCSV.py
    ├── spider_fake.py
    └── spider_fake.py
```

## Reference
If you are using this dataset, please kindly cite the following paper:
~~~~
@article{yang2020checked,
  title={CHECKED: Chinese COVID-19 Fake News Dataset},
  author={Yang, Chen and Zhou, Xinyi and Zafarani, Reza},
  journal={arXiv preprint arXiv:2010.09029},
  year={2020}
}
~~~~

## Contact
Please contact *zhouxinyi@data.syr.edu* if you have any question on our dataset.
