from models import Event
from datetime import datetime

def parse(line: str) -> Event:

    spaced = line.split(' ')
    quoted = line.split('"')

    # print("space delimit: ", spaced)
    # print("quote delimit: ", quoted)

    source_ip = spaced[0]
    
    dandtandz = spaced[3] + ":" + spaced[4]
    d_t_z = dandtandz.lstrip('[').rstrip(']')
    date_time_zone = datetime.strptime(d_t_z, "%d/%b/%Y:%H:%M:%S:%z")
    # print(date_time_zone)
    
    HTTP_group = quoted[1]
    http_method, endpoint, version = HTTP_group.split(' ')
    
    status_code = int(spaced[8])
    result_size = int(spaced[9])

    source_domain = quoted[3]
    user_agent = quoted[5]

    event = Event(
        source_ip,
        date_time_zone,
        http_method,
        endpoint,
        version,
        status_code,
        result_size,
        source_domain,
        user_agent
    )

    return event