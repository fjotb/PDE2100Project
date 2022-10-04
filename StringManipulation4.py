import serial # pip3 install pyserial
import datetime #pip3 install datetime
import os # pip3 install os
import time #pip3 install pytime or pip3 install time
import pyrebase #pip3 install pyrebase4 or pip3 install pyrebase
ser = serial.Serial("COM7", 9600) # Establishes serial connection to COM7[USB PORT], BAUD rate = 9600 and stores serial data
# in variable ser
ser.flushInput()# clear ser
firebaseConfig ={
    "apiKey": "AIzaSyCHmAg5V0CIfGZhJZwViiA2OCXeFdn09GM",
    "authDomain": "myappfinal-7af0a.firebaseapp.com",
    "databaseURL": "https://myappfinal-7af0a-default-rtdb.firebaseio.com",
  "projectId": "myappfinal-7af0a",
  "storageBucket": "myappfinal-7af0a.appspot.com",
  "messagingSenderId": "460623334634",
  "appId": "1:460623334634:web:6873f67743df7a93be1b93",
  "measurementId": "G-VVDM998KLD"
    } #Mentioning the properties of our firebase web application including the databaseURL of our realtime database
firebase = pyrebase.initialize_app(firebaseConfig) #initializing the application to variable firebase
db = firebase.database() # storing the database application that was initialized as db
list1 = []
step =0
stepsfinal = 0
avg_temperature = 0
idle = 0
stage = 0
idlehours = []
idleminutes = []
idleseconds = []
endhours = []
endminutes= []
endseconds = []
idlenumber = 0
idletimes = []
idledurationhour = 0
idledurationminute = 0
idledurationsecond = 0
idledurationhours = []
idledurationminutes= []
idledurationseconds = []
sleepstarttimes = []
avg_sleepstarttime = 99
timetosleepnow = 1
while True:
    try:
        ser_bytes = ser.readline() #Reads a line of of the serial data and stores in variable 'ser_bytes'
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") #decodes the line into readable data
        now = datetime.datetime.now()   #Creating a timestamp and storing it in variable 'now'
        now = now.strftime("%Y-%m-%d %H:%M:%S") #Formatting the timestamp
        data = str( "'{}',{}\r\n".format(now,decoded_bytes) ) #storing the timestamp and the readable data into the variable 'data'
# Refer to Serial Output given earlier for this.
#This is a sorting method that picks out a value and assigns it to a corresponding variable
        index = data.find("MX") # For example for Magnetometer X axis values
        # We first find in the serial data 'MX' then find 'MY' and knowing
        # that the value of magnetometer X axis is between these two strings
        # we will take out the value thats between those strings and assign 
        # the value to variable 'Magneto_X'
        index2 = data.find("MY")
        index3 = data.find("MZ")
        index4 = data.find("AX")
        index5 = data.find("AY")
        index6 = data.find("AZ")
        index7 = data.find("TP") # Finds TP in the serial data
        Magneto_X = int((data[index+5:index2]))
        Magneto_Y = int((data[index2+5:index3]))
        Magneto_Z = int((data[index3+5:index4]))
        Accelero_X = int((data[index4+5:index5]))
        Accelero_Y = int((data[index5+5:index6]))
        Accelero_Z = int((data[index6+5:]))
        Temperature = int(round(float((data[index7+5:index])))) #picks the value after 'TP' and before 'MX' and rounds it up to
        #integer and stores it in variable 'Temperature'
        current_temperature = Temperature
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        #Now we will create time stamps of seconds, minutes, hours
        seconds = time.localtime()
        seconds_time = time.strftime("%S",seconds)
        usableseconds = int(seconds_time)
        #the variable 'usableseconds' holds the current second of the current time
        #for example the time is 10:25:23, if we mention secondstime = usableseconds
        # then secondstime = 23
        
        minutes = time.localtime()
        minutes_time = time.strftime("%M",minutes)
        usableminutes = int(minutes_time)
        #the variable 'usableminutes' holds the current minute of the current time
        # for example the time is 10:25:23, if we mention minutestime = usablemintues
        # then minutestime = 25

        hours = time.localtime()
        hours_time = time.strftime("%H", hours)
        usablehours = int(hours_time)
        # The variable 'usablehours' holds the current hour of the current time
        # for example the time si 10:25:23, if we mention hourstime = usablehours
        # then hourstime = 10
