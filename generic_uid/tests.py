from django.contrib.sites.models import Site
from django.test import TestCase
from generic_uid.models import UID

class Test(TestCase):
    def test_uid(self):
        # Baseline, 1 Site object.
        self.assertEqual(Site.objects.count(), 1)

        # Add unique ID to existing content object.
        site = Site.objects.get()
        UID.related.add('default', site)
        self.assertEqual(UID.objects.count(), 1)

        # Get content object.
        site2 = UID.related.get(Site, 'default')
        self.assertEqual(site, site2)

        # Remove unique ID without deleting its related content object.
        UID.related.remove(Site, 'default')
        self.assertEqual(Site.objects.count(), 1)
        self.assertEqual(UID.objects.count(), 0)

        # Create content object.
        site = UID.related.create(Site,
            'unique-id', name='site name', domain='domain.com')
        self.assertEqual(Site.objects.count(), 2)

        # Delete unique ID and its related content object.
        UID.related.delete(Site, 'unique-id')
        self.assertEqual(UID.objects.count(), 0)
        self.assertEqual(Site.objects.count(), 1)

        # Create with get_or_create().
        site, created = UID.related.get_or_create(Site,
            'unique-id', name='site name', domain='domain.com')
        self.assertTrue(created)

        # Get with get_or_create(). Ignore defaults.
        site, created = UID.related.get_or_create(Site,
            'unique-id', name='site name 2', domain='domain2.com')
        self.assertFalse(created)
        self.assertEqual(site.name, 'site name')

        # Create with update_or_create().
        site, created = UID.related.update_or_create(Site,
            'unique-id-2', name='site name', domain='domain.com')
        self.assertTrue(created)

        # Update with update_or_create().
        site, created = UID.related.update_or_create(Site,
            'unique-id-2', name='site name 2', domain='domain2.com')
        self.assertFalse(created)
        self.assertEqual(site.name, 'site name 2')

        # Multiple unique IDs for the same Site object.
        UID.related.add('unique-id-3', site)
        site3 = UID.related.get(Site, 'unique-id-3')
        self.assertEqual(site, site3)
        self.assertEqual(Site.objects.count(), 3)
        self.assertEqual(UID.objects.count(), 3)
