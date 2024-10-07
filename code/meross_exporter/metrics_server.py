import asyncio
import logging

from aiohttp import web
from meross_exporter.power_monitor import PowerMonitor

_LOGGER = logging.getLogger(__name__)

class MetricsServer:
  def __init__(
    self,
    port
  ) -> None:
    self._port = port
    self._app = None
    self._power_monitors = dict()
  
  def register_power_monitor(self, power_monitor : PowerMonitor) -> None:
    _LOGGER.info(f'Registered power monitor with lan ip {power_monitor._device.lan_ip}')
    self._power_monitors[power_monitor._device.lan_ip] = power_monitor

  # A simple async handler function
  async def handle_metrics(self, request):
    target = request.query.get('target', 'default_value')

    if target in self._power_monitors:
      await self._power_monitors[target].get_power_metrics()
      response_text = self._power_monitors[target].str_power_metrics()
    else:
      response_text = f"target {target} not exist"

    return web.Response(text=response_text)

  # Function to create and start the server
  async def async_run_app(self):
    self._app = web.Application()
    self._app.add_routes([web.get('/metrics', self.handle_metrics)])  # Define routes
    
    runner = web.AppRunner(self._app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', self._port)
    await site.start()

    # Keep the server running
    while True:
      await asyncio.sleep(3600)  # Sleep for an hour


# Main entry point to run the server
def main():
  server = MetricsServer(9090)
  server.run_app()

if __name__ == '__main__':
  main()