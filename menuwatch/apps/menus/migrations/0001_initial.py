# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Food'
        db.create_table(u'menus_food', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('attrs', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_date', self.gf('django.db.models.fields.DateField')()),
            ('next_date', self.gf('django.db.models.fields.DateField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('meal', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('foodgroup', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('_hash', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'menus', ['Food'])

        # Adding model 'Watch'
        db.create_table(u'menus_watch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('food', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.Food'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.Profile'])),
            ('frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'menus', ['Watch'])

        # Adding model 'Profile'
        db.create_table(u'menus_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pro', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'menus', ['Profile'])


    def backwards(self, orm):
        # Deleting model 'Food'
        db.delete_table(u'menus_food')

        # Deleting model 'Watch'
        db.delete_table(u'menus_watch')

        # Deleting model 'Profile'
        db.delete_table(u'menus_profile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'menus.food': {
            'Meta': {'object_name': 'Food'},
            '_hash': ('django.db.models.fields.IntegerField', [], {}),
            'attrs': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'foodgroup': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_date': ('django.db.models.fields.DateField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'meal': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'next_date': ('django.db.models.fields.DateField', [], {})
        },
        u'menus.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'menus.watch': {
            'Meta': {'object_name': 'Watch'},
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['menus.Food']"}),
            'frequency': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['menus.Profile']"})
        }
    }

    complete_apps = ['menus']