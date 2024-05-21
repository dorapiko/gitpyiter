import git
import datetime, time
import json
import os 

i = 0

while True:
    i += 1

    if not os.path.exists(f"pythondata/data{i}.json"):
        break


    with open(f'pythondata/data{i}.json') as f:
        data = json.load(f)

    for node in data["data"]["search"]["nodes"] :

        user_name = node["owner"]["login"]
        project_name = node["name"]

        print(user_name)
        print(project_name)

        if not os.path.exists(project_name):
            repo = git.Repo.clone_from(f"https://github.com/{user_name}/{project_name}.git",project_name)

        else :
            repo = git.Repo(project_name)
            data = []

            for item in repo.iter_commits(max_count = 1000):
                if item.parents:
                    dt = datetime.datetime.fromtimestamp(item.authored_date).strftime("%Y/%m/%d, %H:%M:%S")

                    for diff in item.diff(item.hexsha+'~1'):
                        s = diff.a_path
                        if s.endswith('.py'):
                            if diff.change_type == 'D':
                                data.append({'commit_name': diff.a_path, 'date': dt, 'change_type': diff.change_type, 'hash': item.hexsha})
                                #print(diff.a_path)
                                #print(dt)
                                #print(diff.change_type)

            json_data = json.dumps(data)
            #print(json_data)
            #print(list(repo.iter_commits('main',max_count=10)))    
            with open(f'difftype/{project_name}.json', 'w') as f:
                json.dump(data, f,indent=2)
