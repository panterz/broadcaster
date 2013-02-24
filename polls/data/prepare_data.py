#from voting.models import Poll, Choice, User, Area
from django.utils import timezone
import csv

"""
p = Poll(question="Are you going to vote?", pub_date=timezone.now())

p.save()

p = Poll(question="Who are you going to vote for?", pub_date=timezone.now())

p.save()

Poll.objects.all()

p = Poll.objects.get(id=1)

p.choice_set.create(choice_text='Yes')
p.choice_set.create(choice_text='No')

p = Poll.objects.get(id=2)

p.choice_set.create(choice_text='Candidate 1')
p.choice_set.create(choice_text='Candidate 2')
p.choice_set.create(choice_text='Candidate 3')"""

with open("preparation/gb_wpc_2010_05.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row[1] != "name":
            a = Area(name=row[1])
            a.save()

