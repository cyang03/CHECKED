## fake_news
This folder includes 344 microblogs (json file) labeled *fake*.
Each microblog (json file) consists of the following components:

* `id`: The microblog's ID. Each microblog is identified by a unique 16 digit ID assigned by Weibo. To protect users' privacy, we have **hashed** each ID to 32 digits in the dataset.
* `label`: The microblog's label. The label of each microblog is either *real* or *fake*.
* `analysis`: The official report including detailed analysis and a result on detecting fake news from Weibo experts. Note that only microblogs identified as *fake* news contain this component. 
* `date`: The date that the microblog is posted (in format yyyy-mm-dd hh:mm).
* `user_id`: The user's ID who posted the microblog. Weibo assigns each of its users a unique ID number with 10 digits. Note that each user can change his ID only once to a string formed by 4-20 characters, where letters are allowed. To protect users' privacy, we have also **hashed** each user's ID to 32 digits in the dataset.
* `text`: Textual information of microblogs.
* `pic_url`: The URL of the visual information of microblog. Note that users are allowed to attach no more than 18 images in each microblog.
* `video_url`: The URL of the video information of microblog. Note that each microblog (i) can only include at most one video; and (ii) cannot attach both the video and image.
* `comment_num`, `repost_num`, and `like_num`: The number of comments, forwards, and likes of the microblog.
* `comments`: The detailed information of user comments for the microblog, including (i) the ID (**hashed**), date, and content of comments (microblogs), and (ii) the ID (**hashed**) of commenters (users). Note that for each comment, no more than one image and no video are allowed.
* `reposts`: The detailed information of user forwards for the microblog, which specifies (i) the ID (**hashed**), date, and content of forwards (microblogs), and (ii) the ID (**hashed**) of forwarders (users). Similar to comments, each forward has at most one image and no video information. Note that if a user forwards a repost with an image, the `pic_url` of the new forward will also include this image along with the original image.

## real_news
This folder involves 1776 microblogs (json file) labeled *real*.
Each microblog (json file) consists of all the same components as that in the *fake_news* folder excluding `analysis`.

## fake_news.csv
This file contains all 344 *fake* microblogs (transfered from json files in the *fake_news* folder) with identical components except for `comments` and `reposts`. 

## real_news.csv
This file contains all 1776 *real* microblogs (transfered from json files in the *real_news* folder) with identical components except for `comments` and `reposts`.

## fake_news_comment.csv
This file contains the relationship between *fake* microblogs and comments. Each row contains one `microblog_id` and `comment_id` that commented the microblog.

## fake_news_repost.csv
This file contains the relationship between *fake* microblogs and reposts. Each row contains one `microblog_id` and `repost_id` that forwarded the microblog. 

## real_news_comment.csv
This file contains the relationship between *real* microblogs and comments. Each row contains one `microblog_id` and `comment_id` that commented the microblog. 

## real_news_repost.csv
This file contains the relationship between *real* microblogs and reposts. Each row contains one `microblog_id` and `repost_id` that forwarded the microblog. 

## keyword_list.txt
This file includes all the keywords that we used to determine if the microblog is about COVID-19. There are total 39 keywords (33 Chinese + 6 English).