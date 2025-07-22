def search(query, ranking = lambda r: -r.stars):
    results = [r for r in Restaurant.all if query in r.name]
    return sorted(results, key = ranking)

def fast_overlap(r, s):
    i, j, cnt = 0, 0, 0
    while i < len(r) and j < len(s):
        if r[i] == s[j]:
            i, j, cnt = i + 1, j + 1, cnt + 1
        elif r[i] < s[j]:
            i += 1
        else:
            j += 1
    return cnt

def reviewed_both(r, s):
    return fast_overlap(sorted(r.reviewers), sorted(s.reviewers))

class Restaurant:
    all = []
    def __init__(self, name, stars, reviewers):
        self.name = name
        self.stars = stars
        self.reviewers = reviewers
        Restaurant.all.append(self)

    def similair(self, k, similarity = reviewed_both):
        others = Restaurant.all
        others.remove(self)
        different = lambda r: -similarity(r, self)
        return sorted(others, key = different)[:k]
    
    def __repr__(self):
        return '<' + self.name + '>'

import json

reviewers_for_restaurant ={}

for lines in open('reviews.json'):
    r = json.loads(lines)
    biz = r['business_id']
    if biz not in reviewers_for_restaurant:
        reviewers_for_restaurant[biz] = [r['user_id']]
    else:
        reviewers_for_restaurant[biz].append(r['user_id'])

for lines in open('restaurants.json'):
    r = json.loads(lines)
    reviewers = reviewers_for_restaurant[r['business_id']]
    Restaurant(r['name'], r['stars'], reviewers)

while True:
    print('NEXT SEARCH')
    print('->', end='')
    result = search(input().strip())
    for i in result:
        print(i , 'share reviewers with', i.similair(3))
