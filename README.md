# CHECKED
The first Chinese COVID-19 fake news dataset based on the Weibo platform.

## Notice
We care about users' privacy and made (will keep making) efforts to protecting it.
* We did not make the `user name` public, which enables to identify Weibo users. In addition, we released the **hashed** `user_id` instead of the original `user_id` of Weibo. 
* Please use the CHECKED data only for academic research.

## Overiew
This repository includes 2 folders which are code and dataset.

The `code` folder contains codes for collecting COVID-19 microblogs and analyzing collected data.

The `dataset` folder includes 2 folders - `fake_news` and `real_news` where 
* `fake_news`  includes 344 microblogs labeled 'fake'.
* `real_news` involves 1776 microblogs labeled 'real'.

Each microblog (json file) consists of the following components:
* `id`: The microblog's ID. Each microblog is identified by a unique 16 digit ID assigned by Weibo.
* `label`: The microblog's label. The label of each microblog is either 'real' or 'fake'.
* `date`: The date that the microblog is posted (in format yyyy-mm-dd hh:mm).
* `user_id`: The user's ID who posted the microblog. Weibo assigns each of its users a unique ID number with 10 digits. Note that each user can change his ID only once to a string formed by 4-20 characters, where letters are allowed.
* `text`: Textual information of microblogs.
* `pic url`: The URL of the visual information of microblog. Note that users are allowed to attach no more than 18 images in each microblog.
* `video url`: The URL of the video information of microblog. Note that each microblog (i) can only include at most one video; and (ii) cannot attach both the video and image.
* `comment num`, `repost num`, and `like num`: The number of comments, forwards, and likes of the microblog.
* `comments`: The detailed information of user comments for the microblog, including (i) the ID, date, and content of comments (microblogs), and (ii) the ID and name of commenters (users). Note that for each comment, no more than one image and no video are allowed.
* `reposts`: The detailed information of user forwards for the microblog, which specifies (i) the ID, date, and content of forwards (microblogs), and (ii) the ID and name of forwarders (users). Similar to comments, each forward has at most one image and no video information. Note that if a user forwards a repost with an image, the `pic url` of the new forward will also include this image along with the original image.

`news_fake.csv` contains all the fake microblogs in `fake_news` with identical components except for 'comments' and 'reposts'.

`news_real.csv` contains all the real microblogs in `real_news` with identical components except for 'comments' and 'reposts'.

`news_total.csv` is a combination of `news_fake.csv` and `news_real.csv`.

`list.txt` includes all the keywords that we used to determine if the microblog about COVID-19.

## Reference
If you are using this dataset, please kindly cite the following paper:
~~~~
@article{yang2020checked,
  title={CHECKED: Chinese COVID-19 Fake News Dataset},
  author={Yang, Chen and Zhou, Xinyi and Zafarani, Reza},
  journal={arXiv preprint arXiv:submit/3422152},
  year={2020}
}
~~~~

## Contact
Please contact zhouxinyi@data.syr.edu if you have any question on our dataset.
