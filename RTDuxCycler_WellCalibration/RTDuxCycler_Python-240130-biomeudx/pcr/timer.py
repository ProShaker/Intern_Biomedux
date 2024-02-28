import time
import threading

from PyQt5.QtCore import QCoreApplication, QTimer, Qt

from constants.constant import Command, State, StateOper

from hid import hid_controller as hid
import hid.tx_action as TxAction
import hid.rx_action as RxAction

from task import PCRTask

# Timer Loop time definitions
TIMER_DURATION = 100  # 100ms


class PCRTimer(QTimer):

    def __init__(self):
        super().__init__()
        self.task = PCRTask.instance()

        self.task.mainUI.frame_camctrl.init_display()

        # Must be use precise timer
        self.setTimerType(Qt.TimerType.PreciseTimer)
        self.setInterval(TIMER_DURATION)
        self.timeout.connect(self.run)

        self.cnt = 0

    def read_buffer(self):
        raw_data = hid.read()

        if raw_data:
            RxAction.set_buffer(raw_data)  # Set info
            self.task.state = RxAction.rx_buffer['State']  # Set state

            # Set current_loop
            loop = RxAction.rx_buffer["Current_Loop"]
            self.task.cur_loop = 0 if loop == 255 else self.task.cycle_num - loop

            self.task.pre_label = self.task.cur_label
            self.task.cur_label = RxAction.rx_buffer["Current_Action"]  # Set current_action
            self.task.sec_TimeLeft = RxAction.rx_buffer["Sec_TimeLeft"]
        else:  # if get rx_buffer nothing
            pass

    def send_buffer(self):
        command = self.task.command

        if command == Command.NOP:
            tx_buffer = TxAction.make_nop()

        elif command == Command.TASK_WRITE:
            tx_buffer = TxAction.make_taskWrite(self.task.protocol[self.task.action_num],
                                                self.task.preheat,
                                                self.task.action_num)
            print(f"--self.task.preheat : {self.task.preheat}")
        elif command == Command.TASK_END:
            tx_buffer = TxAction.make_taskEnd()

        elif command == Command.GO:
            tx_buffer = TxAction.make_go()

        elif command == Command.STOP:
            tx_buffer = TxAction.make_stop()
        elif command == Command.RESUME:
            tx_buffer = TxAction.make_resume()

        hid.write(tx_buffer)

    def run(self):
        # read buffer
        self.read_buffer()

        # check status
        self.task.check_status()

        # calc temperature
        self.task.calc_temp()

        # line task
        self.task.line_task()

        # calc time
        self.task.calc_time()

        # Camera shot check
        self.task.check_shot()

        # send buffer
        self.send_buffer()