import threading
from envir import *

BACKGROUD_COLOR = 'black'

window = tk.Tk()                                                    # 创建窗口
window.title('Elevator scheduler')
window.geometry('1080x720')
window['bg'] = BACKGROUD_COLOR

floor_label_1 = [tk.Label(window, text = 'F'+str(i+1), bd = 0,      # 楼层标签
                    bg = BACKGROUD_COLOR, fg = 'Lavender', 
                    width = 3, heigh = 2,
                    font = ('Arial',13)) for i in range(20)]
for i in range(0,20):
    floor_label_1[i].place(x=30, y=32*(19-i)+82, anchor=tk.CENTER)

floor_label_2 = [tk.Label(window, text = 'F'+str(i+1), bd = 0,      # 楼层标签
                    bg = BACKGROUD_COLOR, fg = 'Lavender', 
                    width = 3, heigh = 2,
                    font = ('Arial',13)) for i in range(20)]
for i in range(0,20):
    floor_label_2[i].place(x=950, y=32*(19-i)+82, anchor=tk.CENTER)

elevator_list = [Elevator(n, window) for n in range(0,5)]           # 创建电梯列表

ex_button = [tk.Button(window, bg = BUTTON_OFF_COLOR, bd = 2,       # 外部按钮列表
                       width = 24, heigh = 24, relief = BUTTON_TYPE) for i in range(0,38)]

up_image = tk.PhotoImage(file = 'source/up.png')                    # 加载按钮图片
up_on_image = tk.PhotoImage(file = 'source/up_on.png')
down_image = tk.PhotoImage(file = 'source/down.png')
down_on_image = tk.PhotoImage(file = 'source/down_on.png')

for i in range(0,19):                                               # 布置按钮位置
    ex_button[i]['image'] = up_image
    ex_button[i].place(x=985, y=32*(19-i)+82, anchor=tk.CENTER)
for i in range(19,38):
    ex_button[i]['image'] = down_image
    ex_button[i].place(x=1030, y=32*(38-i)+50, anchor=tk.CENTER)


def ex_button_callback(i):                                          # 外部按钮回调函数
    ex_button[i]['bg'] = BUTTON_ON_COLOR

    if i < 19:
        ex_button[i]['image'] = up_on_image
        floor = i
        direction = 1
    else:
        ex_button[i]['image'] = down_on_image
        floor = i-18
        direction = -1
    eleno = 0
    mindis = elevator_list[0].arrive_time(floor, direction)

    for n in range(1,5):
        t = elevator_list[n].arrive_time(floor, direction)
        if mindis > t:
            mindis = t
            eleno = n
    
    elevator_list[eleno].exterior_request(floor, direction)


for i in range(0,38):                                              # 设置外部按钮回调函数
    ex_button[i]['command'] = partial(ex_button_callback, i) 


def ex_button_recover():                                           # 外部按钮恢复函数
    while True:
        mes = MQ.get()
        ex_button[mes]['bg'] = BUTTON_OFF_COLOR
        if mes < 19:
            ex_button[mes]['image'] = up_image
        else:
            ex_button[mes]['image'] = down_image
       

for i in range(0,5):                                               # 创建线程运行电梯
    threading.Thread(target = elevator_list[i].run).start()

threading.Thread(target = ex_button_recover).start()               # 创建线程运行外部按钮恢复函数

window.mainloop()                                                  # 启动主循环
