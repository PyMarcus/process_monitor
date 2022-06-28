import subprocess

import psutil as pu
import wmi as wmi


def convertBytesToGigaBytes(value: int) -> str:
    return f"{(((value / 1024) / 1024) / 1024):.2f} GB"


# virtual memory:
virtual_memory = pu.virtual_memory()
print("Virtual memory")
print(convertBytesToGigaBytes(virtual_memory[0])) # total GB
print(convertBytesToGigaBytes(virtual_memory[1])) # avaible GB
print(virtual_memory[2]) # percent used %
print(convertBytesToGigaBytes(virtual_memory[3])) # used GB
print(convertBytesToGigaBytes(virtual_memory[4])) # free GB (compatibility between systems)
print("AFTER ARRAY IN MEMORY")
array_alloc = list(range(1000000))


# CPU
print("CPU")
cpu = pu.cpu_freq()
print(f"{(cpu.current/1000):.2f} GHZ")  # current frequency
print(f"{(cpu.max/1000):.2f} GHZ") # max frequency
print(f"{(cpu.min/1000):.2f} GHZ")  # min frequency

core = pu.cpu_count()
print(core)  # with threads
print(pu.cpu_count(logical=False))  # fisical core
print(pu.cpu_percent(), end="%\n")
print(subprocess.getstatusoutput('vcgencmd measure_temp'))

# time used
print(f"{(pu.cpu_times().user / 60):.2f}", end=' min\n')  # time of use per min
print(f"{pu.cpu_times().system:.2f} ")  # sistem


# disk
print(convertBytesToGigaBytes(pu.disk_usage('C:')[0]))  # total
print(convertBytesToGigaBytes(pu.disk_usage('C:')[1]))  # used
print(convertBytesToGigaBytes(pu.disk_usage('C:')[2]))
for disk in pu.disk_partitions()[0].device.split():
    print(f"DISK {disk}\nsize: {convertBytesToGigaBytes(pu.disk_usage(disk)[0])} \n"
          f"used: {convertBytesToGigaBytes(pu.disk_usage(disk)[1])}")

    print(pu.disk_io_counters()) # bytes read
    print(convertBytesToGigaBytes(pu.disk_io_counters(True)['PhysicalDrive0'].write_bytes))  # bytes write