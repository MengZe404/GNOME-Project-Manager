
run = True
def timer():
    start = time.time()
    while True:
        current = time.time()
        if current - start == 1800:
            Notify.init("GNOME Project Manager")
            Notify.Notification.new("You have been working for 30 minutes!", "It's time to take a break!").show()
            Notify.uninit()
            return False
        elif run == False:
            return False

thread = threading.Thread(target=timer, args=())
thread.start()