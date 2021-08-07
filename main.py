import time
import GPUtil
import subprocess
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
import smtplib
import psutil
import os



def make_toast(title, message):
    try:
        # create notifier
        nManager = notifications.ToastNotificationManager
        notifier = nManager.create_toast_notifier()

        # define your notification as string
        tString = """
            <toast>
                <visual>
                    <binding template='ToastGeneric'>
                        <text>{title}</text>
                        <text>{message}</text>
                    </binding>
                </visual>
            </toast>
            """

        # convert notification to an XmlDocument
        xDoc = dom.XmlDocument()
        xDoc.load_xml(tString.format(title=title, message=message))

        # display notification
        notifier.show(notifications.ToastNotification(xDoc))
    except:
        print("Couldn't make Toast")


def send_email(message):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        login_user = os.environ.get("DEFAULT_FROM_EMAIL_RAMLA")
        login_pass = os.environ.get("EMAIL_RAMLA_PASS")
        s.login(login_user, login_pass)
        massage = message
        receiver = os.environ.get("MY_EMAIL")
        s.sendmail(login_user, receiver, massage)
        s.quit()
    except:
        print("Error: Email not sent!")


def mine():
    os.startfile("start miner.bat")
    time.sleep(5)


if __name__ == '__main__':
    killed_mining = False
    mine()
    while True:
        # gpu power
        gpu_power = GPUtil.getGPUs()[0].load*100
        print(gpu_power)
        if gpu_power < 80:
            message = "Mining has stopped!!"
            make_toast("Miner Not Running", message)
            send_email(message)
            if not killed_mining:
                mine()
        # gpu temp
        gpu_temp = GPUtil.getGPUs()[0].temperature
        print(gpu_temp)
        if gpu_temp > 95:
            message = "Your GPU needs a BREAK!!"
            make_toast("GPU Overheating", message)
            send_email(message)
            for process in (process for process in psutil.process_iter() if process.name() == "cmd.exe"):
                process.kill()
            make_toast("Killed Mining Process", message)
            send_email("Killed Mining Process")
            killed_mining = True
        time.sleep(30)
