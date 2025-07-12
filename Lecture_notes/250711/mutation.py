# objects can change
# only objects of mutable tyoes can change: list & dictionary
# story of cards
card = ['string', 'coin', 'myraid']
suite = card
card.pop()
card.remove('string')
card.append('cup')
card.extend(['sword', 'club'])
card[2] = 'spade'
card[0:2] =['heart', 'diamond']
print(suite)

l = [1, 2, 4, 8]
def mystry(s):
    s.pop()
    s.pop()

def mystry2():
    l.pop()
    l.pop()

# mystry(l)
mystry2()
print(len(l))
