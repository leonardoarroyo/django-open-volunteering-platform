

def store_on_sf(sender, *args, **kwargs):
  """
  Schedule task for 7 days after apply asking if user has received contact from organization
  """
  instance = kwargs["instance"]

  if instance.channel.slug == "gdd" and kwargs["created"] and not kwargs["raw"]:
    if not instance.address:
        return None
    address = GoogleAddress.objects.get(pk=instance.address.pk)
    country = address.address_components.filter(types__name='country').first()
    if country:
        country = country.short_name
    else:
        return None
    managers = User.objects.filter(groups__name="mng-{}".format(country.lower()))

    for manager in managers:
      GDDMail(manager, async_mail=True).sendProjectCreatedToCountryManager({'project': instance})
post_save.connect(send_email_to_manager, sender=Project)
