# phoney - a honeypot tool

This basic python script monitors a folder for unauthorized access via the command line or GUI; if detected it sends a text alert to your phone!  Note, it requires a Twilio account, set-up, and correlation to your personal device to receive texts; for information on how to get a trial Twilio account please visit https://console.twilio.com/.

##Prerequisites

You'll need a proxy Twilio number, Twilio account SID, and Twilio auth token, a cellular device and number, and creation of a folder that will serve as your honeypot folder.  The path of this folder will need to be inputted into the script where designated.

## Usage

Simply run your equivalent of >>"python phoney.py" from the command line to kick things off, and then wait!

## Operation

This script uses os, psutil, and Twilio libraries to monitor a folder you designate as a honeypot to would-be intruders or unauthorized persons; if the folder is opened via a command line or through the GUI, alerts are triggered and sent to your phone or device via the Twilio proxy number.  For potential command line access, the PPID, PID, and associated timestamp of the intruding process is sent along with the message: "Someone opened the Passwords1 folder from the command line!"; for GUI access, a timestamp and the message: "Someone opened the Passwords1 folder!".  "Passwords1" folder is the default message, but obviously can be changed to suit your needs and created folder name.

Also, please modify the wait and check times as you deem appropriate!

Thank you!

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

No license!
