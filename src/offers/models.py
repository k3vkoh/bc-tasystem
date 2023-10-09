from django.db import models
from enum import Enum

class OfferStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

class Offer(models.Model):
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='offer_application')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='offer_course')
    recipient = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='offer_recipient')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='offer_sender')

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in OfferStatus], default=OfferStatus.PENDING.value)

    def __str__(self):
        return f'Offer for {self.course} from {self.sender} to {self.recipient}'
    
    def get_status(self):
        return OfferStatus(self.status).name

    def accept(self):
        self.status = OfferStatus.ACCEPTED.value
        self.save()

    def reject(self):
        self.status = OfferStatus.REJECTED.value
        self.save()

    def reset(self):
        self.status = OfferStatus.PENDING.value
        self.save()       