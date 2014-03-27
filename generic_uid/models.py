from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models, transaction
import six

class RelatedManager(models.Manager):
    """
    Provides methods for managing related content objects by unique ID.
    """
    def _ct(self, model):
        """
        Returns a ContentType object for the given model.
        """
        content_type = ContentType.objects.get_for_model(model)
        return content_type

    def add(self, uid, content_object):
        """
        Adds a unique ID to the given content object. If the unique ID already
        exists, its content object will be updated.
        """
        try:
            with transaction.atomic():
                UID.objects.create(uid=uid, content_object=content_object)
        except IntegrityError:
            UID.objects \
                .filter(uid=uid, content_type=self._ct(type(content_object))) \
                .update(object_pk=content_object.pk)

    def create(self, model, uid, **kwargs):
        """
        Creates and returns a new content object.
        """
        with transaction.atomic():
            obj = model.objects.create(**kwargs)
            UID.objects.create(uid=uid, content_object=obj)
            return obj

    def delete(self, model, uid):
        """
        Deletes a unique ID and its related content object.
        """
        obj = UID.objects.get(uid=uid, content_type=self._ct(model))
        with transaction.atomic():
            obj.content_object.delete()
            obj.delete()

    def get(self, model, uid):
        """
        Gets an existing content object.
        """
        obj = UID.objects.get(uid=uid, content_type=self._ct(model))
        return obj.content_object

    def get_or_create(self, model, uid, **defaults):
        """
        Returns a content object and a boolean that indicates whether or not it
        was created. New objects will be created with ``defaults``.
        """
        try:
            return self.get(model, uid), False
        except UID.DoesNotExist:
            return self.create(model, uid, **defaults), True

    def remove(self, model, uid):
        """
        Deletes a unique ID without deleting its related content object.
        """
        UID.objects.filter(uid=uid, content_type=self._ct(model)).delete()

    def update_or_create(self, model, uid, **defaults):
        """
        Returns a content object and a boolean that indicates whether or not it
        was created. Existing objects will be updated with ``defaults``.
        """
        with transaction.atomic():
            try:
                obj = UID.objects.get(uid=uid, content_type=self._ct(model))
            except UID.DoesNotExist:
                return self.create(model, uid, **defaults), True
            # Lock content object for update.
            model.objects.select_for_update(pk=obj.object_pk)
            # Update.
            obj = obj.content_object
            for k, v in six.iteritems(defaults):
                setattr(obj, k, v)
            obj.save()
            return obj, False

class UID(models.Model):
    """
    Add a textual unique ID to any model with Django's generic relations.
    """
    uid = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType,
        related_name='content_type_set_for_%(app_label)s_%(class)s')
    object_pk = models.IntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_pk')
    objects = models.Manager()
    related = RelatedManager()

    class Meta:
        unique_together = ['uid', 'content_type']
