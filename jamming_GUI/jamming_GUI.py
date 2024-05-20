import tkinter as tk
import mysql.connector
from playsound import playsound

### Connect to Database: "mydatabase"
mydatabase = mysql.connector.connect(
    host="161.246.18.205",
    user="TTS",
    password="ttsproj",
    port=3306,
    database="Jamming2024_station01")


### Create a base window
root = tk.Tk()
root.geometry("1280x600")
root.minsize(1280,600)
root.configure(bg="#B3B6B7")
root.title("Jamming Monitor")


### Create a big frame for Monitoring
frame_monitor = tk.Frame(master=root, width=275, height=540, bg='#F2F3F4')
frame_monitor.place(x=30, y=30)

### Create subframe on the frame_monitor
subframe_status = tk.Frame(master=frame_monitor,width=215, height=30, bg='#F2F3F4')
subframe_status.place(x=30, y=30)

subframe_power_max = tk.Frame(master=frame_monitor, width=215, height=85 , bg='#2874A6')
subframe_power_max.place(x=30, y=80)

subframe_power_mean = tk.Frame(master=frame_monitor, width=215, height=85 , bg='#3498DB')
subframe_power_mean.place(x=30, y=195)

subframe_num_satellite = tk.Frame(master=frame_monitor, width=215, height=85 , bg='#2874A6')
subframe_num_satellite.place(x=30, y=310)

subframe_CNR_mean = tk.Frame(master=frame_monitor, width=215, height=85 , bg='#3498DB')
subframe_CNR_mean.place(x=30, y=425)

def create_subframe_monitor():

    ### Create label on subframe monitor
    label_header_status = tk.Label(master=subframe_status, text='Status : ')
    label_header_status.configure(font=("Arial", 16,"bold"))
    label_header_status.place(x=0,y=0)

    label_header_power_max = tk.Label(master=subframe_power_max, text='Power Max',fg="white",bg='#2874A6')
    label_header_power_max.configure(font=("Arial", 10))
    label_header_power_max.place(x=70,y=60)

    label_header_power_mean = tk.Label(master=subframe_power_mean, text='Power Mean',fg="white",bg='#3498DB')
    label_header_power_mean.configure(font=("Arial", 10))
    label_header_power_mean.place(x=70,y=60)

    label_header_num_satellite = tk.Label(master=subframe_num_satellite, text='Satellite',fg="white",bg='#2874A6')
    label_header_num_satellite.configure(font=("Arial", 10))
    label_header_num_satellite.place(x=80,y=60)

    label_header_CNR_mean = tk.Label(master=subframe_CNR_mean, text='CNR Mean',fg="white",bg='#3498DB')
    label_header_CNR_mean.configure(font=("Arial", 10))
    label_header_CNR_mean.place(x=75,y=60)


### Create a big frame for show data history
frame_data = tk.Frame(master=root, width=915, height=300, bg='#F2F3F4')
frame_data.place(x=335, y=30)

def create_subframe_data():

    ### Create sub-object on frame_data
    label_header_data_history = tk.Label(master=frame_data,text=' '*10+'ID'+' '*20+'DateTime'+' '*15+'Level'+' '*25+'Power-Max'+' '*17+'Power-Mean'+' '*12+'Num-Satellite'+' '*18+'CNR-Mean'+' '*10,fg='black',bg='#D2B4DE')
    label_header_data_history.configure(font=("Arial", 10,'bold'))
    label_header_data_history.place(x=0,y=0)


### Create a big frame for show report history
frame_report = tk.Frame(master=root, width=915, height=200, bg='#F2F3F4')
frame_report.place(x=335, y=370)

def create_subframe_report():

    ### Create sub-object on frame_report
    label_header_report_history = tk.Label(master=frame_report,text=' '*10+'ID'+' '*25+'Start'+' '*30+'Stop'+' '*16+'Duration'+' '*13+'Power-Max'+' '*8+'Power-Mean'+' '*6+'Satellite'+' '*13+'CNR-Mean'+' '*10,fg='black',bg='#D2B4DE')
    label_header_report_history.configure(font=("Arial", 10,'bold'))
    label_header_report_history.place(x=0,y=0)


def jamming_alarm():

    playsound('public-domain-beep-sound-100267.mp3')


