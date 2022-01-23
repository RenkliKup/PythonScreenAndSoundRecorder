import time
import threading
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os
import subprocess
import wave
import pyautogui
import numpy as np
import logs
import cv2
from SMWinservice import SMWinservice
import pyaudio
from win32api import GetSystemMetrics
import ffmpeg
from filesAndFolders import create_path_yaml,create_video_folder,remove_file,create_audio_devices_yaml,read_control_txt,create_main_folder,create_control_txt
from hostIndex import get_host_indexes
create_main_folder()
class RecorderPython(SMWinservice):
    global w,h,log_path,video_path,audio_clip_path,clip_path,dir,mic_path,logger
    
    create_control_txt()
    '''paths'''
    log_path=create_path_yaml()["log_path"]
    video_path=create_path_yaml()["video_path"]
    audio_clip_path=create_path_yaml()["audio_clip_path"]
    clip_path=create_path_yaml()["clip_path"]
    dir=create_path_yaml()["dir"]
    mic_path=create_path_yaml()["mic_path"]
    '''--------------'''
    
    
    '''width and height video '''
    
    w=GetSystemMetrics(0)
    h=GetSystemMetrics(1)
    
    '''---------------'''
    '''logs'''
    
    logger=logs.create_log_file(__name__,"record.log",log_path)
    
    '''---------------'''
    
    _svc_name_ = "CallCenterRecorder"
    _svc_display_name_ = "CallCenterRecorder"
    _svc_description_ = "CallCenterRecorder"
    
    def stop(self):
        self.isrunning=False
    def start(self):
        self.isrunning = True
    def rec(self):
        create_video_folder()
        
        try:
            remove_file(dir)
            
            writer = cv2.VideoWriter(clip_path, cv2.VideoWriter_fourcc(*"MJPG"), 13, (w, h))
            while True:
                
                    
                    frame = pyautogui.screenshot()
                    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
                    
                    writer.write(frame)
                    if read_control_txt()==0:
                        break

            writer.release()
            self.combine()
            
        except Exception as e:
            logger.error(str("Error Ocurred in Video Record"))

    def voice_record(self):
        
        try:
                
                remove_file(dir)
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 2
                RATE = 44100
                
                
                WAVE_OUTPUT_FILENAME = audio_clip_path
                p = pyaudio.PyAudio()
                host_index=get_host_indexes(p)
                create_audio_devices_yaml(p)
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK,
                                input_device_index=host_index[0])
                frames = []
                while True:
                    
                        data = stream.read(CHUNK)
                        frames.append(data)
                        if read_control_txt() == 0:
                            break
                        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(p.get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()
                stream.stop_stream()
                stream.close()
                p.terminate()
        except Exception as e:
            logger.error(str("Error Ocurred in Voice Record"))
            

    def thread(self):
        try:
            self.t1=threading.Thread(target=lambda: self.voice_record())
            self.t2=threading.Thread(target=lambda: self.rec())
            self.t1.start()
            self.t2.start()
            self.t1.join()
            self.t2.join()
            
        except Exception as e:
            logger.error(str("Error Ocurred in Threads"))
        

    def setDuration(self):
        try:
            audioclip = AudioFileClip(audio_clip_path)
            clip = VideoFileClip(clip_path)
            
            self.file_exist = 0
            while True:

                if os.path.exists(video_path+"\\"+str(self.file_exist) + ".avi") == 0:
                    durations1 = round(int(audioclip.duration) / int(clip.duration), 4)
                    file_loc = clip_path
                    output_loc = dir+"video\\{}.avi".format(self.file_exist)
                    set_duration = subprocess.Popen(f"ffmpeg -y -i {file_loc} -vf \"setpts={durations1}*PTS\" -r 24 {output_loc}",
                    stdout=subprocess.PIPE, shell=True)
                    
                    set_duration.communicate()
                    set_duration.kill()
                    break
                            
                else:
                    self.file_exist = self.file_exist + 1
            
        except Exception as e:
            logger.error(str("error occurred in setDuration"))
    def combine(self) :
        try:
            t = str(time.strftime('%X').replace(':', '.').replace("/", ".").replace("\\", "."))
            mp4_name = dir+"video\\{}.mp4".format(t)
            self.setDuration()
            time.sleep(5)
            if os.path.exists(mic_path):
                video_stream = ffmpeg.input(dir+'video\\{}.avi'.format(self.file_exist))
                combine_wav =subprocess.Popen(f'ffmpeg -y -i {audio_clip_path} -i {mic_path} -filter_complex "[0:0][1:0] amix=inputs=2:duration=longest" -c:a libmp3lame ./video/output5.wav',
                stdout=subprocess.PIPE, shell=True)
                combine_wav.communicate()
                combine_wav.kill()
                audio_stream = ffmpeg.input(dir+'video\\output5.wav')
                t = str(time.strftime('%X').replace(':', '.').replace("/", ".").replace("\\", "."))
                mp4_name = dir+"video\\{}.mp4".format(t)
                output_mp4=ffmpeg.output(audio_stream, video_stream, mp4_name)
                ffmpeg.run(output_mp4)
                remove_file(dir)
            
            else:
                video_stream = ffmpeg.input(dir+'video\\{}.avi'.format(self.file_exist))
                audio_stream = ffmpeg.input(dir+'video\\output.wav')
                output_mp4=ffmpeg.output(audio_stream, video_stream,mp4_name)
                ffmpeg.run(output_mp4)
                remove_file(dir)
                logger.error(str("there arent any microphone file"))
        except Exception as e:
            logger.error(str("error occured in combine"))
    def main(self):
        while True:        
            if read_control_txt()==1:
                
                self.thread()
if __name__=="__main__":
    RecorderPython.parse_command_line()