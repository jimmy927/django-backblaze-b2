from django.db import models

from django_backblaze_b2 import BackblazeB2Storage, LoggedInStorage, PublicStorage, StaffStorage


class ModelWithFiles(models.Model):
    b2_storagefile = models.FileField(
        name="b2_storagefile",
        upload_to="uploads",
        verbose_name="B2 Storage File",
        storage=BackblazeB2Storage,  # type: ignore
        blank=True,
    )
    public_file = models.FileField(
        name="public_file",
        upload_to="uploads",
        verbose_name="Public File",
        storage=PublicStorage,  # type: ignore
        blank=True,
    )
    logged_in_file = models.FileField(
        name="logged_in_file",
        upload_to="uploads",
        verbose_name="Logged-In File",
        storage=LoggedInStorage,  # type: ignore
        blank=True,
    )
    staff_file = models.FileField(
        name="staff_file",
        upload_to="uploads",
        verbose_name="Staff-Only File",
        storage=StaffStorage,  # type: ignore
        blank=True,
    )

    def __str__(self) -> str:
        return (
            f"f={self.b2_storagefile or '<none>'}"
            f", p={self.public_file or '<none>'}"
            f", li={self.logged_in_file or '<none>'}"
            f", s={self.staff_file or '<none>'}"
        )
