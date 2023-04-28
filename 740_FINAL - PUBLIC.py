import os
import time
import threading
import psutil
from twilio.rest import Client

account_sid = '<TWILIO ACCOUNT NUMBER>'
auth_token = '<TWILIO TOKEN>'
client = Client(account_sid, auth_token)

#Message parameters and info:

def send_text(message_body):
    message = client.messages.create(
        body=message_body,
        from_="<YOUR TWILIO NUMBER HERE>",
        to="<YOUR PHONE NUMBER HERE>"
    )
    print(message.sid)


class FolderMonitor:

    #This function establishes baseline variables
    def __init__(self, path):
        self.path = path
        self.last_access_time = None
        self.is_running = False
        self.lock = threading.Lock()
        self.alert_sent = False  # Flag to track if alert has been sent


    #This kicks things off
    def start(self):
        self.is_running = True
        thread_folder = threading.Thread(target=self.monitor_folder_access)
        thread_cmd = threading.Thread(target=self.monitor_cmd_access)
        thread_folder.start()
        thread_cmd.start()


    #Checks to see if its already running
    def stop(self):
        self.is_running = False

    
#GUI check: continually checking for last access time of designated folder; if it ever changes to current time, then it triggers

    def monitor_folder_access(self):
        while self.is_running:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            current_access_time = os.stat(self.path).st_atime
            if self.last_access_time is None:
                self.last_access_time = current_access_time
            elif self.last_access_time != current_access_time:
                self.last_access_time = current_access_time
                self.folder_accessed(timestamp)


#Command line check: Using psutil to search by processes called cmd.exe or powershell.exe and correlating cwd of a designated folder; if true it triggers

    def monitor_cmd_access(self):
        while self.is_running:
            cmd_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cwd', 'ppid']):
                if proc.info['name'] == 'cmd.exe' or proc.info['name'] == 'powershell.exe':
                    cmd_procs.append(proc)
            
            #Cwd check
            for proc in cmd_procs:
                current_dir = proc.info['cwd']
                if current_dir == r'<YOUR FOLDER PATH HERE>':
                    PPID = proc.info['ppid']
                    PID = proc.info['pid']
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    self.cmd_folder_accessed(PPID, PID, timestamp)

            time.sleep(5)

#Two respective functions to send the alerts, based on the above trigger functions 

    def folder_accessed(self, timestamp):
        if not self.alert_sent:  # Only send alert if it has not been sent before
            send_text(f'Someone opened the Passwords1 folder! Timestamp: {timestamp}')
            self.alert_sent = True

    def cmd_folder_accessed(self, PPID, PID, timestamp):
        if not self.alert_sent:  # Only send alert if it has not been sent before
            send_text(
                f'Someone opened the Passwords1 folder from the command line! PPID: {PPID}, PID: {PID}, Timestamp: {timestamp}')
            self.alert_sent = True


folder_monitor = FolderMonitor("<YOUR FOLDER PATH HERE>")
folder_monitor.start()

# Wait for designated amount of time
time.sleep(120)

folder_monitor.stop()