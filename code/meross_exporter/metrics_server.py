import asyncio
import logging

from aiohttp import web
from meross_exporter.power_monitor import PowerMonitor

_LOGGER = logging.getLogger(__name__)

class MetricsServer:
  '''
    Initializer
  '''
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

  # Function to create and start the server
  async def async_run_app(self, run_for_second : int = -1):
    self._app = web.Application()
    self._app.add_routes([web.get('/metrics', self.handle_metrics)])  # Define routes
    
    runner = web.AppRunner(self._app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', self._port)
    await site.start()

    # Keep the server running
    _LOGGER.info(f'Metrics server running with run_for_second={run_for_second}...')
    if run_for_second > 0:
      # Run for a fix amount of time
      await asyncio.sleep(run_for_second)
      _LOGGER.info(f'Exiting metrics server.')
    else:
      # Run forever
      while True:
        await asyncio.sleep(3600)  # Sleep for an hour

  # A simple async handler function
  async def handle_metrics(self, request):
    target = request.query.get('target', 'default_value')
    
    if target in self._power_monitors:
      await self._power_monitors[target].fetch_power_metrics()
      power_metrics = self._power_monitors[target].get_power_metrics()
      response_text = ''
      for key in power_metrics:
        response_text += f'{key} {power_metrics[key]}\n'
    else:
      response_text = f"target {target} not exist"

    return web.Response(text=response_text)

# Main entry point to run the server
def main():
  server = MetricsServer(9090)
  server.run_app()


if __name__ == '__main__':
  main()