# comics_rx

## Comic Book Recommendation System

**Goal:** Build a recommendation system to 'prescribe' comics to read/buy/subscribe.

---

### Business Understanding
I subscribe to comic books at a fanastic local comic shop, [Arcane Comic & More](https://www.arcanecomicbooks.com/), and one of the many awesome services they provide is something they call ‘associations’. These associations are intended to match customers to new titles (e.g. new comic books to be released in the near future) that they may be interested. If you opt-in to assocations, you will be automatically subscribed to these associated titles.

**For example: 

<img src="./comrx/dev/assets/assoc_example.png" width=600, align='center'>

In the example above “Savage Avengers” is being recommended to those who subscribe to “Savage Sword of Conan”.

After discussing it with the shop manager, it turns out this process is completely human-driven. We have built a comic book recommendation system that performs a similar task: to recommend comics titles to a customer (existing and new) based on their current preferences. For current customers this could simply be a replica of their current subscriptions (or more)! For new customers this could be a list of their favorite comic titles.

### Data Understanding
With the help of Arcane Comics we obtained a set of de-identified data of comic books titles sold since they implemented their current point-of-sale system in Feb 2010. 

We built an implicit-ratings matrix based on this information. Because buyers at brick-and-mortar stores don’t usually review their books, we proxied their ‘review’ with the fact that they purchased the item. The transaction data provides customer id, date of purchase, and specific issue (e.g. Batman #123). There are some limitations that we will discuss further below.

Once weakness in the data was the inability to easily link sold issues to their specific volumes. This is important because comic books are notorious for being 're-booted' frequently. And each re-boot, may have different create teams, characters, etc. For example, according to [www.comicbookdb.com](http://www.comicbookdb.com/search.php?form_search=Amazing%20Spider-Man&form_searchtype=Title), _The Amazing Spider-Man_ has distinct volumes in both 2015 and 2018.  

### Data Preparation
Since the data originated from a point-of-sale system it was already clean. The primary task was to prune down the data for accounts (i.e. customers) such as:
- Only had a handful of transactions. These are outliers in the sense that they may not be regular comic book consumers and we want to tailor our recommendations to regular customers.
- Had very many transactions. To give sense, the 75th percentile of number of titles bought is 51; but there are customers with 100's of titles bought. We capped the 3 of titles bought in the interest of controlling for outliers.

#### Storage
- We used AWS RDS to store the structured data. 
- We used AWS S3 bucket to store assets for the webapp.

#### Prep
The primary task was getting purchase/review data into the proper form to create an ALS matrix factorization model to be the basis of the recommendation system. The cleaning was as described above, in pruning outliers.

### Modeling
We used ALS matrix factorization method to build the base algorithm via (Py)Spark.

### Evaluation
We used grid search and k-fold cross-validation for parameter searching and tuning.

We used RMSE as our error metric.

### Deployment
Our application is a website [www.comics-rx.com](www.comics-rx.com) where a customer can identify 3 of their favorite comics and be offered 1-20 recommendations.

Future development goals are to allow for a more flexible number of favorite comics to be identified to get recommendations.

### User Story
Henry is a currently a box subscriber at Arcane Comics & More. He has opted-in to Assocations as a way to automatically keep in the loop with new titles on the horizon. The store does a great job for the most part of subscribing him to titles that align with his current reading interests. This is a great value to him because he doesn't have much additional free time to do things like read up on new titles his favorite publishers or writers are developing. He wonders, though,if there is a way to get recommendations on comic books that may have already been published but he hasn't noticed yet.

Bobbie works at the shop. It's incredibly rewarding to use her vast knowledge of all things comics culture to curate the associations list! But she wonders if there is a tool she could use to help further augment the development of recommendations. Is there a way to not only use subscription data, but purchase data as well, to efficiently identify potential comic matches for customers?   

#### _Execution_
The intial deployment is in form or a web application. In can be found at [http://www.comics-rx.com](http://www.comics-rx.com)!

In order to recreate the project do the following:
#### UNDER CONSTRUCTION

