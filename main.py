
from os import system, get_terminal_size, path
from time import sleep
from subprocess import Popen, PIPE
from psutil import cpu_percent, getloadavg, virtual_memory, swap_memory, disk_usage, disk_io_counters, \
    net_io_counters, sensors_temperatures, cpu_freq, disk_partitions


def display_ui(cpu_name, gpu_name, cpu_temp, gpu_stats, cpu_util, system_load, cpu_fr, phy_mem, swa_mem, disks_usage,
               disk_io_speed, disk_temps, net_io_speed):
    columns = get_terminal_size().columns
    tab_width = int(columns / 3)
    column_width = 35
    column0 = []
    column1 = []
    column2 = []
    system("clear")
    print("-".center(columns, "-"))
    print("Py-Mon ".center(columns))
    print("-".center(columns, "-"))
    print("")
    column0.append(expand_string(cpu_name, column_width))
    column0.append(expand_string("", column_width))
    counter = -1

    for util in cpu_util:

        if counter == -1:
            column0.append(expand_string("      Utilization: " + str(util) + "%", column_width))
        else:
            column0.append(expand_string("                " + str(counter) + ": " + str(util) + "%", column_width))

        counter += 1

    column0.append(expand_string("", column_width))
    counter = -1

    for freq in cpu_fr:

        if counter == -1:
            column0.append(expand_string("        Frequency: " + str(freq) + " MHz", column_width))
        else:
            column0.append(expand_string("                " + str(counter) + ": " + str(freq) + " MHz", column_width))

        counter += 1

    column0.append(expand_string("", column_width))
    column0.append(expand_string("      Load - 1min: " + str(system_load[0]), column_width))
    column0.append(expand_string("             5min: " + str(system_load[1]), column_width))
    column0.append(expand_string("            15min: " + str(system_load[2]), column_width))
    column0.append(expand_string("", column_width))
    counter = -1

    for temp in cpu_temp:

        if counter == -1:
            column0.append(expand_string("      Temperature: " + str(temp) + "°", column_width))
        else:
            column0.append(expand_string("                " + str(counter) + ": " + str(temp) + "°", column_width))

        counter += 1

    gpu_display = False

    for stat in gpu_stats:

        if stat != "":
            gpu_display = True

    if gpu_display:
        column0.append(expand_string("", column_width))
        column2.append(expand_string(gpu_name, column_width))
        column2.append(expand_string("", column_width))

        if gpu_stats[0] != "":
            column2.append(expand_string("      Temperature: " + str(gpu_stats[0]) + "°", column_width))

        if gpu_stats[1] != "":
            column2.append(expand_string("        Fan Speed: " + str(gpu_stats[1]) + " RPM", column_width))

        if gpu_stats[2] != "":
            column2.append(expand_string("            Power: " + str(gpu_stats[2]) + " W", column_width))

        if gpu_stats[3] != "":
            column2.append(expand_string("   Core Frequency: " + str(gpu_stats[3]) + " MHz", column_width))

        if gpu_stats[4] != "":
            column2.append(expand_string(" Memory Frequency: " + str(gpu_stats[4]) + " MHz", column_width))

        if gpu_stats[5] != "":
            column2.append(expand_string("             Load: " + str(gpu_stats[5]) + "%", column_width))

        column2.append(expand_string("", column_width))

    column2.append(expand_string("---------------Memory--------------", column_width))
    column2.append(expand_string("", column_width))
    column2.append(expand_string(" Physical - Total: " + str(phy_mem[0]) + " MB", column_width))
    column2.append(expand_string("             Used: " + str(phy_mem[1]) + " MB", column_width))
    column2.append(expand_string("        Available: " + str(phy_mem[2]) + " MB", column_width))
    column2.append(expand_string("", column_width))
    column2.append(expand_string("     Swap - Total: " + str(swa_mem[0]) + " MB", column_width))
    column2.append(expand_string("             Used: " + str(swa_mem[1]) + " MB", column_width))
    column2.append(expand_string("             Free: " + str(swa_mem[2]) + " MB", column_width))
    column2.append(expand_string("", column_width))
    column1.append(expand_string("---------------Disks---------------", column_width))
    column1.append(expand_string("", column_width))

    for disk in disk_io_speed:
        column1.append(expand_string(disk[0].rjust(10) + " - Read: " + str(disk[1]) + " MB/S", column_width))
        column1.append(expand_string("            Write: " + str(disk[2]) + " MB/S", column_width))
        column1.append(expand_string("", column_width))

    for disk in disks_usage:
        column1.append(expand_string(disk[0].rjust(9) + " - Total: " + str(disk[1]) + " MB", column_width))
        column1.append(expand_string("             Used: " + str(disk[2]) + " MB", column_width))
        column1.append(expand_string("             Free: " + str(disk[3]) + " MB", column_width))
        column1.append(expand_string("          Percent: " + str(disk[4]) + "%", column_width))
        column1.append(expand_string("", column_width))

    disk_temp_display = False

    for disk in disk_temps:

        if disk[1] != "0":
            disk_temp_display = True

    if disk_temp_display:
        for disk in disk_temps:
            column1.append(expand_string(disk[0].rjust(12) + " Temp: " + str(disk[1]) + "°", column_width))

        column1.append(expand_string("", column_width))

    column2.append(expand_string("--------------Network--------------", column_width))
    column2.append(expand_string("", column_width))
    column2.append(expand_string("             Send: " + str(net_io_speed[0]) + " Mb/S", column_width))
    column2.append(expand_string("         Received: " + str(net_io_speed[1]) + " Mb/S", column_width))
    column2.append(expand_string("", column_width))

    max_length = len(column0)

    if max_length < len(column1):
        max_length = len(column1)
    elif max_length < len(column2):
        max_length = len(column2)

    for x in range(0, max_length):
        line = ""

        if x < len(column0):
            line += column0[x].center(tab_width)
        else:
            line += " ".center(tab_width)

        if x < len(column1):
            line += column1[x].center(tab_width)
        else:
            line += " ".center(tab_width)

        if x < len(column2):
            line += column2[x].center(tab_width)
        else:
            line += " ".center(tab_width)

        print(line)


