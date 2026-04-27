from random import choice


def get_from_table(**kwargs):
    return ["qwe", "asd", "zxc", "jke", "iop", "dfg", "cvb"][:kwargs['time']]

def get_service_status(**kwargs):
    statuses = ['running', 'stopped', 'stopped', 'stopped', 'stopped', 'error']
    return choice(statuses)
    
def restart_service(**kwargs):
    return f'{kwargs["service"]} restarted'