from src.util.util_io import data_path
import subprocess
from datetime import datetime
import re

class VCRCodeCalculator:
    vcr_code_pattern = re.compile(
        'Program: ([^,]*), channel ([^,\(]*)[^,]*, at ([^\s]*) ([^,]*), duration ([^:]*):([^\.]*).'
    )

    channel_map = {
        '2': '2',
        '4': '4',
        '5': '5',
        '7': '7',
        '8': '8',
        '9': '9',
        '11': '11',
        '13': '13',
        '21': '21',
        '25': '25',
        '31': '31',
        '12': '41',
        '6': '47',
        '14': '49',
        '50': '50',
        '10': '55',
        '39': 'A&E',
        '35': 'AMC',
        '57': 'BET',
        '54': 'BRV',
        '23': 'CNBC',
        '42': 'CNN',
        '26': 'COM',
        '28': 'C-SPAN',
        '29': 'CUNY',
        '53': 'DIS',
        '63': 'E!',
        '34': 'ESPN',
        '88': 'ESPN2',
        '47': 'FAM',
        '67': 'FOOD',
        '74': 'FX',
        '33': 'HBO',
        '95': 'HBOPL',
        '87': 'HIST',
        '46': 'LIFE',
        '45': 'MAX',
        '19': 'MSG',
        '48': 'MTV',
        '38': 'NICK',
        '16': 'ODY',
        '32': 'ROM',
        '59': 'SC/FSN',
        '89': 'SCI-FI',
        '41': 'SHO',
        '80': 'STARZ',
        '43': 'TBS',
        '37': 'TDC/DSC',
        '51': 'TLC',
        '58': 'TMC',
        '49': 'TNN',
        '52': 'TNT',
        '77': 'TOON',
        '78': 'TVL',
        '44': 'USA',
        '62': 'VH1'
    }

    @staticmethod
    def from_vcr_code(year, month, day, vcr_code):
        out = subprocess.check_output([f'{data_path}/data/vcr_code.exe', '-y', str(year), '-m', str(month), '-d', str(day), str(vcr_code)]).decode()
        date, channel, time, am_pm, duration_hour, duration_minute = re.findall(VCRCodeCalculator.vcr_code_pattern, out)[0]
        hour, minute = map(int, time.split(':') if ':' in time else [time, 0])
        hour = hour + 12 if am_pm == 'PM' else hour
        dt = datetime.strptime(f'{date} {hour}:{minute}', '%B %d %Y %H:%M')
        duration_minutes = int(duration_hour) * 60 + int(duration_minute)
        return VCRCodeCalculator.channel_map[channel.strip()], dt, duration_minutes
