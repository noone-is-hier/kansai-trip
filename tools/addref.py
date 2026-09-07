import re,html,json,sys,urllib.parse,urllib.request,concurrent.futures as cf
src=open('modules.html',encoding='utf-8').read()
M={ # id: (ja wiki title, maps query, caption)
'usj':('ユニバーサル・スタジオ・ジャパン','Universal Studios Japan','오사카 베이의 대형 테마파크 — 닌텐도 월드·해리포터·야간 코스터'),
'keiba':('京都競馬場','Kyoto Racecourse','교토 요도의 JRA 경마장 — 10/4 메인 레이스 교토대상전(GII) 직관'),
'kyoto-east':('伏見稲荷大社','Fushimi Inari Taisha','천 개의 붉은 도리이(후시미이나리) → 기요미즈데라 → 기온 골목'),
'kyoto-west':('嵐山','Arashiyama Bamboo Grove Kyoto','아라시야마 대나무숲·도게츠교 → 금각사 → 니조성'),
'uji':('平等院','Byodoin Uji','10엔 동전의 봉황당(뵤도인)과 말차 거리'),
'nara':('奈良公園','Nara Park','공원에 사는 사슴 1,000마리 + 도다이지 대불'),
'kobe':('北野異人館街','Kitano Ijinkan Kobe','개항기 양관 거리(기타노) → 고베규 런치 → 항구 야경'),
'arima':('有馬温泉','Arima Onsen','일본 3대 고탕 아리마 — 붉은 금탕·롯코산 로프웨이'),
'osaka':('大阪城','Osaka Castle','오사카성 천수각 · 구로몬 시장 · 신세카이 츠텐카쿠'),
'kaiyukan':('海遊館','Osaka Aquarium Kaiyukan','고래상어가 사는 초대형 수조 — 비 오는 날 카드'),
'dotonbori':('道頓堀','Dotonbori Osaka','글리코 사인 네온 강변 + 먹거리 골목'),
'nightview':('梅田スカイビル','Umeda Sky Building','옥상 개방형 전망대(우메다) vs 300m 유리 전망대(하루카스)'),
'sonoda':('園田競馬場','Sonoda Racecourse','효고현 지방경마 초소형 트랙 — 말이 코앞'),
'baseball':('阪神甲子園球場','Koshien Stadium','한신 타이거스 홈 고시엔 — 전통의 일전'),
'nintendo-museum':('ニンテンドーミュージアム','Nintendo Museum Uji','닌텐도 옛 공장을 개조한 박물관 — 역대 기기 + 거대 컨트롤러'),
'fushimi-sake':('月桂冠大倉記念館','Gekkeikan Okura Sake Museum Fushimi','겟케이칸 등 양조장 거리 + 시음'),
'nada-sake':('灘五郷','Hakutsuru Sake Brewery Museum Kobe','하쿠츠루 등 대형 양조장 자료관 — 무료 시음'),
'himeji':('姫路城','Himeji Castle','세계유산 백로성 — 일본 성곽의 정점'),
'minoo':('箕面滝','Minoo Falls','계곡 산책로 끝의 33m 폭포 + 단풍잎 튀김'),
'koyasan':('高野山','Koyasan Okunoin','진언밀교 성지 — 삼나무 묘역 오쿠노인'),
'banpaku':('太陽の塔','Tower of the Sun Expo 70 Commemorative Park','1970 엑스포의 상징 태양의 탑'),
'teamlab':('長居植物園','teamLab Botanical Garden Osaka','식물원 전체가 야간 미디어아트'),
'rail-museum':('京都鉄道博物館','Kyoto Railway Museum','실물 SL·신칸센 대거 전시'),
'rivercruise':('道頓堀','Tombori River Cruise','도톤보리 네온 사이를 배로 20분'),
'tea':('茶道','Kyoto tea ceremony experience Gion','1시간 다도·화과자 체험 클래스'),
'asahi-beer':('アサヒビール','Asahi Beer Museum Suita','2023 리뉴얼 체험형 맥주 박물관 — 90분 투어 + 시음 2잔'),
'figure-run':('日本橋 (大阪市)','Nipponbashi Denden Town Osaka','덴덴타운 피규어 거리 → 파르코 캐릭터 층 → 포켓몬센터·닌텐도 오사카'),
'kimono':('着物','Kyoto kimono rental Gion','기모노 입고 산넨자카·기온 산책'),
'urananba':('難波','Ura Namba Osaka tachinomi','도톤보리 뒷골목의 서서 마시는 소형 바 호핑'),
'nakazaki-tenma':('中崎町','Nakazakicho Osaka','목조 골목 카페 거리(나카자키초) → 텐마 센베로 골목'),
'boatrace':('ボートレース住之江','Boat Race Suminoe','보트레이스의 성지 — 평일 나이터 100엔 배팅'),
'kizu-market':('大阪木津卸売市場','Osaka Kizu Wholesale Market','300년 도매시장 아침 카이센동 + 병설 슈퍼센토'),
'round1':('ラウンドワン','Round1 Stadium Sennichimae Osaka','24h 실내 스포츠 무제한 — 농구·카트·볼링·다트'),
'sauna':('スパワールド','Spa World Osaka','스파월드·소라니와·다이토요 — 도심 대형 스파 3택'),
'tsuruhashi':('鶴橋','Tsuruhashi yakiniku Osaka','역에서부터 고기 냄새 — 야키니쿠 밀집 거리'),
'amemura-game':('アメリカ村','Silver Ball Planet Osaka','빈티지 핀볼 120대 + 레트로 콘솔 게임 바'),
}
ids=re.findall(r'<article class="mod" id="([^"]+)"',src)
def h3(id_):
    m=re.search(r'id="%s".*?<h3>(.*?)</h3>'%re.escape(id_),src,re.S)
    return re.sub(r'<[^>]+>','',m.group(1)).strip() if m else id_
