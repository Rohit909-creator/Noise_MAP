import requests

req = requests.get("https://api.meersens.com/environment/public/noise/current", headers={
  'apikey': 'ZHrHb6XRLtGX7peYLG3fWCHUZMDQw2K9'
}, params={
  'lat': 8.484140536292756,
  'lng': 76.94341420944959
})

print(req.content)