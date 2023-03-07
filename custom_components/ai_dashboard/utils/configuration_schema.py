"""AI Facial Dashboard Configuration Schemas."""
# pylint: disable=dangerous-default-value
import voluptuous as vol

from ..const import LOCALE

# Configuration:
SIDEPANEL_TITLE = "sidepanel_title"
SIDEPANEL_ICON = "sidepanel_icon"
FRONTEND_REPO = "frontend_repo"
FRONTEND_REPO_URL = "frontend_repo_url"


# Options:
COUNTRY = "country"
DEBUG = "debug"
EXPERIMENTAL = "experimental"

# Config group
PATH_OR_URL = "frontend_repo_path_or_url"

def ai_facial_dashboard_config(options: dict = {}) -> dict:
    """Return a shcema for HACS configuration options."""
    if not options:
        options = {
            COUNTRY: "ALL",
            DEBUG: False,
            EXPERIMENTAL: False,
            SIDEPANEL_ICON: "mdi:face-recognition",
            SIDEPANEL_TITLE: "AI Dashboard",
            FRONTEND_REPO: "",
            FRONTEND_REPO_URL: "http://localhost:5000",
        }
    return {
        vol.Optional(SIDEPANEL_TITLE, default=options.get(SIDEPANEL_TITLE)): str,
        vol.Optional(SIDEPANEL_ICON, default=options.get(SIDEPANEL_ICON)): str,
        vol.Optional(COUNTRY, default=options.get(COUNTRY)): vol.In(LOCALE),
        vol.Optional(DEBUG, default=options.get(DEBUG)): bool,
        vol.Optional(EXPERIMENTAL, default=options.get(EXPERIMENTAL)): bool,
        vol.Exclusive(FRONTEND_REPO, PATH_OR_URL): str,
        vol.Exclusive(FRONTEND_REPO_URL, PATH_OR_URL): str,
    }
