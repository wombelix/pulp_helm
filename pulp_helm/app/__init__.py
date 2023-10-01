from pulpcore.plugin import PulpPluginAppConfig


class PulpHelmPluginAppConfig(PulpPluginAppConfig):
    """Entry point for the helm plugin."""

    name = "pulp_helm.app"
    label = "helm"
    version = "0.1.0a1.dev"
    python_package_name = "pulp_helm"
