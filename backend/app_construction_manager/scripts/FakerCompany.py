from django.contrib.auth import get_user_model
from app_construction_manager.models import Address, Company
from faker import Faker
import random

def run():
    fake = Faker('pl_PL')
    User = get_user_model()

    print("▶ Szukam użytkownika...")
    user = User.objects.first()
    if not user:
        print("⛔ Nie znaleziono użytkownika — tworzę testowego...")
        user = User.objects.create_user(username='testuser', password='password')

    print("▶ Tworzę adresy...")
    addresses = []
    for _ in range(300):
        addr = Address.objects.create(
            street=fake.street_name(),
            building_number=fake.building_number(),
            apartment_number=fake.building_number() if random.random() > 0.5 else None,
            postal_code=fake.postcode(),
            city=fake.city(),
            state=random.choice([
                'dolnośląskie', 'kujawsko-pomorskie', 'lubelskie', 'lubuskie',
                'łódzkie', 'małopolskie', 'mazowieckie', 'opolskie',
                'podkarpackie', 'podlaskie', 'pomorskie', 'śląskie',
                'świętokrzyskie', 'warmińsko-mazurskie', 'wielkopolskie', 'zachodniopomorskie'
            ]),
            country='Polska',
        )
        addresses.append(addr)

    print("▶ Tworzę firmy...")
    for i in range(1000):
        Company.objects.create(
            name=fake.company(),
            email=fake.company_email(),
            address=random.choice(addresses),
            phone_number_1=fake.phone_number(),
            phone_number_2=fake.phone_number(),
            phone_number_3=fake.phone_number(),
            vat_id=fake.msisdn()[:10],
            regon_id=fake.msisdn()[:14],
            is_active=random.choice([True, False]),
            timezone='Europe/Warsaw',
            create_by=user,
        )
        if i % 100 == 0:
            print(f" - {i} firm utworzonych...")

    print("✅ Gotowe: 1000 firm i 300 adresów wygenerowanych.")