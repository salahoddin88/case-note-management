"""
Django management command to seed the database with test data for the practical assessment
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clients.models import Client
from case_notes.models import CaseNote

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with specific test data for practical assessment'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Starting test data seeding...')
        )

        # Sample users (caseworkers) from the assessment specification
        test_users = [
            {"username": "sarah.smith", "first_name": "Sarah", "last_name": "Smith"},
            {"username": "john.doe", "first_name": "John", "last_name": "Doe"}
        ]

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

        # Create test caseworkers
        caseworkers = {}
        for user_data in test_users:
            username = user_data["username"]
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='testpass123',
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    employee_id=f'EMP-{username.upper().replace(".", "")}',
                    department='Community Services',
                    phone_number='+1234567890'
                )
                caseworkers[username] = user
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created caseworker: {user.username}')
                )
            else:
                caseworkers[username] = User.objects.get(username=username)

        # Sample clients from the assessment specification
        test_clients = [
            {
                "client_id": "CL-2024-001",
                "first_name": "Jane",
                "last_name": "Wilson",
                "assigned_caseworker": "sarah.smith"
            },
            {
                "client_id": "CL-2024-002",
                "first_name": "Robert",
                "last_name": "Brown",
                "assigned_caseworker": "sarah.smith"
            },
            {
                "client_id": "CL-2024-003",
                "first_name": "Maria",
                "last_name": "Garcia",
                "assigned_caseworker": "john.doe"
            }
        ]

        # Create test clients
        clients = []
        for client_data in test_clients:
            if not Client.objects.filter(client_id=client_data["client_id"]).exists():
                client = Client.objects.create(
                    client_id=client_data["client_id"],
                    first_name=client_data["first_name"],
                    last_name=client_data["last_name"],
                    assigned_caseworker=caseworkers[client_data["assigned_caseworker"]]
                )
                clients.append(client)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created client: {client.full_name} ({client.client_id})')
                )
            else:
                clients.append(Client.objects.get(client_id=client_data["client_id"]))

        # Create some sample case notes for demonstration
        sample_notes = [
            {
                "client_id": "CL-2024-001",
                "content": "Initial assessment completed. Client is seeking assistance with housing application. Discussed available options and next steps.",
                "interaction_type": "in-person"
            },
            {
                "client_id": "CL-2024-001",
                "content": "Follow-up phone call regarding housing application progress. Client has submitted required documents. Waiting for approval.",
                "interaction_type": "phone"
            },
            {
                "client_id": "CL-2024-002",
                "content": "Home visit conducted. Assessed living conditions and discussed family support services. Client expressed interest in parenting classes.",
                "interaction_type": "in-person"
            },
            {
                "client_id": "CL-2024-002",
                "content": "Email sent with information about parenting classes and registration details. Client confirmed attendance for next session.",
                "interaction_type": "email"
            },
            {
                "client_id": "CL-2024-003",
                "content": "Video consultation completed. Discussed employment support services and resume building. Scheduled follow-up meeting.",
                "interaction_type": "video"
            },
            {
                "client_id": "CL-2024-003",
                "content": "In-person meeting for resume review. Provided feedback and discussed interview preparation strategies.",
                "interaction_type": "in-person"
            }
        ]

        # Create case notes
        notes_created = 0
        for note_data in sample_notes:
            client = Client.objects.get(client_id=note_data["client_id"])
            
            # Check if a similar note already exists (to avoid duplicates)
            existing_note = CaseNote.objects.filter(
                client=client,
                content=note_data["content"]
            ).first()
            
            if not existing_note:
                note = CaseNote.objects.create(
                    client=client,
                    content=note_data["content"],
                    interaction_type=note_data["interaction_type"],
                    created_by=client.assigned_caseworker
                )
                notes_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created case note for {client.full_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Test data seeding completed!\n'
                f'   - {len(caseworkers)} caseworkers created\n'
                f'   - {len(clients)} clients created\n'
                f'   - {notes_created} case notes created\n\n'
                f'💡 Test login credentials:\n'
                f'   Admin: admin / admin123\n'
                f'   Sarah Smith: sarah.smith / testpass123\n'
                f'   John Doe: john.doe / testpass123\n\n'
                f'📋 Test clients:\n'
                f'   - Jane Wilson (CL-2024-001) assigned to Sarah Smith\n'
                f'   - Robert Brown (CL-2024-002) assigned to Sarah Smith\n'
                f'   - Maria Garcia (CL-2024-003) assigned to John Doe'
            )
        )
