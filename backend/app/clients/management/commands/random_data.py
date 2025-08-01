"""
Django management command to seed the database with sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clients.models import Client
from case_notes.models import CaseNote
from faker import Faker
import random

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seed the database with sample data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of caseworker users to create'
        )
        parser.add_argument(
            '--clients',
            type=int,
            default=20,
            help='Number of clients to create'
        )
        parser.add_argument(
            '--notes',
            type=int,
            default=50,
            help='Number of case notes to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🌱 Starting database seeding...')
        )

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                employee_id='EMP-ADMIN',
                department='IT'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created superuser: {admin.username}')
            )

        # Create caseworker users
        departments = ['Social Services', 'Mental Health', 'Family Support', 'Youth Services']
        caseworkers = []

        for i in range(options['users']):
            username = f'caseworker{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    employee_id=f'EMP-{1000 + i}',
                    department=random.choice(departments),
                    phone_number=fake.phone_number()[:15]
                )
                caseworkers.append(user)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created caseworker: {user.username}')
                )
            else:
                caseworkers.append(User.objects.get(username=username))

        # Create clients
        clients = []
        for i in range(options['clients']):
            client_id = f'CL-2024-{str(i+1).zfill(3)}'
            if not Client.objects.filter(client_id=client_id).exists():
                client = Client.objects.create(
                    client_id=client_id,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    assigned_caseworker=random.choice(caseworkers)
                )
                clients.append(client)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created client: {client.full_name} ({client.client_id})')
                )
            else:
                clients.append(Client.objects.get(client_id=client_id))

        # Create case notes
        interaction_types = ['phone', 'in-person', 'email', 'video', 'other']
        note_templates = [
            "Initial assessment completed. Client is cooperative and engaged.",
            "Follow-up meeting scheduled. Discussed progress on goals.",
            "Phone check-in completed. Client reported positive progress.",
            "Home visit conducted. Environment is safe and stable.",
            "Crisis intervention provided. Situation stabilized.",
            "Referral made to additional services. Client agreed to participate.",
            "Case plan review completed. Goals updated based on progress.",
            "Family meeting facilitated. Good communication established.",
            "Court hearing attended with client. Positive outcome achieved.",
            "Service coordination meeting held with other providers."
        ]

        for i in range(options['notes']):
            client = random.choice(clients)
            note = CaseNote.objects.create(
                client=client,
                content=random.choice(note_templates) + f" (Note #{i+1})",
                interaction_type=random.choice(interaction_types),
                created_by=client.assigned_caseworker
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created case note for {client.full_name}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Database seeding completed!\n'
                f'   - {len(caseworkers)} caseworkers created\n'
                f'   - {len(clients)} clients created\n'
                f'   - {options["notes"]} case notes created\n\n'
                f'💡 Login credentials:\n'
                f'   Admin: admin / admin123\n'
                f'   Caseworkers: caseworker1-{options["users"]} / password123'
            )
        )