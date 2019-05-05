import tkinter as tk
from time import sleep
from queue import Queue
from functools import partial

BUTTON_ON_COLOR = 'DarkOrange'
BUTTON_OFF_COLOR = 'lavender'
BUTTON_TYPE = 'flat'
OPEN_TIME = 1.5                       # 电梯开门的时间 
MOVE_TIME = 0.015                     # 移动1像素的时间

MQ = Queue(maxsize=20)                # 消息队列

class Elevator:
    def __init__(self, no, window):
        self.no = no                  # 电梯编号
        
        self.location = 0             # 电梯当前位置
        
        self.door = False             # 电梯门的状态

        self.door_signal = False      # 电梯开门信号

        self.pathwap = None           # 电梯轨道

        self.pic_file = None          
        self.pic = None               # 电梯图片

        self.create_elevator(window, no)
        
        self.open_button_pic = None
        self.open_button = None       # 开门按钮

        self.close_button_pic = None
        self.close_button = None      # 关门按钮
        
        self.alert_button_pic = None
        self.alert_button = None      # 报警按钮

        self.create_door_button(window, no)

        self.button = []              # 电梯内部楼层按钮

        self.create_floor_button(window, no)

        self.floor_label = None       # 楼层显示器

        self.state_pic = None
        self.state_label = None       # 电梯状态显示器

        self.create_label(window, no)

        self.state = 0                # 电梯当前工作状态(1-上行,0-静止,-1-下行)
        
        self.up_list = []             # 电梯上行的目标列表
        
        self.down_list = []           # 电梯下行的目标列表


    def create_elevator(self, window, no):
        self.pathwap = tk.Label(window, width = 4, heigh = 38, # 电梯轨道
                                bg = 'DimGray')
        self.pathwap.place(x=70+no*150,y=384,anchor=tk.CENTER)

        self.pic_file = tk.PhotoImage(file = 'source/ElevatorOff.png')
        self.pic = tk.Label(window, image = self.pic_file, bd = 2,
                           relief = 'raised')                  # 电梯图片
        self.pic.place(x=70+no*150, y=690, anchor = tk.CENTER)


    def create_door_button(self, window, no):
        self.open_button_pic = tk.PhotoImage(file = 'source/open.png') # 电梯开关门按钮
        self.close_button_pic = tk.PhotoImage(file = 'source/close.png')
        self.open_button = tk.Button(window, image = self.open_button_pic, bd = 2,
                                     bg = BUTTON_OFF_COLOR, command = partial(self.door_button_callback, 1),
                                     width = 24, heigh = 24, relief = BUTTON_TYPE)
        self.open_button.place(x=116+no*150,y=690,anchor=tk.CENTER)
        self.close_button = tk.Button(window, image = self.close_button_pic,bd = 2,
                                      bg = BUTTON_OFF_COLOR, command = partial(self.door_button_callback, 0),
                                      width = 24, heigh = 24, relief = BUTTON_TYPE)
        self.close_button.place(x=116+no*150,y=658,anchor=tk.CENTER)

        self.alert_button_pic = tk.PhotoImage(file = 'source/alert.png') # 电梯报警按钮
        self.alert_button = tk.Button(window, image = self.alert_button_pic, bd = 2,
                                      bg = BUTTON_OFF_COLOR,
                                      width = 24, heigh = 24, relief = BUTTON_TYPE).place(x=116+no*150,y=626,anchor=tk.CENTER)


    def create_floor_button(self, window, no): # 创建电梯内部按钮
        for i in range(0,20):
            self.button.append(tk.Button(window, command = partial(self.interior_request,i),
                                         text = str(i+1), width = 3, heigh = 1, bg = BUTTON_OFF_COLOR,
                                         relief = BUTTON_TYPE))
        for i in range(0,20):
            self.button[i].place(x=150+no*150, y=32*(19-i)+82, anchor=tk.CENTER)


    def create_label(self, window, no):
        self.floor_label = tk.Label(window, width = 2, heigh = 1, bd = 3, # 电梯楼层显示器
                                    text = str(self.location+1), font = ('Arial',18),
                                    fg = 'DodgerBlue', bg = 'black', relief = 'sunken')
        self.floor_label.place(x=70+no*150,y=45,anchor=tk.CENTER)

        self.state_pic = tk.PhotoImage(file = 'source/state_0.png')       # 电梯状态显示器
        self.state_label = tk.Label(window, width = 30, heigh = 30, bd = 3,
                                    image = self.state_pic,
                                    bg = 'black', relief = 'sunken')
        self.state_label.place(x=116+no*150,y=45,anchor=tk.CENTER)
        
    
    def set_location(self, location):
        self.location = location
        self.floor_label['text'] = str(self.location+1)


    def set_state(self, state):
        self.state = state
        if state == 0:
            self.state_pic['file'] = 'source/state_0.png'
        elif state == 1:
            self.state_pic['file'] = 'source/state_up.png'
        elif state == -1:
            self.state_pic['file'] = 'source/state_down.png'
        

    def insert_uplist(self, floor):                        # 插入上行列表
        if floor not in self.up_list:
            self.up_list.append(floor)
        self.up_list.sort()
        
        
    def insert_downlist(self, floor):                      # 插入下行列表
        if floor not in self.down_list:
            self.down_list.append(floor)
        self.down_list.sort()


    def interior_request(self, floor):                     # 处理内部请求
        if floor != self.location:
            self.button[floor]['bg'] = BUTTON_ON_COLOR

        if floor > self.location:
            self.insert_uplist(floor)
            if self.state == 0:
                self.set_state(1)
        elif floor < self.location:
            self.insert_downlist(floor)
            if self.state == 0:
                self.set_state(-1)


    def exterior_request(self, floor, direction):          # 处理外部请求        
        if self.state == 0:                                # 若电梯静止则改变电梯运行状态
            if floor > self.location:
                self.set_state(1)
            elif floor < self.location:
                self.set_state(-1)
            else:
                self.set_state(direction)
        
        if direction == 1:
            self.insert_uplist(floor)
        elif direction == -1:
            self.insert_downlist(floor)
            

    def up_max(self):                                        # 计算上行的最高层
        um = self.location
        if self.up_list:
            if self.up_list[-1] > um:
                um = self.up_list[-1]
        if self.down_list:
            if self.down_list[-1] > um:
                um = self.down_list[-1]
        return um


    def down_min(self):                                      # 计算下行的最低层
        dm = self.location
        if self.up_list:
            if self.up_list[0] < dm:
                dm = self.up_list[0]
        if self.down_list:
            if self.down_list[0] < dm:
                dm = self.down_list[0]
        return dm

            
    def arrive_time(self, floor, direction):                  # 计算达到时间,用于外部按钮的调度
        if self.state == 0:
            return abs(self.location - floor)
        else:
            if self.state == direction:                       # 同向   
                if (floor-self.location)*direction > 0:       # 同向且顺路
                    return abs(self.location - floor)
                else:                                         # 同向不顺路
                    if self.state == 1:
                        return 2*(self.up_max()-self.location)+abs(self.up_max()*2-self.location-floor)
                    else:
                        return 2*(self.location-self.down_min())+abs(self.down_min()*2-self.location-floor)
            else:                                             # 反向
                if self.state == 1:
                    return abs(self.up_max()*2-self.location-floor)
                else:
                    return abs(self.down_min()*2-self.location-floor)
                
            
    def run(self):                                            # 控制电梯运行
        while True:
            sleep(0.02)                                       # 控制基础循环时间
            
            if self.state == 1:
                if self.location in self.up_list:             # 将已到达的目标位置消去
                    self.up_list.remove(self.location)
                    self.send()
                    self.open_door()                          # 开门
                if len(self.up_list)==0 and len(self.down_list)==0:
                    self.set_state(0)
                elif (self.up_list and self.up_list[-1]>self.location)or(self.down_list and self.down_list[-1]>self.location):
                    self.move(1)                              # 上升
                else:
                    self.move(0)                              # 转向
            elif self.state == -1:
                if self.location in self.down_list:
                    self.down_list.remove(self.location)
                    self.send()
                    self.open_door()                          # 开门
                if len(self.up_list)==0 and len(self.down_list)==0:
                    self.set_state(0)
                elif (self.up_list and self.up_list[0]<self.location)or(self.down_list and self.down_list[0]<self.location):
                    self.move(-1)                             # 下降
                else:
                    self.move(0)                              # 转向


    def move(self, s):                                        # s=0: 电梯转向
        self.set_location(self.location+s)

        if s != 0:
            d = 31
            while d >= 0:
                self.pic.place(y=32*(19-self.location)+82+d*s)
                d -= 1
                sleep(MOVE_TIME)
        else:
            s = -self.state
            self.set_state(-self.state)
        
        self.button[self.location]['bg'] = BUTTON_OFF_COLOR


    def send(self):                                           # 发出消息改变外部按钮状态
        if self.state == 1:
            if self.location != 19:
                mes = self.location
                MQ.put(mes)
        else:
            if self.location != 0:
                mes = self.location + 18
                MQ.put(mes)


    def door_button_callback(self, op):                       # 开关门按钮回调函数,op=1表示开门操作
        if op == 1:
            if self.door == True:
                self.door_signal = True
            else:
                if self.state == 0:
                    self.set_state(1)
                    self.insert_uplist(self.location)


    def open_door(self):                                      # 电梯开门动画
        self.door = True
        sleep(OPEN_TIME/12)
        self.pic_file['file'] = 'source/ElevatorOn1.png'
        sleep(OPEN_TIME/12)
        self.pic_file['file'] = 'source/ElevatorOn2.png'
        sleep(OPEN_TIME/12)
        self.pic_file['file'] = 'source/ElevatorOn3.png'
        sleep(OPEN_TIME/2)
        self.pic_file['file'] = 'source/ElevatorOn2.png'
        sleep(OPEN_TIME/12)                                   # 检测是否有开门请求
        if self.door_signal == True:
            self.door_signal = False
            self.open_door()
            return
        self.pic_file['file'] = 'source/ElevatorOn1.png'
        sleep(OPEN_TIME/12)
        if self.door_signal == True:
            self.door_signal = False
            self.open_door()
            return
        self.pic_file['file'] = 'source/ElevatorOff.png'
        sleep(OPEN_TIME/12)
        self.door = False
        self.door_signal = False
        return
                
                