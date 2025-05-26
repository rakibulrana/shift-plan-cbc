from django.db import models


# Choice options
CONTRACT_TYPES = [
    ('VZ', 'Full-Time'),
    ('TZ', 'Part-Time'),
    ('AZB', 'Internship'),
    ('SAH', 'Student Assistant'),
    ('AH', 'Mini Job'),
]

DAYS_OF_WEEK = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
]


class Employee(models.Model):
    name = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=4, choices=CONTRACT_TYPES)

    def __str__(self):
        return self.name
    

class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.day} ({self.start_time}–{self.end_time})"


class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    role = models.CharField(max_length=50, default='Küche')

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time} - {self.employee}"