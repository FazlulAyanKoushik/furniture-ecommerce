from django.conf import settings
from django.db import models

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from .managers import NewsdeskPostQuerySet

from .choices import NewsdeskPostKind, NewsdeskPostStatus, NewsPostAccessKind
from .paths import get_newsdeskpost_image_path
from .slugifiers import get_newsdeskpost_slug, get_newsdeskpost_organization_slug


class NewsdeskPost(BaseModelWithUID):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from=get_newsdeskpost_slug, unique=True, db_index=True
    )
    summary = models.TextField(blank=True)
    image = VersatileImageField(
        upload_to=get_newsdeskpost_image_path, blank=True, null=True
    )
    description = models.TextField(blank=True)
    is_featured = models.BooleanField()
    kind = models.CharField(
        max_length=20,
        default=NewsdeskPostKind.EVENT,
        choices=NewsdeskPostKind.choices,
        db_index=True,
    )
    status = models.CharField(
        max_length=20, choices=NewsdeskPostStatus.choices, db_index=True
    )
    event_datetime = models.DateTimeField(blank=True, null=True)

    # FKs
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    organization = models.ForeignKey(
        "accountio.Organization", blank=True, null=True, on_delete=models.CASCADE
    )
    organization_slug = AutoSlugField(
        populate_from=get_newsdeskpost_organization_slug, unique=False, db_index=True
    )

    # custom managers use
    objects = NewsdeskPostQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Organization: ({self.organization}), Title: {self.title}, Slug: {self.slug}"


class NewsdeskContent(BaseModelWithUID):
    post = models.ForeignKey(NewsdeskPost, on_delete=models.CASCADE)
    content = models.TextField()
    frozen = models.TextField()


class NewsPostAccess(BaseModelWithUID):
    """
    Keep track of who has access to a Newspost
    * Can be shared with a Partner (an accountio.Organization instance)
    * Can be shared with a User (a core.User instance)
    """

    newspost = models.ForeignKey(NewsdeskPost, on_delete=models.CASCADE)
    partner = models.ForeignKey(
        "accountio.Organization", null=True, blank=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "core.User", null=True, blank=True, on_delete=models.CASCADE
    )
    kind = models.CharField(
        max_length=20,
        choices=NewsPostAccessKind.choices,
        default=NewsPostAccessKind.PARTNER,
    )

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            ("newspost", "partner"),
            ("newspost", "user"),
        )
        unique_together = (
            ("newspost", "partner"),
            ("newspost", "user"),
        )

    def __str__(self):
        try:
            if self.kind == NewsPostAccessKind.PARTNER:
                return (
                    f"Partner: ({self.partner.name}), Newspost: {self.newspost.title}"
                )
            if self.kind == NewsPostAccessKind.USER:
                return (
                    f"User: ({self.user.get_name()}), Newspost: {self.newspost.title}"
                )

        except AttributeError:
            pass

        return None
