"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    https://docs.pulpproject.org/pulpcore/plugins/plugin-writer/index.html
"""
from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin import serializers as platform

from . import models


# FIXME: SingleArtifactContentSerializer might not be the right choice for you.
# If your content type has no artifacts per content unit, use "NoArtifactContentSerializer".
# If your content type has many artifacts per content unit, use "MultipleArtifactContentSerializer"
# If you want create content through upload, use "SingleArtifactContentUploadSerializer"
# If you change this, make sure to do so on "fields" below, also.
# Make sure your choice here matches up with the create() method of your viewset.
class HelmContentSerializer(platform.SingleArtifactContentSerializer):
    """
    A Serializer for HelmContent.

    Add serializers for the new fields defined in HelmContent and
    add those fields to the Meta class keeping fields from the parent class as well.

    For example::

    field1 = serializers.TextField()
    field2 = serializers.IntegerField()
    field3 = serializers.CharField()

    class Meta:
        fields = platform.SingleArtifactContentSerializer.Meta.fields + (
            'field1', 'field2', 'field3'
        )
        model = models.HelmContent
    """

    class Meta:
        fields = platform.SingleArtifactContentSerializer.Meta.fields
        model = models.HelmContent


class HelmRemoteSerializer(platform.RemoteSerializer):
    """
    A Serializer for HelmRemote.

    Add any new fields if defined on HelmRemote.
    Similar to the example above, in HelmContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.RemoteSerializer.Meta.validators + [myValidator1, myValidator2]

    By default the 'policy' field in platform.RemoteSerializer only validates the choice
    'immediate'. To add on-demand support for more 'policy' options, e.g. 'streamed' or 'on_demand',
    re-define the 'policy' option as follows::

    policy = serializers.ChoiceField(
        help_text="The policy to use when downloading content. The possible values include: "
                  "'immediate', 'on_demand', and 'streamed'. 'immediate' is the default.",
        choices=models.Remote.POLICY_CHOICES,
        default=models.Remote.IMMEDIATE
    )
    """

    class Meta:
        fields = platform.RemoteSerializer.Meta.fields
        model = models.HelmRemote


class HelmRepositorySerializer(platform.RepositorySerializer):
    """
    A Serializer for HelmRepository.

    Add any new fields if defined on HelmRepository.
    Similar to the example above, in HelmContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.RepositorySerializer.Meta.validators + [myValidator1, myValidator2]
    """

    class Meta:
        fields = platform.RepositorySerializer.Meta.fields
        model = models.HelmRepository


class HelmPublicationSerializer(platform.PublicationSerializer):
    """
    A Serializer for HelmPublication.

    Add any new fields if defined on HelmPublication.
    Similar to the example above, in HelmContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.PublicationSerializer.Meta.validators + [myValidator1, myValidator2]
    """

    class Meta:
        fields = platform.PublicationSerializer.Meta.fields
        model = models.HelmPublication


class HelmDistributionSerializer(platform.DistributionSerializer):
    """
    A Serializer for HelmDistribution.

    Add any new fields if defined on HelmDistribution.
    Similar to the example above, in HelmContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.DistributionSerializer.Meta.validators + [
            myValidator1, myValidator2]
    """

    publication = platform.DetailRelatedField(
        required=False,
        help_text=_("Publication to be served"),
        view_name_pattern=r"publications(-.*/.*)?-detail",
        queryset=models.Publication.objects.exclude(complete=False),
        allow_null=True,
    )

    # uncomment these lines and remove the publication field if not using publications
    # repository_version = RepositoryVersionRelatedField(
    #     required=False, help_text=_("RepositoryVersion to be served"), allow_null=True
    # )

    class Meta:
        fields = platform.DistributionSerializer.Meta.fields + ("publication",)
        model = models.HelmDistribution
