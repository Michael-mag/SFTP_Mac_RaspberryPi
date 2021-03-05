# SFTP_Mac_RaspberryPi
 - Implementation of Secure File Transfer Protocol to transfer files between my laptop and a headless Raspberry Pi.
 - In an effort to determine the most effective way to simultaneously and accurately gather sensor data from several 
      slave micro-controllers synced to the master Raspberry pi, I had to analyse how effective the methods at hand were.
      After testing different methods, and collecting perfomance data on the raspbery pi in a CSV file, I had to use pandas 
      and matplotlib to perfom the data analysis, but this was not possible while using a headless raspberry pi as it could 
      not detect a display.
- The immediate solution would have been to get an extra monitor and HDMI cable to attach to the raspbery pi but since I was 
    already using SSH to remotely access the raspbery pi using my mac, getting an extra display would not be cost effective.
- To get the files from the raspberry pi to the macbook, where I would perfom the data analysis since i already had Pandas
    and matplotlib installed there, I had to write a short script that would circumvent the limitations of sftp file transfer
    on the commandline, and tweak it to my taste and needs.
