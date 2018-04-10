# !streak: Win streak

A *Streamlabs Chatbot* command that print the win streak of the hoster on a txt file. The file can be imported on OBS to show the result on screen.

Example:
```
>> !streak +      // increase win by 1
>> !streak -      // descrease loss by 1
>> !streak reset  // reset count
>> !streak +5 -3  // set win to 5 and loss to 3
```

## Installation
First of all download the last version of the *WinStreak* command from [here](https://github.com/lucarin91/winstreak-streamlabs/releases).
After the download, open the *Streamlab Chatbot* program and under the script section, install the `.zip` file by clicking the import buttom.

After the installation, it is possible to configure the command using the UI interface in the script tab.

The txt file is saved with all the other StreamLabs .txt files, namely `%AppData%\Roaming\Streamlabs\Streamlabs Chatbot\Services\Twitch\Files`.

## License
MIT license