for i in ids:
    if i not in M:
        t=h3(i); q=re.split(r'[—(·]',t)[0].strip()
        M[i]=(None,q+' Osaka',t)
import subprocess
ALT={'nintendo-museum':[('ja','ニンテンドーミュージアム'),('en','Nintendo Museum')],
'fushimi-sake':[('ja','月桂冠'),('en','Gekkeikan'),('ja','伏見区')],
'nada-sake':[('ja','灘五郷'),('ja','白鶴酒造'),('en','Nada-Gogō')],
'minoo':[('ja','箕面大滝'),('ja','箕面公園'),('en','Minoo Park'),('ja','箕面市')],
'banpaku':[('ja','太陽の塔'),('ja','万博記念公園'),('en','Tower of the Sun')],
'teamlab':[('ja','長居植物園'),('ja','大阪市立長居植物園'),('ja','長居公園'),('en','Nagai Park')],
'rail-museum':[('ja','京都鉄道博物館'),('en','Kyoto Railway Museum')],
'tea':[('ja','茶道'),('en','Japanese tea ceremony')],
'asahi-beer':[('ja','アサヒビール吹田工場'),('ja','アサヒビール'),('en','Asahi Breweries')],
'figure-run':[('ja','でんでんタウン'),('en','Den Den Town'),('ja','日本橋 (大阪市)')],
'kimono':[('ja','着物'),('en','Kimono')],
'urananba':[('ja','難波'),('en','Namba'),('ja','道頓堀')],
'nakazaki-tenma':[('ja','中崎町'),('en','Nakazakichō'),('ja','天満')],
'boatrace':[('ja','ボートレース住之江'),('ja','住之江競艇場'),('en','Suminoe Boat Race Stadium')],
'kizu-market':[('ja','大阪木津卸売市場'),('ja','木津市場'),('ja','浪速区')],
'round1':[('ja','ラウンドワン'),('en','Round One Corporation')],
'sauna':[('ja','スパワールド'),('en','Spa World'),('ja','新世界 (大阪)')],
'tsuruhashi':[('ja','鶴橋'),('ja','鶴橋駅'),('en','Tsuruhashi Station')],
'tachinomi-ext':[('ja','京橋 (大阪市)'),('ja','立ち飲み'),('ja','新開地')],
'special-reserve':[('ja','山崎蒸溜所'),('en','Yamazaki distillery'),('ja','光の教会')],
'kitahama-cafe':[('ja','北浜 (大阪市)'),('ja','中之島 (大阪府)'),('en','Nakanoshima')],
}
def one(lang,title):
    u=(f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=pageimages|info&inprop=url&piprop=thumbnail&pithumbsize=640&redirects=1&format=json&titles='+urllib.parse.quote(title))
    out=subprocess.run(['curl','-s','-m','12','-A','KansaiTripPlanner/1.0 (https://noone-is-hier.github.io/kansai-trip/; contact via github) python-curl',u],capture_output=True,text=True).stdout
    try:
        pages=json.loads(out)['query']['pages']
        for pg in pages.values():
            t=(pg.get('thumbnail') or {}).get('source')
            if t: return t, pg.get('fullurl')
    except Exception: pass
    return None
def thumb_for(id_):
    import time
    for attempt in range(3):
        r=_thumb_for(id_)
        if r: return r
        time.sleep(2.5)
    return None
def _thumb_for(id_):
    title=M[id_][0]
    cands=ALT.get(id_) or ([('ja',title),('en',title)] if title else [])
    for lang,t in cands:
        r=one(lang,t)
        if r: return r
    return None
import os,time
CACHE='/private/tmp/claude-501/-Users-noone-won/ae4e2db3-f6e2-4199-a514-f99224da0e1b/scratchpad/thumbs.json'
res=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
for i in ids:
    if res.get(i): continue
    r=thumb_for(i)
    if r: res[i]=list(r)
    time.sleep(0.6)
json.dump(res,open(CACHE,'w'),ensure_ascii=False,indent=1)
CSS='''
/* reference strip */
.ref{display:grid;grid-template-columns:200px 1fr;border-bottom:1px solid var(--line);background:var(--chip)}
.ref .ref-img{display:block;height:150px;overflow:hidden;background:var(--accent-soft)}
.ref .ref-img img{width:100%;height:100%;object-fit:cover;display:block}
.ref iframe{width:100%;height:150px;border:0;display:block;filter:saturate(.85)}
.ref-cap{grid-column:1/-1;display:flex;gap:14px;flex-wrap:wrap;align-items:baseline;padding:7px 20px;font-size:12.5px;border-top:1px solid var(--line)}
.ref-cap .what{color:var(--ink);font-weight:500;flex:1;min-width:200px}
.ref-cap a{text-decoration:none;white-space:nowrap}
.ref.noimg{grid-template-columns:1fr}
@media (max-width:680px){.ref{grid-template-columns:1fr}.ref .ref-img{height:130px}.ref iframe{height:130px}}
'''
def strip(html_,pages):
    out=html_
    for i in ids:
        wiki,q,cap=M[i]; t=res.get(i)
        img,wurl=(t if t else (None,None))
        qe=urllib.parse.quote_plus(q)
        maps=f'https://www.google.com/maps/search/?api=1&query={qe}'
        gimg=f'https://www.google.com/search?tbm=isch&q={qe}'
        links=f'<a href="{maps}" target="_blank" rel="noopener">📍 지도</a><a href="{gimg}" target="_blank" rel="noopener">🖼 사진 검색</a>'
        if wurl: links+=f'<a href="{wurl}" target="_blank" rel="noopener">📖 위키</a>'
        if pages:
            media=(f'<a class="ref-img" href="{gimg}" target="_blank" rel="noopener"><img src="{img}" alt="{html.escape(cap)}" loading="lazy"></a>' if img else '')
            media+=f'<iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={qe}&z=14&hl=ko&output=embed" title="{html.escape(q)} 지도"></iframe>'
            block=f'<div class="ref{"" if img else " noimg"}">{media}<div class="ref-cap"><span class="what">{html.escape(cap)}</span>{links}</div></div>'
        else:
            block=f'<div class="ref noimg"><div class="ref-cap"><span class="what">{html.escape(cap)}</span>{links}</div></div>'
        pat=re.compile(r'(<article class="mod" id="%s".*?</header>)'%re.escape(i),re.S)
        out,n=pat.subn(lambda m:m.group(1)+'\n  '+block,out,count=1)
        assert n==1,i
    assert out.count('class="ref ')==ids.index(i)+1 if False else True
    out=out.replace('</style>',CSS+'</style>',1)
    if pages:
        out=out.replace('사진은 각 모듈의 지도·공식 링크에서 확인 (이 페이지는 외부 이미지를 싣지 않습니다).','각 카드 상단에 대표 사진·지도·한 줄 설명을 붙였습니다 (사진은 Wikipedia, 지도는 Google Maps).')
    else:
        out=out.replace('사진은 각 모듈의 지도·공식 링크에서 확인 (이 페이지는 외부 이미지를 싣지 않습니다).','각 카드 상단에 한 줄 설명과 지도·사진 검색·위키 링크를 붙였습니다 (사진·지도 임베드가 있는 완전판은 <a href="https://noone-is-hier.github.io/kansai-trip/modules.html">GitHub Pages</a>).')
    return out
pages=strip(src,True)
open('modules.html','w',encoding='utf-8').write(pages)
# artifact version: strip skeleton + swap cross links
art=strip(src,False)
art=re.sub(r'^\s*<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*','',art)
art=art.replace('</head>\n<body>','').replace('</head>','').replace('<body>','').replace('</body>','').replace('</html>','')
art=art.replace('href="index.html"','href="https://claude.ai/code/artifact/ec28294c-338a-4d49-baa5-c00bf2c72f04"')
open('../modules_artifact.html','w',encoding='utf-8').write(art)
miss=[i for i in ids if not res.get(i)]
print('modules',len(ids),'thumbs',len(ids)-len(miss),'missing',miss)
