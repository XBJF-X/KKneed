import os
import re

from requests import get


def get_html_url(text):
    var=text
    prefix = 'og:url" content="'
    suffix = '"og:width" content='
    start_index = 0
    end_index = -1
    try:
        start_index = var.find(f'{prefix}')+len(prefix)

    except Exception as e:
        pass
    try:
        end_index = var.find(f'{suffix}') - len('"><meta data-vue-meta="true" property=')

    except Exception as e:
        pass
    if start_index != 0 and end_index != -1:
        url = var[start_index:end_index]
    return url

def get_video_and_audio_url(url):
    pid=os.getpid()
    urls = []
    headers = {
        "referer": "https://www.bilibili.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "cookie": "buvid3=CE9632C5-615A-3ED7-F906-A6502B0CB04B28461infoc; b_nut=1702821628; _uuid=10CBC184E-449C-D8C4-6F14-4AD105D87F371028195infoc; buvid4=36200BDA-DEA8-2EB2-6AA8-3F4992EE066C29435-023121714-; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(u)YJm~l~m~0J'u~|JkR)~~~; buvid_fp_plain=undefined; FEED_LIVE_VERSION=V8; CURRENT_QUALITY=80; LIVE_BUVID=AUTO8317122246182757; PVID=1; SESSDATA=e002a3f3%2C1734068875%2C59b9f%2A62CjCDCTxs-u94Qodd7F5E2OEsNTD0GzYWh8h_Rb7qSKnEusNrhYVq548khvZ5HWHXWbESVmN6TGE0dDFVQkRNTFAySXY5TU9CaHhudldQamJIU1pOZmViQndMVmFzdU9YdTlYUWNJaGVKV2tRcng2WlNTdW41RGVwWFpzUVpPNExTalR6a2RYdzF3IIEC; bili_jct=3c02ead6019a85564bd61306f637835b; DedeUserID=398448576; DedeUserID__ckMd5=7adb385c03bcbf3b; is-2022-channel=1; fingerprint=de25f028dd8ebfe649ae25ba2bacd3b5; bp_t_offset_398448576=961786088316207104; home_feed_column=4; browser_resolution=1309-557; sid=842auvil; buvid_fp=bff5d92132552fb8895541092f5ba222; bsource=search_bing; b_lsid=7C10DC83D_1912B544978; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMyNjg2NDYsImlhdCI6MTcyMzAwOTM4NiwicGx0IjotMX0.A42yGodZzrRXExTDnGzJksJ2XTYAL4msjY1_Y4doVkM; bili_ticket_expires=1723268586"
    }

    response = get(url, headers=headers)
    with open(f"Log/{pid}/response.txt","w",encoding="utf-8") as res:
        res.write(response.text)

    var=response.text
    pattern = r'"baseUrl":".*?"base_url":"'
    matches=re.findall(pattern,var)
    for match in matches:
        match=match[11:-14]
        urls.append(match)
    pattern = r'<title data-vue-meta="true">.*?</title>'
    matches = re.findall(pattern, var)
    with open(f"Log/{pid}/title.txt","w",encoding="utf-8") as t:
        match=matches[0]
        match = match[28:-8]
        t.write(match)
    return urls



def get_download_address():
    pid = os.getpid()
    with open(f"Log/{pid}/src.txt", "r",encoding="utf-8") as src:
        src1=src.read()

    with open(src1,"r",encoding="utf-8") as html:
        text1=html.read()
        html_url=get_html_url(text1)
        urls=get_video_and_audio_url(html_url)

        with open(f"Log/{pid}/批量下载链接.txt", 'w', encoding="utf-8") as f:
            f.write(f"{urls[0]}\n")
            f.write(f"{urls[-3]}\n")

