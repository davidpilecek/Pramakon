import time

lastTime = 0

while True:
    curr_time = time.time()
    if(curr_time - lastTime >=60):
        

        f = open("testfile.txt", "a")

        f.write(str(time.localtime(curr_time)))
        f.write("\n")
        f.close()
        lastTime = curr_time