import threading
from envir import *


window = tk.Tk()                                               
window.title('Elevator Dispatch')
window.geometry('960x600')

backgroud_image = tk.PhotoImage(file = 'source/BackGroud.png')
backgroud = tk.Label(window, image = backgroud_image, bd = 0).pack()

floor_label_1 = [tk.Label(window, text = 'F'+str(i+1), bd = 0,
                    bg = '#191919', fg = 'Lavender', 
                    width = 3, heigh = 2,
                    font = ('Arial',13)) for i in range(16)]
for i in range(0,16):
    floor_label_1[i].place(x=30, y=32*(15-i)+82, anchor=tk.CENTER)

floor_label_2 = [tk.Label(window, text = 'F'+str(i+1), bd = 0,
                    bg = '#191919', fg = 'Lavender', 
                    width = 3, heigh = 2,
                    font = ('Arial',13)) for i in range(16)]
for i in range(0,16):
    floor_label_2[i].place(x=820, y=32*(15-i)+82, anchor=tk.CENTER)

elevator_list = [Elevator(n, window) for n in range(0,5)]
ex_button = [tk.Button(window, bg = BUTTON_OFF_COLOR, bd = 2,
                       width = 24, heigh = 24, relief = BUTTON_TYPE) for i in range(0,30)]

up_image = tk.PhotoImage(file = 'source/up.png')
up_on_image = tk.PhotoImage(file = 'source/up_on.png')
down_image = tk.PhotoImage(file = 'source/down.png')
down_on_image = tk.PhotoImage(file = 'source/down_on.png')

for i in range(0,15):
    ex_button[i]['image'] = up_image
    ex_button[i].place(x=855, y=32*(15-i)+82, anchor=tk.CENTER)
for i in range(15,30):
    ex_button[i]['image'] = down_image
    ex_button[i].place(x=900, y=32*(30-i)+50, anchor=tk.CENTER)


def ex_button_callback(i):                                      # 外部按钮回调函数
    ex_button[i]['bg'] = BUTTON_ON_COLOR

    if i < 15:
        ex_button[i]['image'] = up_on_image
        floor = i
        direction = 1
    else:
        ex_button[i]['image'] = down_on_image
        floor = i-14
        direction = -1
    eleno = 0
    mindis = elevator_list[0].arrive_time(floor, direction)

    for n in range(1,5):
        t = elevator_list[n].arrive_time(floor, direction)
        if mindis > t:
            mindis = t
            eleno = n
    
    elevator_list[eleno].exterior_request(floor, direction)


for i in range(0,30):
    ex_button[i]['command'] = partial(ex_button_callback, i) 


def ex_button_recover():
    while True:
        mes = MQ.get()
        ex_button[mes]['bg'] = BUTTON_OFF_COLOR
        if mes < 15:
            ex_button[mes]['image'] = up_image
        else:
            ex_button[mes]['image'] = down_image
       

for i in range(0,5):
    threading.Thread(target = elevator_list[i].run).start()

threading.Thread(target = ex_button_recover).start()

window.mainloop()
