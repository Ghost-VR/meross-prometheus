import asyncio
import logging

from meross_iot.controller.device import BaseDevice
from meross_iot.model.enums import Namespace

_LOGGER = logging.getLogger(__name__)

class PowerMonitor:
  def __init__(
    self,
    device: BaseDevice,
    update_interval = 1000 # In ms
  ) -> None:
    self._device = device
    self._power_info = None
    self._update_interval = update_interval

  async def init(self) -> None:
    await self._device.async_update()

  async def run_active(self) -> None:
    print(f'({self._device.name}) run() called')
    while True:
      await asyncio.sleep(self._update_interval / 1000)
      await self.fetch_power_metrics()
      print (self.str_power_metrics())

  async def fetch_power_metrics(self) -> None:
    self._power_info = await self._device.async_get_instant_metrics()
  
  def get_power_metrics(self) -> dict:
    return {
      'voltage_volt': self._power_info.voltage,
      'current_ampere': self._power_info.current,
      'power_watt': self._power_info.power,
      'name': f'"{self._device.name}"'
    }

  def str_power_metrics(self) -> str:
    # _LOGGER.info(f"({self._device.name}) POWER = {self._power_info.power} W, VOLTAGE = {self._power_info.voltage} V, CURRENT = {self._power_info.current} A")
    return f"({self._device.name}) POWER = {self._power_info.power} W, VOLTAGE = {self._power_info.voltage} V, CURRENT = {self._power_info.current} A"

  def __str__(self):
    return f"- {self._device.name} ({self._device.type}) @{self._device.lan_ip}: {self._device.online_status}"
