"""Constants for Pulp Helm plugin tests."""
from urllib.parse import urljoin

from pulp_smash.constants import PULP_FIXTURES_BASE_URL
from pulp_smash.pulp3.constants import (
    BASE_DISTRIBUTION_PATH,
    BASE_PUBLICATION_PATH,
    BASE_REMOTE_PATH,
    BASE_REPO_PATH,
    BASE_CONTENT_PATH,
)

# FIXME: list any download policies supported by your plugin type here.
# If your plugin supports all download policies, you can import this
# from pulp_smash.pulp3.constants instead.
# DOWNLOAD_POLICIES = ["immediate", "streamed", "on_demand"]
DOWNLOAD_POLICIES = ["immediate"]

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
HELM_CONTENT_NAME = "helm.unit"

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
HELM_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "helm/units/")

HELM_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, "helm/helm/")

HELM_REPO_PATH = urljoin(BASE_REPO_PATH, "helm/helm/")

HELM_PUBLICATION_PATH = urljoin(BASE_PUBLICATION_PATH, "helm/helm/")

HELM_DISTRIBUTION_PATH = urljoin(BASE_DISTRIBUTION_PATH, "helm/helm/")

# FIXME: replace this with your own fixture repository URL and metadata
HELM_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "helm/")
"""The URL to a helm repository."""

# FIXME: replace this with the actual number of content units in your test fixture
HELM_FIXTURE_COUNT = 3
"""The number of content units available at :data:`HELM_FIXTURE_URL`."""

HELM_FIXTURE_SUMMARY = {HELM_CONTENT_NAME: HELM_FIXTURE_COUNT}
"""The desired content summary after syncing :data:`HELM_FIXTURE_URL`."""

# FIXME: replace this with the location of one specific content unit of your choosing
HELM_URL = urljoin(HELM_FIXTURE_URL, "")
"""The URL to an helm file at :data:`HELM_FIXTURE_URL`."""

# FIXME: replace this with your own fixture repository URL and metadata
HELM_INVALID_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "helm-invalid/")
"""The URL to an invalid helm repository."""

# FIXME: replace this with your own fixture repository URL and metadata
HELM_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "helm_large/")
"""The URL to a helm repository containing a large number of content units."""

# FIXME: replace this with the actual number of content units in your test fixture
HELM_LARGE_FIXTURE_COUNT = 25
"""The number of content units available at :data:`HELM_LARGE_FIXTURE_URL`."""
