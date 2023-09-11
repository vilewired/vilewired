import requests
import json 
import os 


TOKEN = os.environ['TKN']
GUILD = '902669786763395163'
USER_ID = '1144700316592394371'
r = requests.get(url=f'https://discord.com/api/v9/users/{USER_ID}/profile?with_mutual_guilds=true&with_mutual_friends_count=false&guild_id={GUILD}',headers={'Authorization':TOKEN,'Content-Type':'application/json'})

r = r.json()
with open('data.json', 'w') as f:
    json.dump(r, f, indent=4)
print(r)


if r['premium_type'] == 2:
    profile = {
    'username' : r['guild_member']['user']['username'],
    'globalname' : r['guild_member']['user']['global_name'],
    'avatar' : r['guild_member']['avatar'] if r['guild_member']['avatar'] is not None else r['user']['avatar'],
    'banner' : r['guild_member']['banner'] if r['guild_member']['banner'] is not None else r['user']['banner'],
    'bio' : r['guild_member']['bio'] if r['guild_member']['bio'] != '' else r['user']['bio'],
    'theme_colors' : r['user_profile']['theme_colors'],
    'pronouns' : r['guild_member_profile']['pronouns'],
    'badges' : r['badges'],
    'nitroage' : r['premium_since'],
    'nitrotype' : r['premium_type']
    }

else:
    profile = {
    'username' : r['guild_member']['user']['username'],
    'globalname' : r['guild_member']['user']['global_name'],
    'avatar' : r['guild_member']['avatar'],
    'banner' : r['guild_member']['banner'] if r['guild_member']['banner'] is not None else r['user']['banner'],
    'bio' : r['guild_member']['bio'] if r['guild_member']['bio'] != '' else r['user']['bio'],
    'pronouns' : r['guild_member_profile']['pronouns'],
    'badges' : r['badges'],
    'nitroage' : r['premium_since'],
    'nitrotype' : r['premium_type']
    }

if profile['nitrotype'] == 2:
    profile['banner'] = f'https://cdn.discordapp.com/banners/{USER_ID}/{profile["banner"]}.gif?size=480'
    profile['avatar'] = f'https://cdn.discordapp.com/avatars/{USER_ID}/{profile["avatar"]}.gif?size=128'
    for i, badge in enumerate(profile['badges']):
        profile['badges'][i] = f'https://cdn.discordapp.com/badge-icons/{badge["icon"]}.png'

    for i, color in enumerate(profile['theme_colors']):
        profile['theme_colors'][i] = '#' + hex(color)[2:]

else:
    for i in profile['badges']:
        i = f'https://cdn.discordapp.com/badge-icons/{i["icon"]}.png'

badge_html = []
for i in profile['badges']:
    badge_html.append(f"""<img src="{i}" style="
    width: auto;
    height: 25px;
    position: relative;
    top: -45%;
    left: 40%;
    transform: translate(0%, -50%);
    margin-right: 7px;
" />""")
    
badge_html = ''.join(badge_html)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml" width="410px" height="280">
    <foreignObject x="0" y="0" width="410" height="280">
      <div style="
            position: absolute;
            inset: 0;
            top: 100px;
            height: 180px;
            width: 410px;
            margin: 0;
            background-image: linear-gradient(180deg, {profile['theme_colors'][0]}, {profile['theme_colors'][1]});
        "></div>
        <div xmlns="http://www.w3.org/1999/xhtml" style="
            position: absolute;
            width: 400px;
            height: 200px;
            inset: 0;
            color: #000;
            font-family: 'Century Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
            display: flex;
            flex-direction: column;
            padding: 5px;
            border-radius: 10px;
        ">
            
            <img src="https://cdn.discordapp.com/banners/1144700316592394371/a_9414f176c07469c94416ad41de365e0d.gif?size=480"
            style="
                position: absolute;
                top: 0;
                left: 0;
                width: 410px;
                height: 100px;
                object-fit: cover;
            "/>

            <div style="
                position: absolute;
                top: 60px; 
                width: 410px;
                height: 240px;
                inset: 0;
                display: flex;
                flex-direction: column;
                padding-top: 50px;
                border-bottom: solid 0.5px hsl(0, 0%, 0%, 10%);
                border-radius: 0 0 10px 10px;
            ">

            <div style="
                    display: flex;
                    flex-direction: row;
                    height: 80px;
                    width: 80px;
                    position: relative;
                    top: -40px;
                ">
                
                    <img src="https://cdn.discordapp.com/avatars/1144700316592394371/a_fec7ba2dbef3b5db55d044a8c4c4dab1.gif?size=128"
                    style="
                        border: solid 3px {profile['theme_colors'][1]};
                        border-radius: 50%;
                        width: 80px;
                        height: 80px;
                        position: relative;
                        top: 100%;
                        left: 60%;
                        transform: translate(-50%, -50%);
                    "/>
                </div>
                <div style="
                    height: 800px;
                    width: 260px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="
                        display: flex;
                        flex-direction: row;
                        height: 60px;
                    ">
                        <h2 style="
                            font-size: 1.25rem;
                            margin: 0 12px 0 8px;
                            white-space: nowrap;
                        ">
                            {profile['username']}
                        </h2>
                        {badge_html}
                    </div>
                </div>
                <h1 style="
                           text-align: left;
                            font-size: 1rem;
                            margin: 0 0 0 8px;
                             
                        ">
                    {profile['bio']}
                        </h1>
            </div>
        </div>
    </foreignObject>
</svg>
"""

with open('output.html', 'w') as f:
    f.write(svg)