def expand_string(string, width):

    while len(string) < width:
        string += " "

    return string


def read_cpu_freq():
    cpu_fr = []
    cpu_fr.append(int(round(cpu_freq().current)))
    cpu_freqs = cpu_freq(percpu=True)

    for freq in cpu_freqs:
        cpu_fr.append(int(round(freq.current)))

    return cpu_fr


def read_cpu_name():
    file = open("/proc/cpuinfo", "r")

    for line in file:
        if "model name" in line:
            cpu_name = line[13:-1]

    cpu_name = cpu_name.replace("(R)", "")
    cpu_name = cpu_name.replace("(TM)", "")
    cpu_name = cpu_name.replace("CPU ", "")
    cpu_name = cpu_name[:33]

    while len(cpu_name) < 35:
        cpu_name = "-" + cpu_name

        if len(cpu_name) < 35:
            cpu_name = cpu_name + "-"

    return cpu_name


def read_cpu_temps():
    sensor_temps = sensors_temperatures()
    cpu_temps = sensor_temps["coretemp"]
    cpu_temp = []

    for items in cpu_temps:
        cpu_temp.append(int(items.current))

    return cpu_temp


def read_cpu_util():
    cpu_util = []
    cpu_util.append(cpu_percent())
    cpu_utils = cpu_percent(percpu=True)

    for util in cpu_utils:
        cpu_util.append(util)

    return cpu_util


def read_disk_io():
    per_disk = disk_io_counters(perdisk=True)
    disk_counters = []

    for disks in per_disk:
        disk_name = disks.title().upper()

        if len(disk_name) > 3:
            disk_to_remove = disk_name[:3]

            for old_disks in disk_counters:
                if old_disks[0] == disk_to_remove:
                    disk_counters.remove(old_disks)

        disk_io = per_disk[disks]
        disk = []
        disk.append(disk_name)
        disk.append(int(disk_io.read_bytes / 1048576))
        disk.append(int(disk_io.write_bytes / 1048576))
        disk_counters.append(disk)

    return sorted(disk_counters)


def read_disk_temp():
    per_disk = disk_io_counters(perdisk=True)
    disk_names = []
    disk_temps = []

    for disk in per_disk:
        disk_names.append(disk.title().lower())

    disk_names = sorted(disk_names)

    for name in disk_names:
        if len(name) < 4:
            full_name = "/dev/" + name
            disk = []
            disk.append(name.upper())

            try:
                mycall = Popen(["hddtemp", "--debug", full_name], stdout=PIPE)
                result = str(mycall.communicate())
            except:
                result = "0"
            else:
                mycall = Popen(["hddtemp", "--debug", full_name], stdout=PIPE)
                result = str(mycall.communicate())

                if "(190)" in result:
                    result = result.split("(190)")[1]
                    result = result[5:7]
                elif "(194)" in result:
                    result = result.split("(194)")[1]
                    result = result[5:7]
                else:
                    result = "0"
            finally:
                disk.append(result)
                disk_temps.append(disk)

    return disk_temps


def read_disk_usages():
    mountpoints = disk_partitions()
    mount_dir = []
    all_mount_info = []

    for mounts in mountpoints:
        mount_dir.append(mounts.mountpoint)

    for mount in mount_dir:
        mount_usage = []
        mount_usage.append(mount[-9:])
        mount_usage.append(int(disk_usage(mount).total / 1048576))
        mount_usage.append(int(disk_usage(mount).used / 1048576))
        mount_usage.append(int(disk_usage(mount).free / 1048576))
        mount_usage.append(disk_usage(mount).percent)
        all_mount_info.append(mount_usage)

    return all_mount_info


