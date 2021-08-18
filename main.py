# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Utility
import dateutil.parser
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# Seleziona l"account di servizio
credentials = credentials.Certificate("secret.json")
firebase_admin.initialize_app(credentials)
db = firestore.client()

# Recupera i dati utili
all_users: list = db.collection(u"users").get()
all_books: list = db.collection(u"books").get()

print(f"Oggi abbiamo {len(all_users)} utenti!")
print(f"I libri, fra cercati e venduti, sono, invece, {len(all_books)}.")

# Prepara i dati per il grafico
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

# Mostra il grafico
figure(figsize=(10, 6), dpi=80)
plt.plot_date(x, y, "-g")
plt.show()