def live_data():

    ### Get the value from Database
    try:
        mydatabase.reconnect()
        cursor = mydatabase.cursor()
        sql_get = '''SELECT ID, DateTime, Status_Level, Power_Max_dB, Power_Mean_dB, NUM_Satellite, CNR_Mean FROM Data ORDER BY ID DESC LIMIT 11'''
        
        cursor.execute(sql_get)
        data_history = cursor.fetchall()

        print(data_history[0])

        datetime = data_history[0][1]

        ### status_level, power_max, power_mean, num_satellite, CNR_mean
        label_body_status_level = tk.Label(master=frame_monitor,text=data_history[0][2])
        label_body_status_level.configure(font=("Arial", 16))
        label_body_status_level.place(x=120,y=30)

        label_body_power_max = tk.Label(master=subframe_power_max,text=str(data_history[0][3]),fg="white",bg='#2874A6')
        label_body_power_max.configure(font=("Arial", 18, 'bold'))
        label_body_power_max.place(x=55,y=20)

        label_body_power_mean = tk.Label(master=subframe_power_mean,text=str(data_history[0][4]),fg="white",bg='#3498DB')
        label_body_power_mean.configure(font=("Arial", 18, 'bold'))
        label_body_power_mean.place(x=55,y=20)

        label_body_num_satellite = tk.Label(master=subframe_num_satellite,text=str(data_history[0][5]),fg="white",bg='#2874A6')
        label_body_num_satellite.configure(font=("Arial", 18, 'bold'))
        label_body_num_satellite.place(x=85,y=20)

        label_body_CNR_mean = tk.Label(master=subframe_CNR_mean,text=str(data_history[0][6]),fg="white",bg='#3498DB')
        label_body_CNR_mean.configure(font=("Arial", 18, 'bold'))
        label_body_CNR_mean.place(x=75,y=20)

        if data_history[0][2] != 'Green':
            jamming_alarm() 
            
    except:
        pass

    show_data_history(data_history)


def show_data_history(data_history):

    y_axis = 25

    for row in data_history:

        x_axis = 0

        highlight = tk.Label(master=frame_data,text=(" "*240),fg="black",bg='#E8DAEF')
        highlight.configure(font=("Arial", 10))
        highlight.place(x=x_axis,y=y_axis)

        x_axis += 30

        for each in row:
            
            if x_axis == 175:
                x_axis -= 65

            show_data = tk.Label(master=frame_data,text=str(each),fg="black",bg='#E8DAEF')
            show_data.configure(font=("Arial", 10))
            show_data.place(x=x_axis,y=y_axis)

            x_axis += 145

        y_axis += 25


def show_report_history():

    ### Get the value from Database
    try:
        mydatabase.reconnect()
        cursor = mydatabase.cursor()
        sql_getreport = '''SELECT ID, Start_DateTime, Stop_DateTime, Duration, AVG_Power_Max_dB, AVG_Power_Mean_dB, AVG_NUM_Satellite, AVG_CNR_Mean FROM Report ORDER BY ID DESC LIMIT 7'''
        
        cursor.execute(sql_getreport)
        report_history = cursor.fetchall()

        y_axis = 25

        for row in report_history:
            
            x_axis = 0

            highlight = tk.Label(master=frame_report,text=(" "*240),fg="black",bg='#E8DAEF')
            highlight.configure(font=("Arial", 10))
            highlight.place(x=x_axis,y=y_axis)

            x_axis += 30

            for each in row:
                
                if x_axis == 175:
                    x_axis -= 65

                elif x_axis >= 500:
                    x_axis -= 35

                show_report = tk.Label(master=frame_report,text=str(each),fg="black",bg='#E8DAEF')
                show_report.configure(font=("Arial", 10))
                show_report.place(x=x_axis,y=y_axis)

                x_axis += 145

            y_axis += 25
            
    except:
        pass


def clear_frame_monitor():

    for widgets in subframe_status.winfo_children():
        widgets.destroy()

    for widgets in subframe_power_max.winfo_children():
        widgets.destroy()

    for widgets in subframe_power_mean.winfo_children():
        widgets.destroy()

    for widgets in subframe_num_satellite.winfo_children():
        widgets.destroy()

    for widgets in subframe_CNR_mean.winfo_children():
        widgets.destroy()

def clear_frame_data():

   for widgets in frame_data.winfo_children():
        widgets.destroy()


def clear_frame_report():

   for widgets in frame_report.winfo_children():
        widgets.destroy()        


def main_app():

    clear_frame_monitor()
    clear_frame_data()
    clear_frame_report()

    create_subframe_monitor()
    create_subframe_data()
    create_subframe_report()

    live_data()
    show_report_history()

    root.after(3000, main_app)

main_app()

root.mainloop()