def read_gpu_name():
    gpu_name = ""
    mycall = Popen(["lspci"], stdout=PIPE)
    result = str(mycall.communicate())

    if "VGA compatible controller:" in result:
        result = result.split("VGA compatible controller:")[1]
        result = result.split("\\n")[0]

        if "[AMD/ATI]" in result:
            gpu_name = gpu_name + "AMD"
            result = result.split("[AMD/ATI]")[1]
            result = result.split("[")[1]
            result = result.split("]")[0]
            gpu_name = gpu_name + " " + result

    if gpu_name == "":
        gpu_name = "GPU"

    gpu_name = gpu_name[:33]

    while len(gpu_name) < 35:
        gpu_name = "-" + gpu_name

        if len(gpu_name) < 35:
            gpu_name = gpu_name + "-"

    return gpu_name


def read_gpu_stats():
    mem_fr = ""
    cor_fr = ""
    gpu_load = ""
    gpu_power = ""
    gpu_temp = ""
    gpu_fan = ""

    try:
        file = open("/sys/kernel/debug/dri/0/amdgpu_pm_info", "r")
        file.close()

    except:

        pass

    else:
        file = open("/sys/kernel/debug/dri/0/amdgpu_pm_info", "r")

        for line in file:

            if line[-7:-2] == "(MCLK":
                mem_fr = line[1:-12]

            if line[-7:-2] == "(SCLK":
                cor_fr = line[1:-12]

            if line[4:9] == "Load:":
                gpu_load = line[10:-3]

            if line[-14:-2] == "(average GPU":
                gpu_power = round(float(line[1:-17]), 2)

            if line[4:16] == "Temperature:":
                gpu_temp = line[17:-3]

        file.close()

    finally:
        counter = 0
        dir_search = True

        while dir_search:

            if path.isdir("/sys/class/hwmon/hwmon" + str(counter)):

                if path.exists("/sys/class/hwmon/hwmon" + str(counter) + "/name"):
                    file = open("/sys/class/hwmon/hwmon" + str(counter) + "/name", "r")
                    line = file.readline()

                    if "amdgpu" in line:
                        file.close()
                        file = open("/sys/class/hwmon/hwmon" + str(counter) + "/fan1_input", "r")
                        gpu_fan = file.readline().rstrip('\n')
                        file.close()

                counter += 1
            else:
                dir_search = False

        gpu_stats = []
        gpu_stats.append(gpu_temp)
        gpu_stats.append(gpu_fan)
        gpu_stats.append(gpu_power)
        gpu_stats.append(cor_fr)
        gpu_stats.append(mem_fr)
        gpu_stats.append(gpu_load)

        return gpu_stats


def read_net_io():
    net_io = []
    net_io.append(int(net_io_counters().bytes_sent / 131072))
    net_io.append(int(net_io_counters().bytes_recv / 131072))

    return net_io


def read_phy_mem():
    phy_mem = []
    phy_mem.append(int(virtual_memory().total / 1048576))
    phy_mem.append(int(virtual_memory().used / 1048576))
    phy_mem.append(int(virtual_memory().available / 1048576))

    return phy_mem


def read_swa_mem():
    swa_mem = []
    swa_mem.append(int(swap_memory().total / 1048576))
    swa_mem.append(int(swap_memory().used / 1048576))
    swa_mem.append(int(swap_memory().free / 1048576))

    return swa_mem


def read_system_load():

    return getloadavg()


def main_thread():
    run = True
    first_run = True
    cpu_name = read_cpu_name()
    gpu_name = read_gpu_name()

    while run:

        if first_run:
            disk_io_old = read_disk_io()
            net_io_old = read_net_io()
            first_run = False

        disk_io_new = read_disk_io()
        disk_io_speed = []
        counter = 0

        for disks in disk_io_old:
            disk = []
            disk_new = disk_io_new[counter]
            disk.append(disks[0])
            disk.append(disk_new[1] - disks[1])
            disk.append(disk_new[2] - disks[2])
            disk_io_speed.append(disk)
            counter += 1

        disk_io_old = disk_io_new
        net_io_new = read_net_io()
        net_io_speed = []
        net_io_speed.append(net_io_new[0] - net_io_old[0])
        net_io_speed.append(net_io_new[1] - net_io_old[1])
        net_io_old = net_io_new
        display_ui(cpu_name, gpu_name, read_cpu_temps(), read_gpu_stats(), read_cpu_util(), read_system_load(),
                   read_cpu_freq(), read_phy_mem(), read_swa_mem(), read_disk_usages(), disk_io_speed, read_disk_temp(),
                   net_io_speed)
        sleep(1)


main_thread()
