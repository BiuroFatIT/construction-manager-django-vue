from django.contrib.auth import get_user_model
from app_construction_manager.models import Product, Company
from faker import Faker
import random

def run():
    fake = Faker("pl_PL")
    User = get_user_model()

    print("▶ Pobieram użytkownika...")
    user = User.objects.first()
    if not user:
        print("⛔ Brak użytkownika — tworzenie testowego...")
        user = User.objects.create_user(username="testuser", password="password")

    companies = Company.objects.filter(id__lte=1000)
    total = 0

    # Lista przykładowych baz nazw projektów
    base_names = [
        "Dom Marzenie", "Willa Komfort", "Nowoczesny", "Zacisze", "Rodzinny",
        "Przytulny", "Stylowy", "Funkcjonalny", "Elegancki", "Słoneczny Zakątek",
        "Panorama", "Dworek", "Natura", "Przestronny", "Ciepły Dom",
        "Magnolia", "Kalifornia", "Brzoza", "Lipowy Dwór", "Pod Klonem",
        "Dom w Ogrodzie", "Sielanka", "Laguna", "Amber", "Albatros",
        "Topaz", "Rubinowy", "Jantar", "Kryształowy", "Złoty Brzeg",
        "Ustronny", "Dom Przy Lesie", "Dom Na Wzgórzu", "Wygodny",
        "Dom Miejski", "Villa Verde", "Dom w Kwiatach", "Dom pod Sosną",
        "Koral", "Tęczowy", "Kasztanowy", "Malinowy", "Dom w Stylu Toskanii",
        "Lawenda", "Dom przy Cyprysowej", "Bursztynowy", "Modrzewiowy",
        "Dom dla Ciebie", "Słoneczny Dom", "Dom Spokojny", "Dom Cichy",
        "Dom Optymalny", "Dom Premium", "Dom Klasyczny", "Dom Nowoczesny",
        "Projekt Alfa", "Projekt Omega", "Dom Lux", "Dom Max"
    ]

    for company in companies:
        products = []
        for _ in range(10):
            # Dane domu
            usable_area = round(random.uniform(70.0, 220.0), 2)
            net_area = round(usable_area * random.uniform(0.85, 0.98), 2)
            gross_volume = round(usable_area * random.uniform(2.8, 3.5), 2)
            estimated_weeks = random.randint(14, 60)
            price_net = round(usable_area * random.uniform(3500, 7000), 2)
            price_gross = round(price_net * 1.23, 2)

            # Generowanie nazwy projektu domu
            base = random.choice(base_names)
            suffix = random.choice(["", f" {random.randint(1, 9)}", f" {random.randint(100, 999)}"])
            project_name = base + suffix

            product = Product(
                name=project_name,
                description=(
                    f"{base} to projekt domu o powierzchni użytkowej {usable_area} m² "
                    f"z {random.randint(3, 6)} pokojami i przewidywanym czasem budowy ok. {estimated_weeks} tygodni. "
                    f"Idealny dla {random.choice(['rodziny 2+1', 'rodziny 2+2', 'pary', 'osób ceniących przestrzeń'])}."
                ),
                price_net=price_net,
                price_gross=price_gross,
                estimated_duration_weeks=estimated_weeks,
                usable_area_m2=usable_area,
                net_area_m2=net_area,
                gross_volume_m3=gross_volume,
                is_active=True,
                company=company,
                create_by=user
            )

            products.append(product)

        Product.objects.bulk_create(products)
        total += len(products)

        if company.id % 100 == 0:
            print(f" - Produkty dla firm do ID {company.id} wygenerowane.")

    print(f"✅ Utworzono {total} produktów – projekty domów.")