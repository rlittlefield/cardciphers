import card_chameleon

c = card_chameleon.Cipher()
plaintext = "A"*260000
ciphertext = ""

def reset_deck():
    deck = [i for i in xrange(1,53)]
    c._prepare_deck(deck)
    return deck
    
def encrypt(deck, letter):
    return c.prng(deck, letter)

def decrypt(deck, letter):
    return c.prng(deck, letter)

deck = reset_deck()
#c.shuffle_deck(deck)

for char in plaintext:
    ciphertext += encrypt(deck,char)

print ciphertext

plaintext = ""
print ""

deck = reset_deck()
for char in ciphertext:
   plaintext += decrypt(deck,char)

#print plaintext