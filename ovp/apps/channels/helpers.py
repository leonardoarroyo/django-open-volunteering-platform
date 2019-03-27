from ovp.apps.channels.models import Channel

def get_subchannels_list(channel_slug="default"):
    channel = Channel.objects.get(slug=channel_slug)
    channel_list = [c.slug for c in channel.subchannels.all()]
    channel_list.append(channel_slug)

    return channel_list
