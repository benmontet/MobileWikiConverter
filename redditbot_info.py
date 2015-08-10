import requests, requests.auth, praw

r = praw.Reddit('Wikipedia Mobile to Desktop Link Converter v0.1 (by /u/GoCubs10)')

def redditbotdata():
  return 'wabBmX_ZEU_p6A', 'YpHT_mhiSSd_4e0x_r2m5ZYfu_4', 'https://github.com/benmontet'

def get_token():
    client_id, client_secret, redirect_uri = redditbotdata()
    
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "password", "username": "MobileWikiConverter", "password": "ieOPquuj23"}
    headers = {"User-Agent": "Wikipedia Mobile to Desktop Link Converter v0.1 (by /u/GoCubs10)"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    
    access_token = response.json()['access_token']
    headers = {"Authorization": "bearer" + access_token, "User-Agent": "Wikipedia Mobile to Desktop Link Converter v0.1 (by /u/GoCubs10)"}

    r.set_oauth_app_info(client_id, client_secret, redirect_uri)    
    scopes = ['identity', 'edit', 'submit', 'read', 'save']
    r.set_access_credentials(set(scopes), access_token, refresh_token=None, update_user=True)
    return r.get_me(), access_token