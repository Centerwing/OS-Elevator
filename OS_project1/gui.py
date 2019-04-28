import threading
from envir import *


window = tk.Tk()                                               
window.title('Elevator Dispatch')
window.geometry('960x540')
window['bg'] = 'Snow'


elevator_list = [Elevator(n, window) for n in range(0,5)]
ex_button = [tk.Button(window, bg = BUTTON_OFF_COLOR,
                       width = 3, heigh = 1, relief = BUTTON_TYPE) for i in range(0,30)]
for i in range(0,9):
    ex_button[i].place(x=855, y=45*(9-i)+100, anchor=tk.CENTER)
for i in range(9,18):
    ex_button[i].place(x=900, y=45*(18-i)+55, anchor=tk.CENTER)


def ex_button_callback(i):
    ex_button[i]['bg'] = BUTTON_ON_COLOR

    if i < 15:
        floor = i
        direction = 1
    else:
        floor = i-14
        direction = -1
    eleno = 0
    mindis = 50
    for n in range(0,5):
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
       
for i in range(0,5):
    threading.Thread(target = elevator_list[i].run).start()

threading.Thread(target = ex_button_recover).start()

#img_png = tk.PhotoImage(file = 'Elevator.png')
#label_img = tk.Label(window, image = img_png)
#label_img.pack()

window.mainloop()
