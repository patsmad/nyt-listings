from src.util.util_io import data_path
import subprocess
from datetime import datetime, timedelta
import re
from typing import Optional

class ChannelInfo:
    def __init__(self, channel: str, time: datetime, duration_minutes: int):
        self.channel: str = channel
        self.time: datetime = time
        self.duration_minutes: int = duration_minutes

class VCRCodeCalculator:
    vcr_code_pattern: re.Pattern = re.compile(
        'Program: ([^,]*), channel ([^,\(]*)[^,]*, at ([^\s]*) ([^,]*), duration ([^:]*):([^\.]*).'
    )

    channel_list: list[(str, str)] = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('11', '11'),
        ('13', '13'),
        ('20', '20'),
        ('21', '21'),
        ('25', '25'),
        ('30', '30'),
        ('31', '31'),
        ('15', '38'),
        ('12', '41'),
        ('6', '47'),
        ('14', '49'),
        ('50', '50'),
        ('10', '55'),
        ('61', '61'),
        ('39', 'A&E'),
        ('35', 'AMC'),
        ('57', 'BET'),
        ('54', 'BRV'),
        ('23', 'CNBC'),
        ('42', 'CNN'),
        ('26', 'COM'),
        ('28', 'C-SPAN'),
        ('29', 'CUNY'),
        ('53', 'DIS'),
        ('63', 'E!'),
        ('34', 'ESPN'),
        ('88', 'ESPN2'),
        ('47', 'FAM'),
        ('67', 'FOOD'),
        ('74', 'FX'),
        ('33', 'HBO'),
        ('95', 'HBOPL'),
        ('87', 'HIST'),
        ('46', 'LIFE'),
        ('45', 'MAX'),
        ('19', 'MSG'),
        ('48', 'MTV'),
        ('38', 'NICK'),
        ('16', 'ODY'),
        ('32', 'ROM'),
        ('59', 'SC/FSN'),
        ('89', 'SCI-FI'),
        ('41', 'SHO'),
        ('80', 'STARZ'),
        ('43', 'TBS'),
        ('37', 'DSC'),
        ('51', 'TLC'),
        ('58', 'TMC'),
        ('49', 'TNN'),
        ('52', 'TNT'),
        ('77', 'TOON'),
        ('78', 'TVL'),
        ('44', 'USA'),
        ('62', 'VH1')
    ]
    number_to_channel: dict[str, str] = {a[0]: a[1] for a in channel_list}
    channel_to_number: dict[str, str] = {a[1]: a[0] for a in channel_list}

    @staticmethod
    def from_vcr_code(year: int, month: int, day: int, vcr_code: int, add_day: int) -> Optional[ChannelInfo]:
        try:
            out: str = subprocess.check_output([f'{data_path}/data/vcr_code.exe', '-y', str(year), '-m', str(month), '-d', str(day + add_day), str(vcr_code)]).decode()
            date, channel_str, time, am_pm, duration_hour, duration_minute = re.findall(VCRCodeCalculator.vcr_code_pattern, out)[0]
            hour, minute = map(int, time.split(':') if ':' in time else [time, 0])
            hour: int = hour + 12 if am_pm == 'PM' and hour < 12 else hour - 12 if am_pm in ['midnight', 'AM'] and hour == 12 else hour
            dt: datetime = datetime.strptime(f'{date} {hour}:{minute}', '%B %d %Y %H:%M')
            if add_day < 3:
                if abs(dt.day - day) > 3:
                    dt_plus_one = datetime(year, month, day) + timedelta(days=1)
                    return VCRCodeCalculator.from_vcr_code(dt_plus_one.year, dt_plus_one.month, dt_plus_one.day, vcr_code, add_day + 1)
                elif channel_str.strip() in VCRCodeCalculator.number_to_channel:
                    duration_minutes: int = int(duration_hour) * 60 + int(duration_minute)
                    channel: str = VCRCodeCalculator.number_to_channel[channel_str.strip()]
                    return ChannelInfo(channel, dt, duration_minutes)
                else:
                    print('ERROR: ' + out)
            else:
                print('ERROR: ' + out)
        except:
            print('Subprocess Error')

    @staticmethod
    def from_channel_info(channel_info: ChannelInfo) -> int:
        year: str = str(channel_info.time.year)
        month: str = str(channel_info.time.month)
        day: str = str(channel_info.time.day)
        channel_number: str = VCRCodeCalculator.channel_to_number[channel_info.channel]
        duration: str = str(channel_info.duration_minutes)
        out: bin = subprocess.check_output([f'{data_path}/data/vcr_code.exe', '-e',
                                       '-y', year, '-m', month, '-d', day,
                                       '-c', channel_number, '-t', channel_info.time.strftime('%H%M'),
                                       '-l', duration])
        return int(out)
