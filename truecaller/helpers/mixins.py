from django.conf import settings
from safedelete import safedelete_mixin_factory, utils
from django.db import models

policy = settings.SAFE_DELETE_POLICY_SET[settings.SAFE_DELETE_POLICY]

# this mixin enables the soft-delete functionality # Issue #276 - soft delete
safe_delete_mixin = safedelete_mixin_factory(policy=policy)


class SafeDeleteMixinExtended(safe_delete_mixin):
    """
    Safe delete  mixin doesn't support cascade delete and un-delete
    So this will add the functionality to it.
    """

    def delete(self, *args, **kwargs):
        if policy == settings.SAFE_DELETE_POLICY_SET["SOFT_DELETE"]:
            related_objects = utils.related_objects(self)
            for related_object in related_objects:
                related_object.delete()

            self.deleted = True
            self.save(keep_deleted=True)

        else:
            super(self).delete()

    def undelete(self, *args, **kwargs):
        if policy == settings.SAFE_DELETE_POLICY_SET["SOFT_DELETE"]:
            related_objects = utils.related_objects(self)
            for related_object in related_objects:
                related_object.undelete()

            self.deleted = False
            self.save(keep_deleted=False)

        else:
            super(self).undelete()

    class Meta:
        abstract = True


class BaseMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True)  # This should add the created date on its own only once.
    updated_at = models.DateTimeField(
        auto_now=True)  # This should add the updated date every time.

    class Meta:
        abstract = True
