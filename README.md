# edhrec_json_to_txt
This is a Python program to take JSON card lists output from EDHRec.com for a given commander and convert the card lists to txt files that can be used with services like Moxfield, MPCFill and more. There is an executable you can easily run in the dist folder so you don't even need to install Python
## How to use
1. First you will need a JSON (JavaScript Object Notation) card list file for your commander from EDHRec. You get this by going to this URL: https://json.edhrec.com/pages/commanders/<YOUR COMMANDER NAME HERE\>.json
2. Now just run the edhrec_json_to_txt program. It will prompt you to select the JSON file then selec the folder you want to save the card lists to

That's it! Now you will have separate card lists txt files for each of the lists, as well as one big list of all cards called Flat Cardlist 

# "I don't want to deal with Python!"
If don't want to deal with installing Python, just click the green <> Code button --> Download ZIP, then unzip the .zip file, go into dist, and just run edhrec_json_to_txt.exe
