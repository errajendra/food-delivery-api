from user.models import Notification, CustomUser as User


def send_notification_job():
    notifications_qs = []
    users = User.objects.all()
    for user in users:
        notifications_qs.append(
            Notification(
                user = user,
                title = "Book Your Today Meal !",
                description = "This is reminder notification, if you not booked you today meal please book. "
            )
        )
    Notification.objects.bulk_create(notifications_qs, 100)
    print("This is my scheduled job!")
