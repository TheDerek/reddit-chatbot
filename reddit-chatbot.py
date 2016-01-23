import json
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def most_similar_sort(text, comments):
    return sorted(comments, key=lambda x: similar(text, x['body']),
                  reverse=True)


def vote_sort(comments):
    return sorted(comments, key=lambda x: x['ups'] - x['downs'], reverse=True)


def most_similar(text, comments):
    best_ratio = 0
    best_comment = ''

    for comment in comments:
        ratio = similar(text, comment['body'])
        if ratio > best_ratio:
            best_ratio = ratio
            best_comment = comment

    return best_comment


def get_replies(parent, comments):
    replies = []
    for comment in comments:
        if (parent['name'] == comment['parent_id']) and '[deleted]' not in comment['body']:
            replies.append(comment)

    return replies


if __name__ == '__main__':
    data = open('RC_2007-10', 'r').read()
    comments = json.loads(data)

    while True:
        text = input('Say: ')
        similar_comments = most_similar_sort(text, comments)

        for comment in similar_comments:
            replies = get_replies(comment, comments)
            replies = vote_sort(replies)
            if replies:
                for reply in replies:
                    print(reply['body'])
                break
