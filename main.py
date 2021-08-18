import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import dateutil.parser
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# Use a service account
cred = credentials.Certificate('secret.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

all_users: list = db.collection(u'users').get()
all_books: list = db.collection(u'books').get()

print(f"Oggi abbiamo {len(all_users)} utenti!")
print(f"I libri, fra cercati e venduti, sono, invece, {len(all_books)}.")

# Comincia a salvare le date
book_dates: list = list(
    map(lambda book: dateutil.parser.isoparse(book.to_dict()["addedDateTime"]), all_books))

sorted_book_dates: dict = {}
for date in book_dates:
    if date.date() in sorted_book_dates:
        sorted_book_dates[date.date()] = sorted_book_dates[date.date()] + 1
    else:
        sorted_book_dates[date.date()] = 1

sorted_book_dates: list = sorted(sorted_book_dates.items())
for index in range(1, len(sorted_book_dates)):
    sorted_book_dates[index] = sorted_book_dates[index][0], sorted_book_dates[index][1] + sorted_book_dates[index - 1][
        1]

x, y = zip(*sorted_book_dates)

figure(figsize=(10, 6), dpi=80)
plt.plot_date(x, y, "-g")
plt.show()
