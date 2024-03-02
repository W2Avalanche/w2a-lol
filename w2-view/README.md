# W2-View Module

Forked and based on [lol-pick-ban-ui](https://github.com/RCVolus/lol-pick-ban-ui/) european layout from [RCVolus](https://github.com/RCVolus).

Created by a React App and modified from the original version in order to allow additional data, such team logos and render the team logo depending the current active team.

## Requirements

1. NodeJs (v18.17.1)
2. Yarn (1.22.19)

## How to run it

1. Install all requirements via npm `npm install`
2. Run the React App by `yarn start`

## Usage

By default, the webpage will try to connect to `ws://localhost:8000/view` Websocket (a flexible integration based on configuration or env variables is required).

It will be waiting for JSON messages with the following information:

```json
{
   "eventType":"newState",
   "state":{
      "config":{
            "logo": "https://api.leamateur.pro/file/team/uA3r9oN56MvwsmaPouYk.png",
            "scoreEnabled":false,
            "spellsEnabled":true,
            "coachesEnabled":false,
            "blueTeam":{
               "name":"Team Blue",
               "logo": "https://api.leamateur.pro/file/team/zBmEp2rSNU0Ur7vbRyQO.png",
               "score":0,
               "coach":"TEST",
               "color":"rgb(0,151,196)"
            },
            "redTeam":{
               "name":"Team Red",
               "score":0,
               "coach":"TEST",
               "color":"rgb(222,40,70)",
               "logo": "https://api.leamateur.pro/file/team/FBAvKC94jI57OfKQPm4D.png"
            },
            "patch":""
         
      },
      "blueTeam":{
         "picks":[
            {"champion":{"name":"AATROX", "idName":"aatrox", "loadingImg":"https://ddragon.leagueoflegends.com/cdn/img/champion/centered/Aatrox_0.jpg"}, "isActive": false, "displayName":"Pepe"}
         ],
         "bans":[
            
         ],
         "isActive":false
      },
      "redTeam":{
         "picks":[
         ],
         "bans":[
         ],
         "isActive":false
      },
      "timer": 7,
      "champSelectActive":true,
      "leagueConnected": true
   }
}
```
