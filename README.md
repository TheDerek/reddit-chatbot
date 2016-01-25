# reddit-chatbot
A chat bot based on reddit comments, slow to respond and difficult to hold a conversion with.

```
> Hello
Sup dog?
> How are you?
That's what I'd like to know from you.
> Do you like deer?
I'm assuming that was a question, and no, most likely I wouldn't eat veal.
```

This chatbot is uses on a small subset of the [comments made available by /u/Stuck_In_the_Matrix](https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment) as it's dataset.
Specifcally all the reddit comments for the month of October 2007. The chatbot is quite slow, taking up to a minute to respond on my i7 processor.

It works by finding the similarity between the text given to it and all the comments in it's dataset.
It then finds the most similar comment that has replies and prints out the highest rated reply.
The larger the dataset the better the replies, but longer the response time.

Run it using `python3 reddit-chatbot.py`
