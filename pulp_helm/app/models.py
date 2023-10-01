"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    https://docs.pulpproject.org/pulpcore/plugins/plugin-writer/index.html
"""

from logging import getLogger

from django.db import models

from pulpcore.plugin.models import (
    Content,
    ContentArtifact,
    Remote,
    Repository,
    Publication,
    Distribution,
)

logger = getLogger(__name__)


class HelmContent(Content):
    """
    The "helm" content type.

    Define fields you need for your new content type and
    specify uniqueness constraint to identify unit of this type.

    For example::

        field1 = models.TextField()
        field2 = models.IntegerField()
        field3 = models.CharField()

        class Meta:
            default_related_name = "%(app_label)s_%(model_name)s"
            unique_together = (field1, field2)
    """

    TYPE = "helm"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class HelmPublication(Publication):
    """
    A Publication for HelmContent.

    Define any additional fields for your new publication if needed.
    """

    TYPE = "helm"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class HelmRemote(Remote):
    """
    A Remote for HelmContent.

    Define any additional fields for your new remote if needed.
    """

    TYPE = "helm"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class HelmRepository(Repository):
    """
    A Repository for HelmContent.

    Define any additional fields for your new repository if needed.
    """

    TYPE = "helm"

    CONTENT_TYPES = [HelmContent]

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class HelmDistribution(Distribution):
    """
    A Distribution for HelmContent.

    Define any additional fields for your new distribution if needed.
    """

    TYPE = "helm"

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"
