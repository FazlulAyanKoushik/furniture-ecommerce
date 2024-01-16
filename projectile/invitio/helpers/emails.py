from common.tasks import send_email_async


def send_connect_email(instance):
    target = instance.target
    owner = target.get_users().filter(role="OWNER").first()
    context = {
        "name": owner.user.get_name() if owner else "",
        "sender_name": instance.sender.get_name(),
        "organization": instance.organization.name,
        "message": instance.message,
    }
    template = "email/invites/organization_invite_en.html"
    email = target.email
    if target.is_status_placeholder():
        pass
    if target.is_status_pending() or target.is_status_active():
        template = "email/invites/organization_connect_en.html"
        email = owner.user.email
    subject = f"{context['sender_name']} wants to connect with you on Supplers!"
    send_email_async(context, template, email, subject)
