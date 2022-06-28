import os
import sys
import time
import psutil
import requests as requests
from dashing import HSplit, VSplit, VGauge, HGauge, Text


def publicIp() -> str:
    """
    request public ip api
    :return:
    """
    return requests.get('https://api.ipify.org/').text


def localIp() -> str:
    """
    ip in the network
    :return:
    """
    import socket
    return socket.gethostbyname(socket.gethostname())


def convertBytesToGigaBytes(value: int) -> str:
    """
    converte bytes to GB
    :param value:
    :return:
    """
    return f"{(((value / 1024) / 1024) / 1024):.2f} GB"


class DashMonitor:
    """
    Create a dashboard to monitoring the system
    """
    user_interface = HSplit( # horizontal window
            HSplit( # horizontal window
                VGauge(title='Used(RAM)'),
                VGauge(title='SWAP'),
                border_color=4,
                title="MEMORY"
                ),
            VSplit(
                HGauge(title='CPU'),
                HGauge(title='CPU_0'),
                HGauge(title='CPU_1'),
                HGauge(title='CPU_2'),
                HGauge(title='CPU_3'),
                HGauge(title='CPU_4'),
                HGauge(title='CPU_6'),
                border_color=5,
                title="CPU"
            ),
            VSplit(
                Text(f"DISK {psutil.disk_partitions()[0].device}: \nsize: "
                     f"{convertBytesToGigaBytes(psutil.disk_usage(psutil.disk_partitions()[0].device)[0])} \n"
            f"used: {convertBytesToGigaBytes(psutil.disk_usage(psutil.disk_partitions()[0].device)[1])}\n"
            f"read bytes {convertBytesToGigaBytes(psutil.disk_io_counters(True)['PhysicalDrive0'].read_bytes)}\n"
            f"write bytes {convertBytesToGigaBytes(psutil.disk_io_counters(True)['PhysicalDrive0'].write_bytes)}\n"
            , title='DISK'),
            Text(f"Public ip address: {publicIp()}\n"
                 f"Llocal ip address: {localIp()}"
                 , title='NETWORK')
            ,
                border_color=3,
                color=5
                ,
                title="OTHERS"

            ),)

    def __memoryINFO(self) -> None:
        """
        Updating constantly the dashboard
        :return:
        """
        while True:
            try:
                # MEMORY
                memory = self.user_interface.items[0]  # first hsplit

                # RAM MEMORY
                ram = memory.items[0]
                ram.value = psutil.virtual_memory().percent
                ram.title = f"RAM {ram.value} %"

                # SWAP MEMORY
                swap = memory.items[1]  # title
                swap.value = psutil.swap_memory().percent
                swap.title = f"SWAP {swap.value} %"

                try:
                    self.user_interface.display() # show
                    time.sleep(.6)
                except KeyboardInterrupt as ki:
                    break
            except KeyboardInterrupt as e:
                break

    def __cpuINFO(self) -> None:
        """
        Info about cpu
        :return:
        """

        while True:
            try:
                # CPU
                cpu = self.user_interface.items[1]
                cpu_used = cpu.items[0]
                cpu_used.value = psutil.cpu_percent()
                cpu_used.title = f"CPU {cpu_used.value}"

                # per cpu
                cores = cpu.items[1:7]
                core_percent = psutil.cpu_percent(percpu=True)
                for index, (c, v) in enumerate(zip(cores, core_percent)):
                    c.value = v
                    c.title = f'cpu_{index} {v} %'

                """# temperature  (INDISPONIBLE IN WINDOWS)
                temperature_cpu = self.user_interface[2]
                cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current
                title = f"TEMP {cpu_temp} C"
                temperature_cpu.value = cpu_temp
                temperature_cpu.title = title"""

                try:
                    self.user_interface.display() # show
                    time.sleep(.6)
                except KeyboardInterrupt as ki:
                    break
            except KeyboardInterrupt as e:
                break
        os.system('clear')
        sys.exit()

    def __diskINFO(self) -> None:
        """
        Updating constantly the dashboard the disk info
        :return:
        """
        while True:
            try:
                disk = self.user_interface.items[2]
                disk_ = disk.items[0]
                try:
                    self.user_interface.display() # show
                    time.sleep(.6)
                except KeyboardInterrupt as ki:
                    break
            except KeyboardInterrupt:
                sys.exit()

    def execute(self):
        """
        run dashboard
        :return:
        """
        self.__memoryINFO()
        self.__cpuINFO()
        self.__diskINFO()


if __name__ == '__main__':
    dash = DashMonitor()
    dash.execute()