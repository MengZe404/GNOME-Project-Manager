import threading
import time

def timer_function():
    hour = minute = second = 0
    while minute < 1:
        second += 1
        time.sleep(1)
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1 
        print(f"{hour:02d}:{minute:02d}:{second:02d}")


timer = threading.Thread(target=timer, args=())
timer.start()
