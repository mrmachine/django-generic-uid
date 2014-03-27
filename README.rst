Overview
========

Provides a model with a ``uid`` field and a generic foreign key that can be used
to uniquely identify the related content object, which might not itself have any
unique fields.

For example, Django's ``Site`` model has no unique fields, which makes it
difficult to reliably get, update or create a particular site.


Installation
============

1. Add ``generic_uid`` to your ``INSTALLED_APPS`` setting.

2. Apply database migrations::

    $ ./manage.py migrate generic_uid


Usage
=====

Use the ``UID.related`` manager to reliably get, create, update or delete
related content objects by their unique ID::

    # Create Site object.
    site = UID.related.create(
        Site, 'unique-id', name='name', domain='domain.com')

    # Add unique ID to existing Site object.
    UID.related.add('another-unique-id', site)

    # Remove unique ID without deleting its related Site object.
    UID.related.remove(Site, 'another-unique-id')

    # Get Site object.
    UID.related.get(Site, 'unique-id')

    # Get or create Site object.
    UID.related.get_or_create(
        Site, 'unique-id', name='name', domain='domain.com')

    # Update or create Site object.
    UID.related.update_or_create(
        Site, 'unique-id', name='name', domain='domain.com')

    # Delete UID and related Site object.
    UID.related.delete(Site, 'unique-id')
