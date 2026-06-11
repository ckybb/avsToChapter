import argparse
import re
import sys

def frameToMsec(frame):
    # フレーム単位をミリ秒に変換(29.97fps環境)
    return int(((frame * 1001 + 30000/2 )/ 3000))

class rex_check(object):
  # バリデーションのためのクラス
  def __init__(self, pattern):
    # 初期化
    self.pattern = pattern

  def __contains__(self, val):
    # マッチ処理を行う
    return re.match(self.pattern, val)

  def __iter__(self):
    # エラー時にコンソールに表示される
    return iter(("str", self.pattern))

parser = argparse.ArgumentParser(description='avs to chapter')
parser.add_argument('path', help='avsのpathを指定', choices=rex_check(r'.*\.avs'))

args = parser.parse_args()

# text = 'Trim(341,7563) ++ Trim(9362,33816) ++ Trim(35615,46793) ++ Trim(48592,48891)'

try:
    with open(args.path) as f:
        avs = f.read()
except:
    print('ファイルを読み込めませんでした')
    sys.exit()

textsplit = avs.split(' ++ ')
chapters = []

for i in textsplit:
    end, start = re.findall(r'\d+', i)
    chapters.append([int(end), int(start)])

print(chapters)

output = 'c-'

for i in chapters:
    output += str(frameToMsec(i[0]))+'dox-'+str(frameToMsec(i[1]))+'dix-'

output += 'c'
print(output)

new_file_path = args.path.replace('.ts.trim.avs', '.chapter')

print(new_file_path)

try:
    with open(new_file_path, 'w') as f:
        f.write(output)
except:
    print('ファイルを作成できませんでした')
    sys.exit()

print('done')
