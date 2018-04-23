from django import forms
from django.utils.translation import ugettext_lazy as _

from ovp.apps.organizations.models import Organization

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.core.mixins import CountryFilterMixin
from ovp.apps.organizations import validators

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

# This file contains some "pragma: no cover" because the admin
# class is not covered by the test suite

class OrganizationResource(resources.ModelResource):
  organization = Field()
  address = Field()
  contact_name = Field()
  contact_email = Field()
  contact_phone = Field()
  
  class Meta:
    model = Organization
    exclude = ('cover', 'website', 'members', 'facebook_page', 'type', 'verified', 'channel', 'image', 'skills', 'causes', 'categories', 'commentaries', 'owner', 'name', 'slug', 'published', 'highlighted', 'max_applies_from_roles', 'max_applies', 'public_project', 'minimum_age', 'hidden_address', 'crowdfunding', 'published_date', 'closed', 'closed_date', 'deleted', 'deleted_date', 'created_date', 'modified_date', 'details', 'description')
  
  def dehydrate_organization(self, organization):
    return organization.name

  def dehydrate_address(self, organization):
    if organization.address is not None and organization.address is not None:
      return organization.address.typed_address

  def dehydrate_contact_name(self, organization):
    return organization.owner.name

  def dehydrate_contact_email(self, organization):
    return organization.owner.email

  def dehydrate_contact_phone(self, organization):
    return organization.owner.phone


class OrganizationAdmin(ImportExportModelAdmin, ChannelModelAdmin, CountryFilterMixin):
  fields = [
    ('id', 'highlighted'), ('name', 'slug'),
    ('owner'), #- 'type'

    ('published', 'deleted', 'verified'),
    ('published_date', 'deleted_date'),

    'address',
    'document',
    'image', 'cover',

    'facebook_page', 'website',

    'description', 'details',
    'causes', 'members',

    ('created_date', 'modified_date'),
    ]

  resource_class = OrganizationResource

  list_display = [
    'id', 'created_date', 'name', 'owner__email', 'owner__phone', 'address', 'highlighted', 'published', 'deleted', 'modified_date'
  ]

  list_filter = [
    'created_date', 'modified_date', 'highlighted', 'published', 'deleted'
  ]

  list_editable = [
    'highlighted', 'published'
  ]

  search_fields = [
    'name', 'owner__email', 'address__typed_address', 'description'
  ]

  readonly_fields = ['id', 'created_date', 'modified_date', 'published_date', 'deleted_date']


  filter_horizontal = ('causes', 'members')

  def owner__name(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.name
    else:
      return _('None')
  owner__name.short_description = _("Owner's Name")
  owner__name.admin_order_field = 'owner__name'

  def owner__email(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.email
    else:
      return _('None')
  owner__email.short_description = _("Owner's E-mail")
  owner__email.admin_order_field = 'owner__email'

  def owner__phone(self, obj): #pragma: no cover
    if obj.owner:
      return obj.owner.phone
    else:
      return _('None')
  owner__phone.short_description = _("Owner's Phone")
  owner__phone.admin_order_field = 'owner__phone'

  def get_queryset(self, request): #pragma: no cover
    qs = super(OrganizationAdmin, self).get_queryset(request)
    return self.filter_by_country(request, qs, 'address')


admin_site.register(Organization, OrganizationAdmin)

"""class document(InputMask):
    mask = {'mask': 'xx.xxx.xxx/xxxx-xx'}"""