#Skip From here if reading code for first time
        #This is where we start calculating the average time at which the user takes rest/sleep
        # sleepstarttimes is the list where all the hour at which the user takes rest/sleep
        # so we will calculate when the user will probably take rest/sleep again by taking an average
        # on the hour that they previously took rest/sleep on
        lensleepstarttimes = len(sleepstarttimes)
        if (len(sleepstarttimes)>0):
            avg_sleepstarttime = sum(sleepstarttimes)/lensleepstarttimes
        else:
            pass
        if (avg_sleepstarttime-1)<usablehours<(avg_sleepstarttime+1):
            timetosleepnow = 1 # if the current time comes close to average rest/sleep time or schedule
            # the variable timetosleepnow will turn to 1 this indicates its time to rest/sleep
        else:
            timetosleepnow = 0 #if not timetosleepnow will be 0 indicating not time to rest/sleep
            
#Stop Skip here if reading code for first time
        if (usableseconds%20==0): #Every 20 seconds
            time.sleep(0.01)
            list1.append(Temperature) # the list list1 has the current temperature added to it
            time.sleep(0.01)
        else:pass 
        if len(list1)>0: # if list1 has an element or more
                         # we start calculating the average temperature
            avg_temperature = int(round(sum(list1)/len(list1))) 
        else:pass

        # Below is the algorithm to count steps
        # This algorithm basically detects if theres acceleration
        #and if theres acceleration it adds steps
        if (bool(70<Accelero_Z<130)== False)and (bool(-850>Accelero_Y>-1030)==False) and (bool(-950>Accelero_X>-1050)==False) and (bool(20>Accelero_Z>-10)==False):
            step = step+1
            steps = step
            stepsfinal = round(steps/3.0) # To further improve accuracy a buffer is added here
            if idle>0.30: #Skip if reading code first time # this is the code responsible for determining if person is NOT idling ANYMORE
                idle = idle -0.05 # when movements are detected, the buffer starts getting drained
            else:pass
                          #Stop Skip here if reading code for first time
        elif(idle<2): #This is where we start programming the idle.
            #The idea is to judge that the person is not moving if theres no steps detected
            # the variable 'idle' acts like a buffer in between if the person is idle and if the person is not idle
            # as the person doesnt move the buffer keeps filling up as seen later the limit of the buffer has
            # been set at 1.7, the rate at which the buffer gets added up is 0.02
            idle = idle+0.02
        else:pass
        if (idle>1.7) and (stage== 0): #We use the variable stage like a switch, its states go from 0 to 1 or 1 to 0 only
            # so if 'stage' is off or 0 and if idle>1.7 initiating IDLE
            idlenumber = idlenumber+1 #idle number is used to calculate which'th idle this is as in is it the first idle
            # or the second or the third or the nth, the use for this will be understood in later parts of the code.
            stage = 1 #setting 'stage' as 1 or on. (this is an indication that idle WAS started)
            idlefinal =1 #indicates that idle has started
            idlehour = usablehours #setting the variable 'idlehour' to the hour the idle started.
            idleminute = usableminutes #setting the variable 'idleminute' to the minute the idle started
            idlesecond = usableseconds #setting the variable 'idlesecond' to the second the idle start
            idlehours.append(idlehour)# the list idlehours stores all the hourstamps when the idles have started
            idleminutes.append(idleminute) #the list idlemintutes stores all the minute stamps when the idles have started
            idleseconds.append(idlesecond) #the list idleseconds stores all the second stamps when the idles started
            # the hour, minute, second of when the idle started is stored in the respective lists.
        else: pass
        if (idle<1.4) and (stage==1): #if idle buffer is less than 1.4 (after person is NOT idle ANYMORE)
                                      # and if idle stage was initiated before this or stage = 1 or ON
            stage = 0                 # switching back stage to 0 or OFF
            idlefinal = 0             # switching off idle status to 0
            idle = 0                  # Resetting the buffer
            endhour = usablehours     #Storing the hour that the idle ended on the endhour variable
            endminute = usableminutes #Storing the minute that the idle ended on the endminute variable
            endsecond = usableseconds #storing the second that the idle ended on the end second variable
            endhours.append(endhour)  #Appending the ending hour to the endhours list
            endminutes.append(endminute) #Appending the ending minute to the endminutes list
            endseconds.append(endsecond) #Appending the ending second to the endseconds list
            idlenumberindex = idlenumber-1
            # the hour, minute, second of when the idle ended is stored in their respective lists.

            #below is the algorithm to calculate idle durations
            # here we start to calculate how long the person has been idle for and we will add each duration to a list
            # there will be three lists, that hold how many hours person has been idle for, how many minutes, how many seconds
            # the basic idea is to subtract the start time from the end time
            # i.e. endtime - starttime, of each time bracket (hours, minutes, seconds)
            
            idledurationhour = endhours[idlenumberindex]-idlehours[idlenumberindex]
            # the endhours[idlenumberindex] points out to the end hour time of this particular idle instance
            # the idlehours[idlenumberindex] points out to the start hour time of this particular idle instance
            idledurationhours.append(idledurationhour) #Appending the difference i.e. idle duration in hours, to the
            #idle duration hours list which consists of all the idle durations in hours.
            
            if (idledurationhour>3): #detects rest state as in the person is physically resting (idle for longerperiods)
                # this can be considered as sleep also
                sleepstarttimes.append(idlehour)# if the current idle state is longer than 3 hours it is considered as
                #resting or sleeping and the hour (time) that the rest started will be appended to the
                #list named sleepstarttimes
            else:pass
                
            if (endseconds[idlenumberindex]>=idleseconds[idlenumberindex]): # our end time - start time algorithm will work
                #properly only if end time is higher than start time i.e.
                # if person starts idle at 10:01:01 and ends idle at 10:02:02 idle duration = (10-10):(02-01):(02-01) = 0:01:01
                idledurationsecond = endseconds[idlenumberindex]-idleseconds[idlenumberindex]
                idledurationseconds.append(idledurationsecond) # append idle duration to its list
            else:
                idledurationsecond = (endseconds[idlenumberindex]+60)-idleseconds[idlenumberindex]
                idledurationseconds.append(idledurationsecond)
                
            if endminutes[idlenumberindex]>=idleminutes[idlenumberindex]:
                idledurationminute = endminutes[idlenumberindex]-idleminutes[idlenumberindex]
                idledurationminutes.append(idledurationminute)
            else:
                idledurationminute = (endminutes[idlenumberindex]+60)-idleminutes[idlenumberindex]
                idledurationminutes.append(idledurationminute)
            if sum(idledurationseconds)>=60: #if total seconds get more than 60 then it will be counted as a minute and
                #appended to minute and substracted from seconds
                sumidleseconds = sum(idledurationseconds)
                q, mod = divmod(sumidleseconds, 60)
                idledurationseconds.append((q*60)*(-1))
                idledurationminutes.append(q)
            if sum(idledurationminutes)>=60: #if total seconds gets more than 60 then it will be counted as an hour and
                #appended to hours and substracted from minutes
                sumidleseconds = sum(idledurationminutes)
                q, mod = divmod(sumidleminutes, 60)
                idledurationminutes.append((q*60)*(-1))
                idledurationhours.append(q)
            else:pass
            #formatting the durations to strings
            stringidledurationhours = str(sum(idledurationhours))+"Hours"
            stringidledurationminutes = str(sum(idledurationminutes))+"Minutes"
            stringidledurationseconds = str(sum(idledurationseconds))+"Seconds"
            idletimefinalstring = stringidledurationhours + stringidledurationminutes + stringidledurationseconds
            #print(idletimefinalstring)
        else:pass
        #the compass
        # it has been calibrated by checking which physical orientation of the board points to which direction on a real compass
        if 0<Magneto_X and Magneto_X <100 and -5<Magneto_Z and Magneto_Z<25:
            direction = "EAST"
        elif 340<Magneto_X and Magneto_X<500 and -5<Magneto_Z and Magneto_Z<25 and Magneto_Y>-400 and Magneto_Y<-150:
            direction = "NORTH"
        elif 700<Magneto_X and Magneto_X<790 and -5<Magneto_Z and Magneto_Z<25:
            direction = "WEST"
        elif 160<Magneto_X and Magneto_X<300 and Magneto_Y<-700 and Magneto_Y>-1000:
            direction = "SOUTH"
        else:pass

        if (usableseconds%17==0):# Every 17 seconds the fields created earlier will be updated with the new information
            print("X")
            db.child('-MyElY-T4gZQ0J7lYaRT').update({"Steps":stepsfinal})
            time.sleep(0.05)
            db.child('-Mxy_G9CrlJE6whnGst6').update({"Direction":direction})
            time.sleep(0.05)
            db.child('-My7SPh8MCJE_6APo3Ex').update({"CurrentBody":Temperature})
            time.sleep(0.05)
            db.child('-My7SGIw2P5sGSQOcK5O').update({"AvgBody":avg_temperature})
            time.sleep(0.05)
            db.child('-MyEeN2mFNEQ5lxLkCrJ').update({"IdleTime":idletimefinalstring})
            time.sleep(0.05)
            db.child('-MyEp85kctuu6qiU7hKF').update({"timetosleepornot":timetosleepnow})
            time.sleep(0.05)
        else:pass
    except:
        print("*")
        
