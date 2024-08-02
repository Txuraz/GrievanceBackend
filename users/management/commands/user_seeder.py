import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User

class Command(BaseCommand):
    help = 'Seed the database with user data'

    def handle(self, *args, **kwargs):
        nepali_names = ["Ram", "Hari", "Om", "Shyam", "Sita", "Gita", "Bina", "Maya", "Amit", "Raj", "Sanjay", "Dipak", "Kiran", "Ravi", "Nisha", "Anita", "Sunil", "Puja", "Rita", "Manoj"]

        users = [
            {
                "name": random.choice(nepali_names),
                "email": f"{random.choice(nepali_names).lower()}@example.com",
                "password": "password123",
                "is_admin": random.choice([True, False]),
                "is_approved": random.choice([True, False])
            }
            for _ in range(20)
        ]

        for user_data in users:
            user, created = User.objects.update_or_create(
                email=user_data['email'],
                defaults={
                    'name': user_data['name'],
                    'is_admin': user_data['is_admin'],
                    'is_approved': user_data['is_approved'],
                    'completed_article_count': random.randint(0, 10),
                    'date_joined': timezone.now()
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded users'))
