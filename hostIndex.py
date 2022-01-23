import filesAndFolders
def get_host_indexes(p):
    hosts=filesAndFolders.create_hosts_yaml()
    devices=p.get_device_info_by_index
    host_index=[]
    for i in range(p.get_device_count()):
        for j in hosts.values():
            if (j in devices(i)["name"]):
                host_index.append(devices(i)["index"])
    return host_index  
