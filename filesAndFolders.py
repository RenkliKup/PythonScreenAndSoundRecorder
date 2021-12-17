import os 
import yaml
from pathlib import Path
def create_hosts_yaml():
    os.chdir("C:/RecordProgram/")
    if not os.path.exists("recorder.yaml"):
        with open("recorder.yaml","w",encoding="utf-8") as f:
            f.writelines("host_name_en: Stereo Mix (Realtek High Defini\n")
            f.writelines("host_name_tr: Stereo Karışımı (Realtek High Defini\n")
            f.writelines("mme: MME")
        hosts=yaml.full_load(open("recorder.yaml","r",encoding="utf-8"))
        return hosts
    hosts=yaml.full_load(open("recorder.yaml","r",encoding="utf-8"))
    return hosts

def create_path_yaml():
    log_path="C:\\RecordProgram\\logs"
    video_path="C:\\RecordProgram\\video"
    audio_clip_path="C:\\RecordProgram\\video\\output.wav"
    clip_path="C:\\RecordProgram\\video\\output.avi"
    dir="C:\\RecordProgram\\"
    mic_path="C:\\RecordProgram\\video\\microphone.wav"
    path_yaml_name="paths.yaml"
    os.chdir(dir)
    if not os.path.exists(path_yaml_name):
        with open(path_yaml_name,"w") as f:
            f.write(f"log_path: {log_path}\n")
            f.write(f"video_path: {video_path}\n")
            f.write(f"audio_clip_path: {audio_clip_path}\n")
            f.write(f"clip_path: {clip_path}\n")
            f.write(f"dir: {dir}\n")
            f.write(f"mic_path: {mic_path}\n")
        return yaml.full_load(open(path_yaml_name,"r",encoding="utf-8"))
    else:
        return yaml.full_load(open(path_yaml_name,"r",encoding="utf-8"))
        
def create_audio_devices_yaml(pyaudio):
    os.chdir("C:/RecordProgram/")
    with open("record_devices.txt","w",encoding="utf-8") as f:
            for i in range(pyaudio.get_device_count()):
                device=pyaudio.get_device_info_by_index(i)
                f.writelines("index:"+str(device["index"])+" name:"+device["name"]+"\n")

def create_control_txt():
    os.chdir("C:/RecordProgram/")
    with open("control.txt","w") as f:
        f.write("0")
        
def read_control_txt():
    num=None
    os.chdir("C:/RecordProgram")
    with open("control.txt","r") as f:
        num=f.read()
    if num=="0":
            return 0
    elif num=="1":
            return 1

def create_main_folder():
    os.chdir("C:/")
    if not os.path.exists("RecordProgram"):
        os.mkdir("RecordProgram")
    
def create_log_folder():
    os.chdir("C:/RecordProgram/")
    if not os.path.exists("logs"):
        os.mkdir("logs")
def create_video_folder():
    os.chdir("C:/RecordProgram/")
    if not os.path.exists("video"):
        os.mkdir("video")
        
        
def remove_file(dir):
        try:
            filenames = []
            for i in ["*.avi", "*.wav"]:
                filenames.extend([x for x in Path(dir+"video").glob("{}".format(i))])
            for j in range(len(filenames)):
                try:
                    os.remove(str(filenames[j]))
                except :
                    continue
        except Exception as e:
            pass
    