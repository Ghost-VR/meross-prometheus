import asyncio
import logging

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.model.plugin.power import PowerInfo

from meross_exporter.power_monitor import PowerMonitor
from meross_exporter.metrics_server import MetricsServer

_LOGGER = logging.getLogger(__name__)

async def main():
  # Config logger
  logging.basicConfig(level=logging.INFO)

  # Initialize metrics server
  metrics_server = MetricsServer(port=9090) # 9090 by default

  # Login info
  login_file_name = 'config/login'
  with open(login_file_name) as f:
    content = f.read().splitlines()
    meross_email = content[0]
    meross_password = content[1]

  # Initialize meross api server
  # Setup the HTTP client API from user-password
  _LOGGER.info(f'Logging in with email {meross_email}')
  http_api_client = await MerossHttpClient.async_from_user_password(email=meross_email, password=meross_password, api_base_url="https://iot.meross.com")

  # Setup and start the device manager
  _LOGGER.info('Setup and start the device manager')
  manager = MerossManager(http_client=http_api_client)
  await manager.async_init()

  # Discover devices.
  await manager.async_device_discovery()

  # Get all electricity mixin devices and wrap them
  meross_electric_devices = manager.find_devices(device_class=ElectricityMixin)
  power_monitors = []
  for device in meross_electric_devices:
    power_monitors.append(PowerMonitor(device))
  
  # Initialize all power monitors, print once done
  _LOGGER.info('Initializing all power monitors')
  background_tasks = set()
  for monitor in power_monitors:
    _LOGGER.info(f'Initializing power monitor {monitor}')
    await monitor.init()

    # Register monitor with metrics server
    metrics_server.register_power_monitor(monitor)

    if False:
      _LOGGER.info(f'Starting run loop for {monitor}')
      task = asyncio.create_task(monitor.run())
      background_tasks.add(task)
      task.add_done_callback(background_tasks.discard)
  
  if False:
    # Wait for all background tasks to complete
    _LOGGER.info('Running forever...')
    await asyncio.gather(*background_tasks)

  await metrics_server.async_run_app()

  # Close the manager and logout from http_api
  # manager.close()
  # await http_api_client.async_logout()
  # _LOGGER.info('Exiting')


if __name__ == '__main__':
  asyncio.run(main())
