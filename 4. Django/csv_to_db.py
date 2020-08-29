import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wt_project.settings")
django.setup()

from board.models import Webtoon

hand = open('./static/csv_data/webtoon_detail.csv', encoding='UTF8')
reader = csv.reader(hand)

bulk_list = []
for row in reader:
    bulk_list.append(Webtoon(
        wt_id = row[0],
        title = row[1],
        score = row[2],
        writer = row[3],
        genre = row[4],
        summary = row[5],
        link = row[6],
    ))

print("bulk list: ", bulk_list)

Webtoon.objects.bulk_create(bulk_list)

print(Webtoon.objects.values())