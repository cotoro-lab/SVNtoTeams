import subprocess
import json
import pymsteams

from OutPutLog import log

# Json情報取得
def getJsonInfo():
	# json_open = open('C:\\Users\\s.uto\\wk\\src\\noproject\\SVNtoTeams\\setting.json','r',encoding="utf-8_sig")
	json_open = open('setting.json','r',encoding="utf-8_sig")
	sj = json.load(json_open)
	return sj

# Json情報更新（最新RevNo）
def updateJsonInfo(update_json):
	# with open('C:\\Users\\s.uto\\wk\\src\\noproject\\SVNtoTeams\\setting.json', 'w',encoding='utf_8_sig') as n:
	with open('setting.json', 'w',encoding='utf_8_sig') as n:
		json.dump(update_json, n,indent=4, ensure_ascii=False)

# RevNoのチェック
def checkSVNRevNo(url,RevNo):
	commit_message = getSVNLog(url,1)
	cmsplit = commit_message.split('|',1)
	revNo_cm = cmsplit[0]
	revNo_cm = revNo_cm.replace('r','')
	# print(url)
	# print(revNo_cm)
	rtn = int(revNo_cm.strip()) - int(RevNo)
	return rtn

# SVNLogの取得
def getSVNLog(url, back):
	cmd = f'svn log --limit {back} {url}'
	res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

	commit_message = res[0].decode("shift_jisx0213")
	commit_message = commit_message.replace('------------------------------------------------------------------------', '')
	return commit_message

# SVNコミットメッセージの取得
def getSVNCommitMessage(url, revNo):
	cmd = f'svn log -r {revNo} {url}'
	res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

	commit_message = res[0].decode("shift_jisx0213")
	commit_message = commit_message.replace('------------------------------------------------------------------------', '')
	# print(commit_message)
	return commit_message

# Teamsメッセージ送信
def sendToTeams(pj_json, commit_message):
	pj_name = pj_json['name']
	pj_url = pj_json['svnurl']
	webhook_url = pj_json['teamswebhookurl']
	message = commit_message.replace('\r\n', '</br>')
	# print(message)
	teams_obj = pymsteams.connectorcard(webhook_url)
	teams_obj.title(f'コミット通知　【{pj_name}】')
	teams_obj.text(f'{pj_url}</br>{message}')
	teams_obj.send()

# Main()
def main():
	try:
		sj = getJsonInfo()
	
		for v in sj.values():
			tagVal = v['tag']
			lastRevNo = v['lastRevNo']
			RevBack = checkSVNRevNo(v['svnurl'],lastRevNo)
	
			if RevBack > 0:
				i = 1
				while i <= RevBack:
					message = getSVNCommitMessage(v['svnurl'],int(lastRevNo) + i)
					sendToTeams(v, message)
					i += 1
				sj[tagVal]['lastRevNo'] = int(lastRevNo) + RevBack
		
		updateJsonInfo(sj)
	except Exception as e:
		log(e)



if __name__ == '__main__':
	main()
