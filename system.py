#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ Системный Монитор и Менеджер
Мощный инструмент для мониторинга и управления вашим компьютером
Автор: ByredHub
"""

import psutil
import platform
import os
import time
from datetime import datetime, timedelta
import shutil
import socket
import subprocess
import sys

class Colors:
    """ANSI цвета для красивого вывода"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Дополнительные яркие цвета
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_RED = '\033[91m'
    WHITE = '\033[97m'

class SystemMonitor:
    """Класс для мониторинга системы"""
    
    @staticmethod
    def get_size(bytes, suffix="B"):
        """Конвертация байтов в читаемый формат"""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
    
    @staticmethod
    def get_system_info():
        """Получение информации о системе"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}🖥️  ИНФОРМАЦИЯ О СИСТЕМЕ{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        uname = platform.uname()
        print(f"{Colors.BOLD}Операционная система:{Colors.ENDC} {uname.system}")
        print(f"{Colors.BOLD}Имя компьютера:{Colors.ENDC} {uname.node}")
        print(f"{Colors.BOLD}Версия ОС:{Colors.ENDC} {uname.release}")
        print(f"{Colors.BOLD}Архитектура:{Colors.ENDC} {uname.machine}")
        print(f"{Colors.BOLD}Процессор:{Colors.ENDC} {uname.processor or platform.processor()}")
        
        # Время работы системы
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        print(f"{Colors.BOLD}Время запуска:{Colors.ENDC} {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.BOLD}Время работы:{Colors.ENDC} {str(uptime).split('.')[0]}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_cpu_info():
        """Получение информации о CPU"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}⚡ ПРОЦЕССОР (CPU){Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        # Количество ядер
        print(f"{Colors.BOLD}Физических ядер:{Colors.ENDC} {psutil.cpu_count(logical=False)}")
        print(f"{Colors.BOLD}Всего ядер:{Colors.ENDC} {psutil.cpu_count(logical=True)}")
        
        # Частота CPU
        cpufreq = psutil.cpu_freq()
        print(f"{Colors.BOLD}Максимальная частота:{Colors.ENDC} {cpufreq.max:.2f}Mhz")
        print(f"{Colors.BOLD}Минимальная частота:{Colors.ENDC} {cpufreq.min:.2f}Mhz")
        print(f"{Colors.BOLD}Текущая частота:{Colors.ENDC} {cpufreq.current:.2f}Mhz")
        
        # Загрузка CPU
        print(f"\n{Colors.BOLD}Загрузка CPU по ядрам:{Colors.ENDC}")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            bar = SystemMonitor.create_progress_bar(percentage)
            color = SystemMonitor.get_color_by_percentage(percentage)
            print(f"  Ядро {i}: {color}{bar} {percentage}%{Colors.ENDC}")
        
        total_cpu = psutil.cpu_percent(interval=1)
        bar = SystemMonitor.create_progress_bar(total_cpu)
        color = SystemMonitor.get_color_by_percentage(total_cpu)
        print(f"\n{Colors.BOLD}Общая загрузка CPU:{Colors.ENDC} {color}{bar} {total_cpu}%{Colors.ENDC}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_memory_info():
        """Получение информации о памяти"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}💾 ОПЕРАТИВНАЯ ПАМЯТЬ (RAM){Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        svmem = psutil.virtual_memory()
        print(f"{Colors.BOLD}Всего:{Colors.ENDC} {SystemMonitor.get_size(svmem.total)}")
        print(f"{Colors.BOLD}Доступно:{Colors.ENDC} {SystemMonitor.get_size(svmem.available)}")
        print(f"{Colors.BOLD}Используется:{Colors.ENDC} {SystemMonitor.get_size(svmem.used)}")
        
        bar = SystemMonitor.create_progress_bar(svmem.percent)
        color = SystemMonitor.get_color_by_percentage(svmem.percent)
        print(f"{Colors.BOLD}Процент использования:{Colors.ENDC} {color}{bar} {svmem.percent}%{Colors.ENDC}")
        
        # SWAP память
        swap = psutil.swap_memory()
        print(f"\n{Colors.BOLD}SWAP память:{Colors.ENDC}")
        print(f"  Всего: {SystemMonitor.get_size(swap.total)}")
        print(f"  Используется: {SystemMonitor.get_size(swap.used)}")
        bar = SystemMonitor.create_progress_bar(swap.percent)
        color = SystemMonitor.get_color_by_percentage(swap.percent)
        print(f"  Процент: {color}{bar} {swap.percent}%{Colors.ENDC}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_disk_info():
        """Получение информации о дисках"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}💿 ДИСКИ И РАЗДЕЛЫ{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"{Colors.BOLD}📁 Раздел: {partition.device}{Colors.ENDC}")
            print(f"  Точка монтирования: {partition.mountpoint}")
            print(f"  Файловая система: {partition.fstype}")
            
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                print(f"  Всего: {SystemMonitor.get_size(partition_usage.total)}")
                print(f"  Используется: {SystemMonitor.get_size(partition_usage.used)}")
                print(f"  Свободно: {SystemMonitor.get_size(partition_usage.free)}")
                
                bar = SystemMonitor.create_progress_bar(partition_usage.percent)
                color = SystemMonitor.get_color_by_percentage(partition_usage.percent)
                print(f"  Процент: {color}{bar} {partition_usage.percent}%{Colors.ENDC}")
            except PermissionError:
                print(f"  {Colors.YELLOW}⚠️  Нет доступа{Colors.ENDC}")
            print()
        
        # I/O дисков
        disk_io = psutil.disk_io_counters()
        print(f"{Colors.BOLD}Статистика I/O:{Colors.ENDC}")
        print(f"  Прочитано: {SystemMonitor.get_size(disk_io.read_bytes)}")
        print(f"  Записано: {SystemMonitor.get_size(disk_io.write_bytes)}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_network_info():
        """Получение информации о сети"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}🌐 СЕТЕВЫЕ ИНТЕРФЕЙСЫ{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        # Сетевые интерфейсы
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            print(f"{Colors.BOLD}🔌 Интерфейс: {interface_name}{Colors.ENDC}")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  IP адрес: {address.address}")
                    print(f"  Маска сети: {address.netmask}")
                    print(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"  MAC адрес: {address.address}")
            print()
        
        # Сетевая статистика
        net_io = psutil.net_io_counters()
        print(f"{Colors.BOLD}Сетевая статистика:{Colors.ENDC}")
        print(f"  Отправлено: {SystemMonitor.get_size(net_io.bytes_sent)}")
        print(f"  Получено: {SystemMonitor.get_size(net_io.bytes_recv)}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_processes_info(limit=10):
        """Получение информации о процессах"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}⚙️  ТОП {limit} ПРОЦЕССОВ ПО ИСПОЛЬЗОВАНИЮ CPU{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        # Получаем список процессов
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Сортируем по CPU
        processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        print(f"{Colors.BOLD}{'PID':<10} {'Имя процесса':<35} {'CPU %':<10} {'RAM %':<10}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.ENDC}")
        
        for proc in processes[:limit]:
            pid = proc['pid']
            name = proc['name'][:33]
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            
            cpu_color = SystemMonitor.get_color_by_percentage(cpu)
            print(f"{pid:<10} {name:<35} {cpu_color}{cpu:<10.2f}{Colors.ENDC} {mem:<10.2f}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def get_battery_info():
        """Получение информации о батарее"""
        if not hasattr(psutil, "sensors_battery"):
            return
        
        battery = psutil.sensors_battery()
        if battery is None:
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}🔋 БАТАРЕЯ{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Заряд:{Colors.ENDC} {battery.percent}%")
        print(f"{Colors.BOLD}Подключен к сети:{Colors.ENDC} {'Да' if battery.power_plugged else 'Нет'}")
        
        if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            time_left = timedelta(seconds=battery.secsleft)
            print(f"{Colors.BOLD}Время до разряда:{Colors.ENDC} {str(time_left).split('.')[0]}")
        
        bar = SystemMonitor.create_progress_bar(battery.percent)
        color = Colors.GREEN if battery.percent > 50 else Colors.YELLOW if battery.percent > 20 else Colors.RED
        print(f"{color}{bar}{Colors.ENDC}")
        
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    @staticmethod
    def create_progress_bar(percentage, length=30):
        """Создание прогресс-бара"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}]"
    
    @staticmethod
    def get_color_by_percentage(percentage):
        """Получение цвета в зависимости от процента"""
        if percentage < 50:
            return Colors.GREEN
        elif percentage < 80:
            return Colors.YELLOW
        else:
            return Colors.RED


class SystemManager:
    """Класс для управления системой"""
    
    @staticmethod
    def clean_temp_files():
        """Очистка временных файлов"""
        print(f"\n{Colors.YELLOW}🧹 Очистка временных файлов...{Colors.ENDC}\n")
        
        temp_dirs = []
        if platform.system() == "Windows":
            temp_dirs = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
            ]
        else:
            temp_dirs = ['/tmp']
        
        total_freed = 0
        files_deleted = 0
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            os.unlink(item_path)
                            total_freed += size
                            files_deleted += 1
                        elif os.path.isdir(item_path):
                            size = SystemManager.get_dir_size(item_path)
                            shutil.rmtree(item_path)
                            total_freed += size
                            files_deleted += 1
                    except Exception:
                        pass
        
        print(f"{Colors.GREEN}✅ Очистка завершена!{Colors.ENDC}")
        print(f"Удалено файлов/папок: {files_deleted}")
        print(f"Освобождено места: {SystemMonitor.get_size(total_freed)}\n")
    
    @staticmethod
    def get_dir_size(path):
        """Получение размера директории"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += SystemManager.get_dir_size(entry.path)
        except Exception:
            pass
        return total
    
    @staticmethod
    def kill_process(pid):
        """Завершение процесса по PID"""
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            process.terminate()
            print(f"{Colors.GREEN}✅ Процесс '{process_name}' (PID: {pid}) завершен{Colors.ENDC}")
        except psutil.NoSuchProcess:
            print(f"{Colors.RED}❌ Процесс с PID {pid} не найден{Colors.ENDC}")
        except psutil.AccessDenied:
            print(f"{Colors.RED}❌ Нет прав для завершения процесса{Colors.ENDC}")


def print_banner():
    """Вывод заголовка программы"""
    banner = f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🖥️  СИСТЕМНЫЙ МОНИТОР И МЕНЕДЖЕР  🖥️                     ║
║                                                                   ║
║          Полный контроль над вашим компьютером!                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)


def show_neofetch():
    """Показать красивый neofetch с логотипом ByredHub"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ASCII логотип - красивый и ровный
    logo = [
        f"{Colors.BRIGHT_CYAN}  ██████╗ ██╗   ██╗██████╗ ███████╗██████╗ {Colors.ENDC}",
        f"{Colors.BRIGHT_CYAN}  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗{Colors.ENDC}",
        f"{Colors.BRIGHT_BLUE}  ██████╔╝ ╚████╔╝ ██████╔╝█████╗  ██║  ██║{Colors.ENDC}",
        f"{Colors.BRIGHT_BLUE}  ██╔══██╗  ╚██╔╝  ██╔══██╗██╔══╝  ██║  ██║{Colors.ENDC}",
        f"{Colors.BRIGHT_MAGENTA}  ██████╔╝   ██║   ██║  ██║███████╗██████╔╝{Colors.ENDC}",
        f"{Colors.BRIGHT_MAGENTA}  ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═════╝ {Colors.ENDC}",
        "",
        f"{Colors.BRIGHT_YELLOW}      ╦ ╦╦ ╦╔╗ {Colors.ENDC}",
        f"{Colors.BRIGHT_YELLOW}      ╠═╣║ ║╠╩╗{Colors.ENDC}",
        f"{Colors.BRIGHT_YELLOW}      ╩ ╩╚═╝╚═╝{Colors.ENDC}",
    ]
    
    # Получение информации
    username = os.getenv('USERNAME') or os.getenv('USER') or 'User'
    hostname = platform.node()
    
    # CPU информация - улучшенное определение через PowerShell
    try:
        if platform.system() == "Windows":
            # Используем PowerShell вместо wmic
            result = subprocess.run(
                ['powershell', '-Command', 
                 "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            cpu_name = result.stdout.strip()
            if not cpu_name or 'error' in cpu_name.lower():
                cpu_name = platform.processor() or "Unknown CPU"
        else:
            # Для Linux
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_name = line.split(':')[1].strip()
                            break
                    else:
                        cpu_name = platform.processor() or "Unknown CPU"
            except:
                cpu_name = platform.processor() or "Unknown CPU"
    except:
        cpu_name = platform.processor() or "Unknown CPU"
    
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    cpu_info = f"{cpu_name} ({cores}C/{threads}T)"
    
    # GPU информация - улучшенное определение через PowerShell
    try:
        if platform.system() == "Windows":
            # Используем PowerShell вместо wmic
            result = subprocess.run(
                ['powershell', '-Command',
                 "Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            gpu_lines = result.stdout.strip().split('\n')
            # Берем первую видеокарту (основную)
            gpu_name = gpu_lines[0].strip() if gpu_lines and gpu_lines[0].strip() else "Unknown GPU"
        else:
            # Для Linux
            try:
                result = subprocess.run(
                    ['lspci'], capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if 'VGA' in line or 'Display' in line:
                        gpu_name = line.split(':')[-1].strip()
                        break
                else:
                    gpu_name = "Unknown GPU"
            except:
                gpu_name = "Unknown GPU"
    except:
        gpu_name = "Unknown GPU"
    
    # RAM информация
    mem = psutil.virtual_memory()
    ram_info = f"{SystemMonitor.get_size(mem.used)} / {SystemMonitor.get_size(mem.total)} ({mem.percent}%)"
    
    # Disk информация
    disk = psutil.disk_usage('/')
    disk_info = f"{SystemMonitor.get_size(disk.used)} / {SystemMonitor.get_size(disk.total)} ({disk.percent}%)"
    
    # Uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    uptime_parts = []
    if days > 0:
        uptime_parts.append(f"{days}д")
    if hours > 0:
        uptime_parts.append(f"{hours}ч")
    if minutes > 0:
        uptime_parts.append(f"{minutes}м")
    uptime_str = " ".join(uptime_parts) if uptime_parts else "< 1м"
    
    # Shell
    shell = os.path.basename(os.getenv('SHELL') or os.getenv('ComSpec') or 'Unknown')
    
    # Local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "N/A"
    
    # Разрешение экрана
    try:
        if platform.system() == "Windows":
            from ctypes import windll
            user32 = windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            resolution = f"{width}x{height}"
        else:
            resolution = "N/A"
    except:
        resolution = "N/A"
    
    # Дополнительная информация
    # CPU частота
    cpu_freq = psutil.cpu_freq()
    cpu_freq_str = f"{cpu_freq.current:.0f}MHz" if cpu_freq else "N/A"
    
    # Температура (если доступна)
    try:
        temps = psutil.sensors_temperatures() if hasattr(psutil, 'sensors_temperatures') else {}
        cpu_temp = "N/A"
        if temps:
            for name, entries in temps.items():
                if entries:
                    cpu_temp = f"{entries[0].current}°C"
                    break
    except:
        cpu_temp = "N/A"
    
    # Версия Python
    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Количество процессов
    process_count = len(psutil.pids())
    
    separator = f"{Colors.BRIGHT_CYAN}{'─' * 50}{Colors.ENDC}"
    
    # Информационные строки - красиво выровненные
    info = [
        f"{Colors.BRIGHT_GREEN}{Colors.BOLD}{username}@{hostname}{Colors.ENDC}",
        separator,
        f"{Colors.CYAN}🖥️  OS{Colors.ENDC}          {Colors.WHITE}{platform.system()} {platform.release()}{Colors.ENDC}",
        f"{Colors.CYAN}🏠 Host{Colors.ENDC}        {Colors.WHITE}{hostname}{Colors.ENDC}",
        f"{Colors.CYAN}🔧 Kernel{Colors.ENDC}      {Colors.WHITE}{platform.release()}{Colors.ENDC}",
        f"{Colors.YELLOW}⏱️  Uptime{Colors.ENDC}      {Colors.WHITE}{uptime_str}{Colors.ENDC}",
        f"{Colors.YELLOW}📦 Shell{Colors.ENDC}       {Colors.WHITE}{shell}{Colors.ENDC}",
        f"{Colors.WHITE}🔲 Resolution{Colors.ENDC}  {Colors.WHITE}{resolution}{Colors.ENDC}",
        separator,
        f"{Colors.BRIGHT_YELLOW}⚡ CPU{Colors.ENDC}         {Colors.WHITE}{cpu_info}{Colors.ENDC}",
        f"{Colors.BRIGHT_CYAN}📊 CPU Usage{Colors.ENDC}   {Colors.WHITE}{psutil.cpu_percent(interval=0.5)}%{Colors.ENDC}",
        f"{Colors.BRIGHT_CYAN}🔥 CPU Freq{Colors.ENDC}    {Colors.WHITE}{cpu_freq_str}{Colors.ENDC}",
        f"{Colors.BRIGHT_MAGENTA}🎮 GPU{Colors.ENDC}         {Colors.WHITE}{gpu_name}{Colors.ENDC}",
        f"{Colors.BRIGHT_GREEN}💾 Memory{Colors.ENDC}      {Colors.WHITE}{ram_info}{Colors.ENDC}",
        f"{Colors.BRIGHT_BLUE}💿 Disk{Colors.ENDC}        {Colors.WHITE}{disk_info}{Colors.ENDC}",
        separator,
        f"{Colors.YELLOW}🌐 Local IP{Colors.ENDC}    {Colors.WHITE}{local_ip}{Colors.ENDC}",
        f"{Colors.BRIGHT_MAGENTA}🐍 Python{Colors.ENDC}      {Colors.WHITE}{python_ver}{Colors.ENDC}",
        f"{Colors.CYAN}⚙️  Processes{Colors.ENDC}   {Colors.WHITE}{process_count}{Colors.ENDC}",
        separator,
    ]
    
    # Отображение логотипа и информации рядом
    print()
    for i in range(max(len(logo), len(info))):
        # Логотип слева (фиксированная ширина 50 символов без учета ANSI кодов)
        if i < len(logo):
            logo_part = logo[i]
            # Вычисляем реальную длину без ANSI кодов
            clean_logo = logo_part
            for color in [Colors.BRIGHT_CYAN, Colors.BRIGHT_BLUE, Colors.BRIGHT_MAGENTA, 
                         Colors.BRIGHT_YELLOW, Colors.BRIGHT_RED, Colors.ENDC]:
                clean_logo = clean_logo.replace(color, '')
            padding = 50 - len(clean_logo)
            logo_line = logo_part + ' ' * padding
        else:
            logo_line = ' ' * 50
        
        # Информация справа
        info_line = info[i] if i < len(info) else ""
        
        print(f"{logo_line}  {info_line}")
    
    print(f"\n{Colors.ENDC}")
    input(f"{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.ENDC}")


def print_menu():
    """Вывод главного меню"""
    menu = f"""
{Colors.BOLD}{Colors.YELLOW}📋 ГЛАВНОЕ МЕНЮ:{Colors.ENDC}

{Colors.GREEN}МОНИТОРИНГ:{Colors.ENDC}
  0  - ByredFetch (Neofetch с логотипом)
  1  - Информация о системе
  2  - Информация о CPU
  3  - Информация о памяти
  4  - Информация о дисках
  5  - Информация о сети
  6  - Топ процессов
  7  - Информация о батарее
  8  - Полный отчет (всё)

{Colors.GREEN}УПРАВЛЕНИЕ:{Colors.ENDC}
  9  - Очистить временные файлы
  10 - Завершить процесс (по PID)

{Colors.GREEN}ДРУГОЕ:{Colors.ENDC}
  11 - Непрерывный мониторинг CPU/RAM
  99 - Выход

{Colors.CYAN}{'='*70}{Colors.ENDC}
"""
    print(menu)


def continuous_monitor():
    """Непрерывный мониторинг"""
    print(f"{Colors.YELLOW}🔄 Непрерывный мониторинг (Ctrl+C для выхода){Colors.ENDC}\n")
    
    try:
        while True:
            # Очищаем экран
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"{Colors.BOLD}{Colors.CYAN}⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            bar = SystemMonitor.create_progress_bar(cpu_percent)
            color = SystemMonitor.get_color_by_percentage(cpu_percent)
            print(f"{Colors.BOLD}CPU:{Colors.ENDC} {color}{bar} {cpu_percent}%{Colors.ENDC}")
            
            # RAM
            mem = psutil.virtual_memory()
            bar = SystemMonitor.create_progress_bar(mem.percent)
            color = SystemMonitor.get_color_by_percentage(mem.percent)
            print(f"{Colors.BOLD}RAM:{Colors.ENDC} {color}{bar} {mem.percent}%{Colors.ENDC}")
            print(f"      Используется: {SystemMonitor.get_size(mem.used)} / {SystemMonitor.get_size(mem.total)}")
            
            # Диск
            disk = psutil.disk_usage('/')
            bar = SystemMonitor.create_progress_bar(disk.percent)
            color = SystemMonitor.get_color_by_percentage(disk.percent)
            print(f"{Colors.BOLD}ДИСК:{Colors.ENDC} {color}{bar} {disk.percent}%{Colors.ENDC}")
            print(f"       Свободно: {SystemMonitor.get_size(disk.free)} / {SystemMonitor.get_size(disk.total)}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Мониторинг остановлен{Colors.ENDC}\n")


def main():
    """Главная функция"""
    monitor = SystemMonitor()
    manager = SystemManager()
    
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input(f"{Colors.BOLD}{Colors.BLUE}Выберите опцию> {Colors.ENDC}").strip()
            
            if choice == '':
                continue
            elif choice == '0':
                show_neofetch()
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                continue
            elif choice == '1':
                monitor.get_system_info()
            elif choice == '2':
                monitor.get_cpu_info()
            elif choice == '3':
                monitor.get_memory_info()
            elif choice == '4':
                monitor.get_disk_info()
            elif choice == '5':
                monitor.get_network_info()
            elif choice == '6':
                try:
                    limit = input(f"Количество процессов (по умолчанию 10): ").strip()
                    limit = int(limit) if limit else 10
                    monitor.get_processes_info(limit)
                except ValueError:
                    monitor.get_processes_info(10)
            elif choice == '7':
                monitor.get_battery_info()
            elif choice == '8':
                monitor.get_system_info()
                monitor.get_cpu_info()
                monitor.get_memory_info()
                monitor.get_disk_info()
                monitor.get_network_info()
                monitor.get_battery_info()
            elif choice == '9':
                confirm = input(f"{Colors.YELLOW}Вы уверены? (да/нет): {Colors.ENDC}").strip().lower()
                if confirm in ['да', 'yes', 'y', 'д']:
                    manager.clean_temp_files()
            elif choice == '10':
                try:
                    pid = int(input("Введите PID процесса: ").strip())
                    confirm = input(f"{Colors.YELLOW}Завершить процесс {pid}? (да/нет): {Colors.ENDC}").strip().lower()
                    if confirm in ['да', 'yes', 'y', 'д']:
                        manager.kill_process(pid)
                except ValueError:
                    print(f"{Colors.RED}❌ PID должен быть числом{Colors.ENDC}")
            elif choice == '11':
                continuous_monitor()
            elif choice == '99':
                print(f"{Colors.CYAN}👋 До свидания!{Colors.ENDC}")
                break
            else:
                print(f"{Colors.RED}❌ Неверная опция!{Colors.ENDC}\n")
            
            if choice not in ['11', '99', '0']:
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.ENDC}")
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                
        except KeyboardInterrupt:
            print(f"\n{Colors.CYAN}👋 До свидания!{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка: {str(e)}{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
