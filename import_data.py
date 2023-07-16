import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projekt.settings")
django.setup()

from app1.models import Predmeti
import json

fixture_file = "predmeti.json"

with open(fixture_file, encoding='utf-8') as f:
    data = json.load(f)

for subject_data in data:
    izborni_choice_mapping = {
        "da": True,
        "ne": False,
    }
    
    izborni_value = subject_data['fields']['izborni']
    subject_data['fields']['izborni'] = izborni_choice_mapping.get(izborni_value)

    predmet = Predmeti(**subject_data['fields'])
    predmet.save()
