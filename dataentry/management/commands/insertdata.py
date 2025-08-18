from django.core.management.base import BaseCommand

from ...models import Student
class Command(BaseCommand):
    help = "Inserting data into Database"

    def handle(self, *args, **options):
        self.stdout.write("Inserting...")

        dataset = [
            {
                "roll_no": 7,
                "name": "Varun",
                "age": 19
            },
            {
                "roll_no": 6,
                "name": "Va",
                "age": 19
            },
            {
                "roll_no": 9,
                "name": "run",
                "age": 22
            },

        ]

        for student in dataset:
            roll_no = student['roll_no']
            if not Student.objects.filter(roll_no = roll_no).exists():
                Student.objects.create(roll_no = student['roll_no'], name = student['name'], age = student['age'])
            else:
                self.stderr.write(f"student with roll_no {roll_no} already exists")

        self.stdout.write(self.style.SUCCESS("Inserted Successfullyy"))