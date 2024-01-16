def get_payment_slug(instance):
    return f"{instance.name}"


def get_adfeature_slug(instance):
    return f"{instance.kind}-{instance.price}"
