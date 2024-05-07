import git
import datetime, time
import json

#repo = git.Repo.clone_from("https://github.com/R3nzTheCodeGOD/R3nzSkin.git","skin-changer")
repo = git.Repo("skin-changer")
data = []
for item in repo.iter_commits('main',max_count=10):
    dt = datetime.datetime.fromtimestamp(item.authored_date).strftime("%Y/%m/%d,")
    #print("%s %s %s "  %(item.hexsha, item.author, dt))
    for diff in item.diff(item.hexsha+'~1'):
        if diff.change_type == 'A':
            data.append({'commit_name': diff.a_path, 'date': dt, 'change_type': diff.change_type})
            #print(diff.a_path)
            #print(dt)
            #print(diff.change_type)
json_data = json.dumps(data)
print(json_data)
#print(list(repo.iter_commits('main',max_count=10)))    
with open('data.json', 'w') as f:
    json.dump(data, f,indent=2)
