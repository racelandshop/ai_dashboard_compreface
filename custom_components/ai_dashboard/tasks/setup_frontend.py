""""Starting setup task: Frontend"."""
from __future__ import annotations
from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from ..base import AIFacialDashboardBase
from ..const import DOMAIN, SetupStage
from ..hacs_frontend import locate_dir
from ..hacs_frontend.version import VERSION as FE_VERSION
from .base import AIFacialDashboardTask

URL_BASE = "/hacsfiles"

async def async_setup_task(hacs: AIFacialDashboardBase, hass: HomeAssistant) -> Task:
    """Set up this task."""
    return Task(hacs=hacs, hass=hass)


class Task(AIFacialDashboardTask):
    """Setup the HACS frontend."""

    stages = [SetupStage.SETUP]

    async def async_execute(self) -> None:
        """Execute the task."""

        # Register frontend
        if self.AIFacialDashboardBase.configuration.dev_mode == True:
            self.task_logger(
                self.AIFacialDashboardBase.log.warning,
                "Frontend development mode enabled. Do not run in production!",
            )
            self.hass.http.register_view(HacsFrontendDev())
        else:
            #
            self.hass.http.register_static_path(
                f"{URL_BASE}/frontend", locate_dir(), cache_headers=False
            )

        # Custom iconset
        self.hass.http.register_static_path(
            f"{URL_BASE}/iconset.js", str(self.AIFacialDashboardBase.integration_dir / "iconset.js")
        )
        if "frontend_extra_module_url" not in self.hass.data:
            self.hass.data["frontend_extra_module_url"] = set()
        self.hass.data["frontend_extra_module_url"].add(f"{URL_BASE}/iconset.js")

        self.AIFacialDashboardBase.frontend_version = FE_VERSION

        # Add to sidepanel if needed
        if DOMAIN not in self.hass.data.get("frontend_panels", {}):
            self.hass.components.frontend.async_register_built_in_panel(
                component_name="custom",
                sidebar_title=self.AIFacialDashboardBase.configuration.sidepanel_title,
                sidebar_icon=self.AIFacialDashboardBase.configuration.sidepanel_icon,
                frontend_url_path=DOMAIN,
                config={
                    "_panel_custom": {
                        "name": "ai-dashboard",
                        "embed_iframe": True,
                        "trust_external": False,
                        "js_url": f"/hacsfiles/frontend/entrypoint.js?hacstag={FE_VERSION}",
                    }
                },
                require_admin=True,
            )


class HacsFrontendDev(HomeAssistantView):
    """Dev View Class for HACS."""

    requires_auth = False
    name = "hacs_files:frontend"
    url = r"/hacsfiles/frontend/{requested_file:.+}"

    async def get(self, request, requested_file):  # pylint: disable=unused-argument
        """Handle HACS Web requests."""
        hacs: AIFacialDashboardBase = request.app["hass"].data.get(DOMAIN)
        requested = requested_file.split("/")[-1]
        request = await hacs.session.get(f"{hacs.configuration.frontend_repo_url}/{requested}")
        if request.status == 200:
            result = await request.read()
            response = web.Response(body=result)
            response.headers["Content-Type"] = "application/javascript"

            return response
