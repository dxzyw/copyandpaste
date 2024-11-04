import os
import httpx
import re
import urllib.parse

def fetch_ci_time(file_path):
    url = f"https://api.github.com/repos/dxzyw/copyandpaste/commits?path={file_path}&page=1&per_page=1"
    response = httpx.get(url)
    ci_time = response.json()[0]["commit"]["committer"]["date"].split("T")[0]
    print(ci_time)
    return ci_time

if __name__ == "__main__":
    with open('README.md', 'w') as readme_file, open('RECENT.md', 'w') as recent_file:
        readme_file.write("# 开源周刊\n\n> 记录工程师 的不枯燥生活，欢迎订阅，也欢迎 [推荐](https://github.com/dxzyw/copyandpaste/discussions/22) 你的好东西，Fork 自用可见 [开发文档](https://github.com/dxzyw/weekly/blob/main/Deploy.md)，期待你玩得开心~\n\n")

        for root, dirs, filenames in os.walk('./src/pages/posts'):
            filenames = sorted(filenames, key=lambda x: float(re.findall(r"(\d+)", x)[0]), reverse=False)
            print(filenames)

        for index, name in enumerate(filenames):
            if name.endswith('.md'):
                file_path = urllib.parse.quote(name)
                old_title = name.split('.md')[0]
                url = f'https://copyandpaste.herotops.xyz/posts/{old_title}'
                title = f'{old_title.split(" ")[0]}'
                readme_md = f'* [{title}]({url})\n'
                num = 0

                if index < 5:
                    modified = fetch_ci_time(f'/src/pages/posts/{file_path}')
                    recent_md = f'* [{title}]({url}) - {modified}\n'
                    print (recent_md)
                    recent_file.write(recent_md)

                readme_file.write(readme_md)
