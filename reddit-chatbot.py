import json
from difflib import SequenceMatcher


# Returns a percentage between 0 and 1 describing the similarity between the
# two strings
def similar(a, b):
    a = a.lower().strip()
    b = b.lower().strip()
    return SequenceMatcher(None, a, b).ratio()


# Sort the comments in order of similarity to the text given
def most_similar_sort(text, comments):
    return sorted(comments, key=lambda x: similar(text, x['body']),
                  reverse=True)


# Sort the comments based on the number of votes that they have
def vote_sort(comments):
    return sorted(comments, key=lambda x: x['ups'] - x['downs'], reverse=True)


# Return the most similar comment to the one listed
def most_similar(text, comments):
    best_ratio = 0
    best_comment = ''

    for comment in comments:
        ratio = similar(text, comment['body'])
        if ratio > best_ratio:
            best_ratio = ratio
            best_comment = comment



    return best_comment


# Get meaningful replies from the parent comment
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
            # Find the best reply to give the user
            replies = get_replies(comment, comments)
            replies = vote_sort(replies)

            if replies:
                for reply in replies:
                    print(reply['body'])
                    print('(' + comment['body'] + ')')
                break
