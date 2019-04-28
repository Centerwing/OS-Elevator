import tkinter as tk
from time import sleep
from queue import Queue
from functools import partial

BUTTON_ON_COLOR = 'SkyBlue'
BUTTON_OFF_COLOR = 'Snow'
BUTTON_TYPE = 'groove' 
ELEVATOR_SPEED = 2
REACTION_TIME = 0.5

MQ = Queue(maxsize=20)                # 消息队列

class Elevator:
    def __init__(self, no, window):
        self.no = no                  # 电梯编号
        
        self.location = 0             # 电梯当前位置
        
        self.door = False             # 电梯门的状态

        self.picfile = tk.PhotoImage(file = 'Elevator.png')
        self.pic = tk.Label(window, image = self.picfile)   # 电梯图片
        
        self.button = []              # 电梯内部按钮
        for i in range(0,16):
            self.button.append(tk.Button(window, command = partial(self.interior_request,i),
                                         text = str(i+1), width = 3, heigh = 1, bg = BUTTON_OFF_COLOR,
                                         relief = BUTTON_TYPE))
            if i<8:
                self.button[i].place(x=130+no*150, y=400-i*30, anchor = tk.CENTER)
            else:
                self.button[i].place(x=160+no*150, y=400-(i-8)*30, anchor = tk.CENTER)

        #self.floor_text = tk.Label(window,bg = 'lightCyan', fg = 'red', width = 10, textvariable = tk.StringVar(value=str(self.location)))
        #self.floor_text.place(x=500, y=500)     

        self.state = 0                # 电梯当前工作状态(1-上行,0-静止,-1-下行)
        
        self.up_list = []             # 电梯上行的目标列表
        
        self.down_list = []           # 电梯下行的目标列表
        
        
    def insert_uplist(self, floor):                        # 插入上行列表
        if floor not in self.up_list:
            self.up_list.append(floor)
        self.up_list.sort()
        
        
    def insert_downlist(self, floor):                      # 插入下行列表
        if floor not in self.down_list:
            self.down_list.append(floor)
        self.down_list.sort()


    def interior_request(self, req_floor):                 # 处理内部请求
        if req_floor != self.location:
            self.button[req_floor]['bg'] = BUTTON_ON_COLOR

        if req_floor > self.location:
            self.insert_uplist(req_floor)
            if self.state == 0:
                self.state = 1
        elif req_floor < self.location:
            self.insert_downlist(req_floor)
            if self.state == 0:
                self.state = -1


    def exterior_request(self, req_floor, req_direction):  # 处理外部请求        
        if self.state == 0:                                # 若电梯静止则改变电梯运行状态
            if req_floor > self.location:
                self.state = 1
            elif req_floor < self.location:
                self.state = -1
        
        if req_direction == 1:
            self.insert_uplist(req_floor)
        elif req_direction == -1:
            self.insert_downlist(req_floor)
            
            
    def arrive_time(self, floor, direction):              # 计算达到时间,用于外部按钮的调度
        sta = self.state
        loc = self.location
        if sta == 0:
            return abs(floor-self.location)

        time = 0
        while True:
            if loc == floor and direction == sta:
                break
            if len(self.up_list)==0 and len(self.down_list)==0:
                time += abs(floor-self.location)
                break
            if sta == 1:
                if (self.up_list and self.up_list[-1]>self.location)or(self.down_list and self.down_list[-1]>self.location):
                    loc += 1
                    time += 1
                else:
                    sta = -sta
                    time += 1
            else:
                if (self.get_uplist and self.up_list[0]<self.location)or(self.down_list and self.down_list[0]<self.location):
                    loc -= 1
                    time -= 1
                else:
                    sta = -sta
                    time += 1
                    
        return time
                
            
    def run(self):                                            # 控制电梯运行
        while True:
            if self.door:
                self.close_door()

            if self.state == 1:
                if self.location in self.up_list:             # 将已到达的目标位置消去
                    self.up_list.remove(self.location)
                    self.open_door()                          # 开门
                if len(self.up_list)==0 and len(self.down_list)==0:
                    self.state = 0
                elif (self.up_list and self.up_list[-1]>self.location)or(self.down_list and self.down_list[-1]>self.location):
                    self.move(1)                              # 上升
                else:
                    self.move(0)                              # 转向
            elif self.state == -1:
                if self.location in self.down_list:
                    self.down_list.remove(self.location)
                    self.open_door()                          # 开门          
                if len(self.up_list)==0 and len(self.down_list)==0:
                    self.state = 0
                elif (self.up_list and self.up_list[0]<self.location)or(self.down_list and self.down_list[0]<self.location):
                    self.move(-1)                             # 下降
                else:
                    self.move(0)                              # 转向

            if self.state == 0:
                sleep(REACTION_TIME)
            else:
                sleep(ELEVATOR_SPEED)


    def move(self, s):                                        # s=0: 电梯转向
        self.location += s
        self.button[self.location]['bg'] = BUTTON_OFF_COLOR
        if s == 0:
            s = -self.state
            self.state = -self.state

        if s == 1:
            if self.location != 15:
                mes = self.location
                MQ.put(mes)
        else:
            if self.location != 0:
                mes = self.location + 14
                MQ.put(mes)

        print('No' + str(self.no))                        # 调试 
        print('arriving ' + str(self.location) + ' floor')# 调试
        print('state = ' + str(self.state))               # 调试


    def open_door(self):
        print('Open')
        self.door = True
        return
    def close_door(self):
        print('Close')
        self.door = False
        return


    def get_state (self):
        return self.state
    def get_location (self):
        return self.location
    def get_no (self):
        return self.no
    def get_uplist (self):
        print(self.up_list)
    def get_downlist (self):
        print(self.down_list)
                
                