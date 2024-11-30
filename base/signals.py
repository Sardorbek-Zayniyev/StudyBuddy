from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . models import FriendRequest


@receiver(post_save, sender=FriendRequest)
def add_request_count(sender, instance, created, **kwargs):
    if created:
        if instance.status == 'requested':
            instance.sender.sent_request += 1
            instance.sender.save(update_fields=['sent_request'])
            instance.receiver.received_request += 1
            instance.receiver.save(update_fields=['received_request'])
        elif instance.status == 'accepted':
            instance.sender.following_count += 1
            instance.sender.save(update_fields=['following_count'])
            instance.receiver.followers_count += 1
            instance.receiver.save(update_fields=['followers_count'])


@receiver(post_save, sender=FriendRequest)
def delete_request_count(sender, instance, created, **kwargs):
    if not created and instance.status != 'accepted' and instance.status != 'rejected':
        instance.sender.sent_request -= 1
        instance.sender.save(update_fields=['sent_request'])
        instance.receiver.received_request -= 1
        instance.receiver.save(update_fields=['received_request'])


@receiver(post_save, sender=FriendRequest)
def add_follow_count(sender, instance, created, **kwargs):
    if not created and instance.status == 'accepted':
        instance.sender.following_count += 1
        instance.sender.save(update_fields=['following_count'])
        instance.receiver.followers_count += 1
        instance.receiver.save(update_fields=['followers_count'])


@receiver(post_delete, sender=FriendRequest)
def delete_follow_count(sender, instance, **kwargs):
    if instance.status == 'accepted':
        instance.sender.following_count -= 1
        instance.sender.save(update_fields=['following_count'])
        instance.receiver.followers_count -= 1
        instance.receiver.save(update_fields=['followers_count'])
    elif instance.status != 'rejected':
        instance.sender.sent_request -= 1
        instance.sender.save(update_fields=['sent_request'])
        instance.receiver.received_request -= 1
        instance.receiver.save(update_fields=['received_request'])
