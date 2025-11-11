Thank you for visiting the repo page of 'Project OLED"'!
This is a terminal-ui action-puzzle python mini-game presented proudly by me and my dearest teammates. 
Made as a group project submission for a programming course that I took (ENGG1330, fyi) BUT the game itself is very playable and complete (and quite fun if you ask me).

(Screenshots)
<img width="1296" height="658" alt="image" src="https://github.com/user-attachments/assets/a2b167b6-36c1-462b-b096-c043e0a05bb2" />
<img width="1290" height="661" alt="image" src="https://github.com/user-attachments/assets/199bf90d-d2bc-4f9e-9a5c-afc65497d506" />
<img width="1300" height="663" alt="image" src="https://github.com/user-attachments/assets/0b30ee27-29df-43ca-a303-d1df574eb82b" />
<img width="1303" height="657" alt="image" src="https://github.com/user-attachments/assets/5bd7ec1e-3ca5-4ae0-bb4a-a450effed280" />


#######################################################
HOW TO LAUNCH THIS GAME:
1. Unzip all files (preferably into a dedicated folder)
2. Click and run "main.py"
*There should only be a single executable. 
**Yup. I learned how to make my own modules just to make this a clean-enough presentation for you. 

That's it. You're set.
Remember to size the terminal window large enough. 

Also remember to play the tutorial (under the 'Play Project OLED"' sub-menu).

Have fun with the game. 
P.S. I think I've amounted 40 hours of total playtime already at this point. 

Also you can navigate the main menu w/ "WASD+C+X". Arrow keys & Enter are also supported.


#######################################################
Extra: How to set up your own "oled_connectivity" module

If your distribution of the game only comes with a connectivity template (named "oled_connectivity.data.template"), you MIGHT want to be able to set up your own online scoreboard your family and friends to mess with.

Now, if that's you, then your step one is to double click and open the template in your text editor of choice. 

You should now see three fields:

1. ['CSV_URL']
Create a Google Form with a single short-answer field called “scores”.

The Form will auto-create a linked Google Sheet (“Responses”).

In the Sheet: File → Share → Publish to the web → Entire Sheet → CSV.

Copy the CSV publish URL; it looks like:

https://docs.google.com/spreadsheets/d/.../pub?output=csv

Paste it into the 'CSV_URL' field. 

2. ['FORM_URL']
In the Form editor: Preview (eye icon), open your browser’s dev tools, submit once, then in the Network tab find the formResponse request. 

Save its URL; it looks like:

https://docs.google.com/forms/d/e/<FORM_ID>/formResponse

Paste it into the 'FORM_URL' field.

['FIELD_NAME']
Also copy the input name for your field; it will be something like:
entry.123456789

Paste again into the 'FIELD_NAME' field. 

That’s it. 

Your file should now look somewhat like this:

{'CSV_URL': 'https://docs.google.com/spreadsheets/d/e/.../pub?output=csv', 'FORM_URL': "https://docs.google.com/forms/u/0/d/e/.../formResponse", 'FIELD_NAME': 'entry.xxxxxxxxxx'}

Remove the ".template" suffix, and place it back into the home directory of the game (same folder as "main.py").

You should now be able to switch on the "Enable Connectivity" toggle in the settings page. 


#######################################################
P.P.S.

Easiest ways to find the Google Forms field name (entry.xxxxxxxxxx):

Open your form’s Preview (eye icon). You should be at a URL ending in /viewform.

Right-click → Inspect the single text box you created (label “payload”, etc.).

In the HTML, look for the <input> element and read its name attribute.
It will look like name="entry.xxxxxxxxxx".
That whole string is your FIELD_NAME.
