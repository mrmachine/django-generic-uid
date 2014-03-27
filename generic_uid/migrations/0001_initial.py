# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UID'
        db.create_table(u'generic_uid_uid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'content_type_set_for_generic_uid_uid', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'generic_uid', ['UID'])

        # Adding unique constraint on 'UID', fields ['uid', 'content_type']
        db.create_unique(u'generic_uid_uid', ['uid', 'content_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UID', fields ['uid', 'content_type']
        db.delete_unique(u'generic_uid_uid', ['uid', 'content_type_id'])

        # Deleting model 'UID'
        db.delete_table(u'generic_uid_uid')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic_uid.uid': {
            'Meta': {'unique_together': "(['uid', 'content_type'],)", 'object_name': 'UID'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_set_for_generic_uid_uid'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['generic_uid']