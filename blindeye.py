#!/usr/bin/env python3
"""
BlindEye OSINT Tool
Developed by @tc4dy
An advanced Open Source Intelligence tool for educational and research purposes only.
This tool is designed for legal security research, penetration testing, and educational activities.
"""

import requests
import re
import json
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import threading
from datetime import datetime
import signal

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

LANG = {}
CURRENT_LANG = 'en'

global_results = {
    'accounts': [],
    'comments': [],
    'other': []
}
global_lock = threading.Lock()
stop_flag = threading.Event()

TRANSLATIONS = {
    'en': {
        'banner': 'Advanced OSINT Intelligence Tool',
        'author': 'Developed by',
        'legal': 'For Educational and Legal Research Purposes Only',
        'select_lang': 'Select Language / Dil Seçin',
        'lang_en': 'English',
        'lang_tr': 'Türkçe',
        'invalid_choice': 'Invalid choice. Defaulting to English.',
        'main_menu': 'MAIN MENU',
        'search_type': 'Select Search Type',
        'mode_1': 'Exact Match Search',
        'mode_2': 'Partial Match Search (contains)',
        'mode_3': 'RAGE MODE (Multi-target Deep Search)',
        'mode_4': 'Exit',
        'enter_choice': 'Enter your choice',
        'input_type': 'Select Input Type',
        'input_username': 'Username/Nickname',
        'input_realname': 'Real Name',
        'input_both': 'Both (Username + Real Name)',
        'enter_username': 'Enter username/nickname',
        'enter_realname': 'Enter real name',
        'enter_targets': 'Enter target names (min 3, max 12, separated by commas)',
        'invalid_targets': 'Please enter between 3 and 12 targets.',
        'searching': 'Searching',
        'found_accounts': 'FOUND ACCOUNTS',
        'found_comments': 'FOUND COMMENTS/MENTIONS',
        'found_other': 'OTHER FINDINGS',
        'platform': 'Platform',
        'url': 'URL',
        'status': 'Status',
        'comment_link': 'Comment Link',
        'type': 'Type',
        'total_found': 'Total Found',
        'accounts': 'accounts',
        'comments': 'comments/mentions',
        'search_complete': 'Search Complete',
        'save_results': 'Save results to file? (y/n)',
        'file_saved': 'Results saved to',
        'press_continue': 'Press Enter to continue...',
        'checking': 'Checking',
        'active': 'ACTIVE',
        'not_found': 'NOT FOUND',
        'error': 'ERROR',
        'timeout': 'TIMEOUT',
        'interrupted': 'Search interrupted by user (Ctrl+C)',
        'saving_progress': 'Saving current progress...',
        'search_stopped': 'Search stopped. Returning to menu...'
    },
    'tr': {
        'banner': 'Gelişmiş OSINT İstihbarat Aracı',
        'author': 'Geliştiren',
        'legal': 'Yalnızca Eğitim ve Yasal Araştırma Amaçlıdır',
        'select_lang': 'Select Language / Dil Seçin',
        'lang_en': 'English',
        'lang_tr': 'Türkçe',
        'invalid_choice': 'Geçersiz seçim. İngilizce olarak devam ediliyor.',
        'main_menu': 'ANA MENÜ',
        'search_type': 'Arama Türünü Seçin',
        'mode_1': 'Tam Eşleşme Araması',
        'mode_2': 'Kısmi Eşleşme Araması (içeren)',
        'mode_3': 'ÖFKE MODU (Çoklu Hedef Derin Arama)',
        'mode_4': 'Çıkış',
        'enter_choice': 'Seçiminizi girin',
        'input_type': 'Giriş Türünü Seçin',
        'input_username': 'Kullanıcı Adı/Takma Ad',
        'input_realname': 'Gerçek İsim',
        'input_both': 'Her İkisi (Kullanıcı Adı + Gerçek İsim)',
        'enter_username': 'Kullanıcı adı/takma ad girin',
        'enter_realname': 'Gerçek isim girin',
        'enter_targets': 'Hedef isimleri girin (min 3, max 12, virgülle ayrılmış)',
        'invalid_targets': 'Lütfen 3 ile 12 arasında hedef girin.',
        'searching': 'Aranıyor',
        'found_accounts': 'BULUNAN HESAPLAR',
        'found_comments': 'BULUNAN YORUMLAR/ETIKETLER',
        'found_other': 'DİĞER BULGULAR',
        'platform': 'Platform',
        'url': 'URL',
        'status': 'Durum',
        'comment_link': 'Yorum Bağlantısı',
        'type': 'Tür',
        'total_found': 'Toplam Bulunan',
        'accounts': 'hesap',
        'comments': 'yorum/etiket',
        'search_complete': 'Arama Tamamlandı',
        'save_results': 'Sonuçlar dosyaya kaydedilsin mi? (e/h)',
        'file_saved': 'Sonuçlar kaydedildi',
        'press_continue': 'Devam etmek için Enter\'a basın...',
        'checking': 'Kontrol ediliyor',
        'active': 'AKTİF',
        'not_found': 'BULUNAMADI',
        'error': 'HATA',
        'timeout': 'ZAMAN AŞIMI',
        'interrupted': 'Arama kullanıcı tarafından durduruldu (Ctrl+C)',
        'saving_progress': 'Mevcut ilerleme kaydediliyor...',
        'search_stopped': 'Arama durduruldu. Menüye dönülüyor...'
    }
}

PLATFORMS = [
    {"name": "Twitter/X", "url": "https://twitter.com/{}", "check": "profile"},
    {"name": "Facebook", "url": "https://www.facebook.com/{}", "check": "profile"},
    {"name": "Instagram", "url": "https://www.instagram.com/{}/", "check": "profile"},
    {"name": "TikTok", "url": "https://www.tiktok.com/@{}", "check": "profile"},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "check": "profile"},
    {"name": "Threads", "url": "https://www.threads.net/@{}", "check": "profile"},
    {"name": "Mastodon", "url": "https://mastodon.social/@{}", "check": "profile"},
    {"name": "Bluesky", "url": "https://bsky.app/profile/{}.bsky.social", "check": "profile"},
    {"name": "Tumblr", "url": "https://{}.tumblr.com", "check": "profile"},
    {"name": "VK", "url": "https://vk.com/{}", "check": "profile"},
    {"name": "OK.ru", "url": "https://ok.ru/{}", "check": "profile"},
    {"name": "Weibo", "url": "https://weibo.com/{}", "check": "profile"},
    {"name": "Douban", "url": "https://www.douban.com/people/{}/", "check": "profile"},
    {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "check": "profile"},
    {"name": "Flickr", "url": "https://www.flickr.com/people/{}/", "check": "profile"},
    {"name": "Snapchat", "url": "https://www.snapchat.com/add/{}", "check": "profile"},
    {"name": "Likee", "url": "https://likee.video/@{}", "check": "profile"},
    {"name": "Kuaishou", "url": "https://www.kuaishou.com/{}", "check": "profile"},
    {"name": "Mix", "url": "https://mix.com/{}", "check": "profile"},
    {"name": "MeWe", "url": "https://mewe.com/{}", "check": "profile"},
    {"name": "Gab", "url": "https://gab.com/{}", "check": "profile"},
    {"name": "Parler", "url": "https://parler.com/{}", "check": "profile"},
    {"name": "Truth Social", "url": "https://truthsocial.com/@{}", "check": "profile"},
    {"name": "Clubhouse", "url": "https://www.clubhouse.com/@{}", "check": "profile"},
    {"name": "Amino", "url": "https://aminoapps.com/u/{}", "check": "profile"},
    {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "check": "profile"},
    {"name": "Steam Community", "url": "https://steamcommunity.com/profiles/{}", "check": "profile"},
    {"name": "Twitch", "url": "https://www.twitch.tv/{}", "check": "profile"},
    {"name": "Kick", "url": "https://kick.com/{}", "check": "profile"},
    {"name": "YouTube", "url": "https://www.youtube.com/@{}", "check": "profile"},
    {"name": "YouTube Gaming", "url": "https://gaming.youtube.com/channel/{}", "check": "profile"},
    {"name": "Xbox Live", "url": "https://account.xbox.com/profile?gamertag={}", "check": "profile"},
    {"name": "PlayStation Network", "url": "https://my.playstation.com/profile/{}", "check": "profile"},
    {"name": "Epic Games", "url": "https://www.epicgames.com/id/{}", "check": "profile"},
    {"name": "Battle.net", "url": "https://battle.net/{}", "check": "profile"},
    {"name": "Ubisoft Connect", "url": "https://uplay.com/{}", "check": "profile"},
    {"name": "Riot Games", "url": "https://www.riotgames.com/player/{}", "check": "profile"},
    {"name": "EA", "url": "https://www.ea.com/player/{}", "check": "profile"},
    {"name": "Roblox", "url": "https://www.roblox.com/users/{}/profile", "check": "profile"},
    {"name": "Minecraft Forums", "url": "https://www.minecraftforum.net/members/{}", "check": "profile"},
    {"name": "Hypixel", "url": "https://hypixel.net/members/{}/", "check": "profile"},
    {"name": "CurseForge", "url": "https://www.curseforge.com/members/{}", "check": "profile"},
    {"name": "ModDB", "url": "https://www.moddb.com/members/{}", "check": "profile"},
    {"name": "Nexus Mods", "url": "https://www.nexusmods.com/users/{}", "check": "profile"},
    {"name": "Speedrun.com", "url": "https://www.speedrun.com/user/{}", "check": "profile"},
    {"name": "Chess.com", "url": "https://www.chess.com/member/{}", "check": "profile"},
    {"name": "Lichess", "url": "https://lichess.org/@/{}", "check": "profile"},
    {"name": "Faceit", "url": "https://www.faceit.com/en/players/{}", "check": "profile"},
    {"name": "ESEA", "url": "https://play.esea.net/users/{}", "check": "profile"},
    {"name": "OpenRec", "url": "https://www.openrec.tv/user/{}", "check": "profile"},
    {"name": "DLive", "url": "https://dlive.tv/{}", "check": "profile"},
    {"name": "Trovo", "url": "https://trovo.live/{}", "check": "profile"},
    {"name": "AfreecaTV", "url": "https://www.afreecatv.com/{}", "check": "profile"},
    {"name": "Smashcast", "url": "https://www.smashcast.tv/{}", "check": "profile"},
    {"name": "GameJolt", "url": "https://gamejolt.com/@{}", "check": "profile"},
    {"name": "GitHub", "url": "https://github.com/{}", "check": "profile"},
    {"name": "GitLab", "url": "https://gitlab.com/{}", "check": "profile"},
    {"name": "Bitbucket", "url": "https://bitbucket.org/{}/", "check": "profile"},
    {"name": "SourceForge", "url": "https://sourceforge.net/u/{}/profile/", "check": "profile"},
    {"name": "CodePen", "url": "https://codepen.io/{}", "check": "profile"},
    {"name": "JSFiddle", "url": "https://jsfiddle.net/user/{}/", "check": "profile"},
    {"name": "Replit", "url": "https://replit.com/@{}", "check": "profile"},
    {"name": "StackOverflow", "url": "https://stackoverflow.com/users/{}", "check": "profile"},
    {"name": "StackExchange", "url": "https://stackexchange.com/users/{}", "check": "profile"},
    {"name": "HackerRank", "url": "https://www.hackerrank.com/{}", "check": "profile"},
    {"name": "LeetCode", "url": "https://leetcode.com/{}/", "check": "profile"},
    {"name": "Codewars", "url": "https://www.codewars.com/users/{}", "check": "profile"},
    {"name": "Kaggle", "url": "https://www.kaggle.com/{}", "check": "profile"},
    {"name": "Docker Hub", "url": "https://hub.docker.com/u/{}", "check": "profile"},
    {"name": "NPM", "url": "https://www.npmjs.com/~{}", "check": "profile"},
    {"name": "PyPI", "url": "https://pypi.org/user/{}/", "check": "profile"},
    {"name": "RubyGems", "url": "https://rubygems.org/profiles/{}", "check": "profile"},
    {"name": "Maven", "url": "https://mvnrepository.com/artifact/{}", "check": "profile"},
    {"name": "Launchpad", "url": "https://launchpad.net/~{}", "check": "profile"},
    {"name": "Gitea", "url": "https://gitea.com/{}", "check": "profile"},
    {"name": "Phabricator", "url": "https://phabricator.wikimedia.org/p/{}/", "check": "profile"},
    {"name": "OpenHub", "url": "https://www.openhub.net/accounts/{}", "check": "profile"},
    {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org/{}", "check": "profile"},
    {"name": "Dev.to", "url": "https://dev.to/{}", "check": "profile"},
    {"name": "Hashnode", "url": "https://hashnode.com/@{}", "check": "profile"},
    {"name": "Medium", "url": "https://medium.com/@{}", "check": "profile"},
    {"name": "HackTheBox", "url": "https://www.hackthebox.com/home/users/profile/{}", "check": "profile"},
    {"name": "TryHackMe", "url": "https://tryhackme.com/p/{}", "check": "profile"},
    {"name": "Root-Me", "url": "https://www.root-me.org/{}", "check": "profile"},
    {"name": "Exploit-DB", "url": "https://www.exploit-db.com/author/{}", "check": "profile"},
    {"name": "Bugcrowd", "url": "https://bugcrowd.com/{}", "check": "profile"},
    {"name": "HackerOne", "url": "https://hackerone.com/{}", "check": "profile"},
    {"name": "OpenBugBounty", "url": "https://www.openbugbounty.org/researchers/{}/", "check": "profile"},
    {"name": "OWASP", "url": "https://owasp.org/www-community/contributors/{}", "check": "profile"},
    {"name": "PentesterLab", "url": "https://pentesterlab.com/profile/{}", "check": "profile"},
    {"name": "Codeforces", "url": "https://codeforces.com/profile/{}", "check": "profile"},
    {"name": "AtCoder", "url": "https://atcoder.jp/users/{}", "check": "profile"},
    {"name": "Spoj", "url": "https://www.spoj.com/users/{}/", "check": "profile"},
    {"name": "UVa Online Judge", "url": "https://uhunt.onlinejudge.org/id/{}", "check": "profile"},
    {"name": "Project Euler", "url": "https://projecteuler.net/profile/{}", "check": "profile"},
    {"name": "4chan", "url": "https://boards.4channel.org/{}", "check": "profile"},
    {"name": "8kun", "url": "https://8kun.top/{}", "check": "profile"},
    {"name": "Disqus", "url": "https://disqus.com/by/{}/", "check": "profile"},
    {"name": "Quora", "url": "https://www.quora.com/profile/{}", "check": "profile"},
    {"name": "GameFAQs", "url": "https://gamefaqs.gamespot.com/community/{}", "check": "profile"},
    {"name": "Neoseeker", "url": "https://www.neoseeker.com/members/{}/", "check": "profile"},
    {"name": "ResetEra", "url": "https://www.resetera.com/members/{}/", "check": "profile"},
    {"name": "SomethingAwful", "url": "https://forums.somethingawful.com/member.php?username={}", "check": "profile"},
    {"name": "Bitcointalk", "url": "https://bitcointalk.org/index.php?action=profile;u={}", "check": "profile"},
    {"name": "HackForums", "url": "https://hackforums.net/member.php?username={}", "check": "profile"},
    {"name": "BlackHatWorld", "url": "https://www.blackhatworld.com/members/{}/", "check": "profile"},
    {"name": "XDA Developers", "url": "https://forum.xda-developers.com/m/{}/", "check": "profile"},
    {"name": "LinuxQuestions", "url": "https://www.linuxquestions.org/questions/member/{}/", "check": "profile"},
    {"name": "ArchLinux Forum", "url": "https://bbs.archlinux.org/profile.php?id={}", "check": "profile"},
    {"name": "Ubuntu Forums", "url": "https://ubuntuforums.org/member.php?username={}", "check": "profile"},
    {"name": "BoardGameGeek", "url": "https://boardgamegeek.com/user/{}", "check": "profile"},
    {"name": "Binance", "url": "https://www.binance.com/en/user/{}", "check": "profile"},
    {"name": "Coinbase", "url": "https://www.coinbase.com/{}", "check": "profile"},
    {"name": "Kraken", "url": "https://www.kraken.com/u/{}", "check": "profile"},
    {"name": "Blockchain.com", "url": "https://www.blockchain.com/explorer/addresses/{}", "check": "profile"},
    {"name": "Etherscan", "url": "https://etherscan.io/address/{}", "check": "profile"},
    {"name": "BscScan", "url": "https://bscscan.com/address/{}", "check": "profile"},
    {"name": "CoinMarketCap", "url": "https://coinmarketcap.com/user/{}/", "check": "profile"},
    {"name": "CoinGecko", "url": "https://www.coingecko.com/en/users/{}", "check": "profile"},
    {"name": "TradingView", "url": "https://www.tradingview.com/u/{}/", "check": "profile"},
    {"name": "eToro", "url": "https://www.etoro.com/people/{}", "check": "profile"},
    {"name": "OpenSea", "url": "https://opensea.io/{}", "check": "profile"},
    {"name": "Rarible", "url": "https://rarible.com/{}", "check": "profile"},
    {"name": "Foundation", "url": "https://foundation.app/@{}", "check": "profile"},
    {"name": "SuperRare", "url": "https://superrare.com/{}", "check": "profile"},
    {"name": "Mirror.xyz", "url": "https://mirror.xyz/{}", "check": "profile"},
    {"name": "Behance", "url": "https://www.behance.net/{}", "check": "profile"},
    {"name": "Dribbble", "url": "https://dribbble.com/{}", "check": "profile"},
    {"name": "ArtStation", "url": "https://www.artstation.com/{}", "check": "profile"},
    {"name": "DeviantArt", "url": "https://www.deviantart.com/{}", "check": "profile"},
    {"name": "Pixiv", "url": "https://www.pixiv.net/en/users/{}", "check": "profile"},
    {"name": "Unsplash", "url": "https://unsplash.com/@{}", "check": "profile"},
    {"name": "Pexels", "url": "https://www.pexels.com/@{}", "check": "profile"},
    {"name": "500px", "url": "https://500px.com/p/{}", "check": "profile"},
    {"name": "Vimeo", "url": "https://vimeo.com/{}", "check": "profile"},
    {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "check": "profile"},
    {"name": "Bandcamp", "url": "https://{}.bandcamp.com", "check": "profile"},
    {"name": "Mixcloud", "url": "https://www.mixcloud.com/{}/", "check": "profile"},
    {"name": "Last.fm", "url": "https://www.last.fm/user/{}", "check": "profile"},
    {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "check": "profile"},
    {"name": "Sketchfab", "url": "https://sketchfab.com/{}", "check": "profile"},
    {"name": "Thingiverse", "url": "https://www.thingiverse.com/{}/designs", "check": "profile"},
    {"name": "Printables", "url": "https://www.printables.com/@{}", "check": "profile"},
    {"name": "Instructables", "url": "https://www.instructables.com/member/{}/", "check": "profile"},
    {"name": "Figma", "url": "https://www.figma.com/@{}", "check": "profile"},
    {"name": "Canva", "url": "https://www.canva.com/{}", "check": "profile"},
    {"name": "Fiverr", "url": "https://www.fiverr.com/{}", "check": "profile"},
    {"name": "Upwork", "url": "https://www.upwork.com/freelancers/~{}", "check": "profile"},
    {"name": "Freelancer", "url": "https://www.freelancer.com/u/{}", "check": "profile"},
    {"name": "Toptal", "url": "https://www.toptal.com/resume/{}", "check": "profile"},
    {"name": "Etsy", "url": "https://www.etsy.com/shop/{}", "check": "profile"},
    {"name": "eBay", "url": "https://www.ebay.com/usr/{}", "check": "profile"},
    {"name": "Gumroad", "url": "https://gumroad.com/{}", "check": "profile"},
    {"name": "Ko-fi", "url": "https://ko-fi.com/{}", "check": "profile"},
    {"name": "Patreon", "url": "https://www.patreon.com/{}", "check": "profile"},
    {"name": "BuyMeACoffee", "url": "https://www.buymeacoffee.com/{}", "check": "profile"},
    {"name": "Substack", "url": "https://{}.substack.com", "check": "profile"},
    {"name": "Itch.io", "url": "https://{}.itch.io", "check": "profile"},
    {"name": "Pastebin", "url": "https://pastebin.com/u/{}", "check": "profile"},
    {"name": "GitHub Gists", "url": "https://gist.github.com/{}", "check": "profile"},
    {"name": "Keybase", "url": "https://keybase.io/{}", "check": "profile"},
    {"name": "About.me", "url": "https://about.me/{}", "check": "profile"},
    {"name": "Linktree", "url": "https://linktr.ee/{}", "check": "profile"},
    {"name": "Carrd", "url": "https://{}.carrd.co", "check": "profile"},
    {"name": "Gravatar", "url": "https://gravatar.com/{}", "check": "profile"},
    {"name": "WordPress", "url": "https://{}.wordpress.com", "check": "profile"},
    {"name": "Blogger", "url": "https://{}.blogspot.com", "check": "profile"},
    {"name": "Wix", "url": "https://{}.wixsite.com", "check": "profile"},
    {"name": "AngelList", "url": "https://angel.co/u/{}", "check": "profile"},
    {"name": "Crunchbase", "url": "https://www.crunchbase.com/person/{}", "check": "profile"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/in/{}", "check": "profile"},
    {"name": "Glassdoor", "url": "https://www.glassdoor.com/profile/{}", "check": "profile"},
    {"name": "Indeed", "url": "https://my.indeed.com/p/{}", "check": "profile"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/user?id={}", "check": "profile"},
    {"name": "Lobsters", "url": "https://lobste.rs/u/{}", "check": "profile"},
    {"name": "Slashdot", "url": "https://slashdot.org/~{}", "check": "profile"},
    {"name": "ResearchGate", "url": "https://www.researchgate.net/profile/{}", "check": "profile"},
    {"name": "Academia.edu", "url": "https://independent.academia.edu/{}", "check": "profile"},
    {"name": "ORCID", "url": "https://orcid.org/{}", "check": "profile"},
    {"name": "Coursera", "url": "https://www.coursera.org/user/{}", "check": "profile"},
    {"name": "Udemy", "url": "https://www.udemy.com/user/{}/", "check": "profile"},
    {"name": "Skillshare", "url": "https://www.skillshare.com/user/{}", "check": "profile"},
    {"name": "Duolingo", "url": "https://www.duolingo.com/profile/{}", "check": "profile"},
    {"name": "Goodreads", "url": "https://www.goodreads.com/{}", "check": "profile"},
    {"name": "Letterboxd", "url": "https://letterboxd.com/{}/", "check": "profile"},
    {"name": "MyAnimeList", "url": "https://myanimelist.net/profile/{}", "check": "profile"},
    {"name": "AniList", "url": "https://anilist.co/user/{}/", "check": "profile"},
    {"name": "Kitsu", "url": "https://kitsu.io/users/{}", "check": "profile"},
    {"name": "Trustpilot", "url": "https://www.trustpilot.com/users/{}", "check": "profile"},
    {"name": "Yelp", "url": "https://www.yelp.com/user_details?userid={}", "check": "profile"},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/@{}", "check": "profile"},
    {"name": "IndieHackers", "url": "https://www.indiehackers.com/{}", "check": "profile"},
    {"name": "Archive.org", "url": "https://archive.org/details/@{}", "check": "profile"},
    {"name": "Plurk", "url": "https://www.plurk.com/{}", "check": "profile"},
    {"name": "Minds", "url": "https://www.minds.com/{}", "check": "profile"},
    {"name": "Diaspora", "url": "https://diasporafoundation.org/u/{}", "check": "profile"},
    {"name": "Ello", "url": "https://ello.co/{}", "check": "profile"},
    {"name": "Steemit", "url": "https://steemit.com/@{}", "check": "profile"},
    {"name": "Hive", "url": "https://peakd.com/@{}", "check": "profile"},
    {"name": "Lemmy", "url": "https://lemmy.ml/u/{}", "check": "profile"},
    {"name": "Kbin", "url": "https://kbin.social/u/{}", "check": "profile"},
    {"name": "PeerTube", "url": "https://peertube.tv/accounts/{}", "check": "profile"},
    {"name": "Pixelfed", "url": "https://pixelfed.social/{}", "check": "profile"},
    {"name": "Cohost", "url": "https://cohost.org/{}", "check": "profile"},
    {"name": "LiveJournal", "url": "https://{}.livejournal.com", "check": "profile"},
    {"name": "Dreamwidth", "url": "https://{}.dreamwidth.org", "check": "profile"},
    {"name": "Pillowfort", "url": "https://www.pillowfort.social/{}", "check": "profile"},
    {"name": "SpaceHey", "url": "https://spacehey.com/{}", "check": "profile"},
    {"name": "Odysee", "url": "https://odysee.com/@{}", "check": "profile"},
    {"name": "Rumble", "url": "https://rumble.com/user/{}", "check": "profile"},
    {"name": "Bitchute", "url": "https://www.bitchute.com/channel/{}", "check": "profile"},
    {"name": "Gettr", "url": "https://gettr.com/user/{}", "check": "profile"},
    {"name": "Guilded", "url": "https://www.guilded.gg/{}", "check": "profile"},
    {"name": "Habr", "url": "https://habr.com/ru/users/{}/", "check": "profile"},
    {"name": "DevRant", "url": "https://devrant.com/users/{}", "check": "profile"},
    {"name": "CodeProject", "url": "https://www.codeproject.com/Members/{}", "check": "profile"},
    {"name": "MetaFilter", "url": "https://www.metafilter.com/user/{}", "check": "profile"},
    {"name": "Imgur", "url": "https://imgur.com/user/{}", "check": "profile"},
    {"name": "9GAG", "url": "https://9gag.com/u/{}", "check": "profile"},
    {"name": "KnowYourMeme", "url": "https://knowyourmeme.com/users/{}", "check": "profile"},
    {"name": "Wattpad", "url": "https://www.wattpad.com/user/{}", "check": "profile"},
    {"name": "FanFiction.net", "url": "https://www.fanfiction.net/u/{}/", "check": "profile"},
    {"name": "ArchiveOfOurOwn", "url": "https://archiveofourown.org/users/{}", "check": "profile"},
    {"name": "Scribophile", "url": "https://www.scribophile.com/authors/{}/", "check": "profile"},
    {"name": "RoyalRoad", "url": "https://www.royalroad.com/profile/{}", "check": "profile"},
    {"name": "Vocal Media", "url": "https://vocal.media/authors/{}", "check": "profile"},
    {"name": "Zhihu", "url": "https://www.zhihu.com/people/{}", "check": "profile"},
    {"name": "Baidu Tieba", "url": "https://tieba.baidu.com/home/main?un={}", "check": "profile"},
    {"name": "Xiaohongshu", "url": "https://www.xiaohongshu.com/user/profile/{}", "check": "profile"},
    {"name": "Naver", "url": "https://blog.naver.com/{}", "check": "profile"},
    {"name": "Daum Cafe", "url": "https://cafe.daum.net/{}", "check": "profile"},
    {"name": "Mixi", "url": "https://mixi.jp/show_profile.pl?id={}", "check": "profile"},
    {"name": "Line VOOM", "url": "https://timeline.line.me/user/{}", "check": "profile"},
    {"name": "Blind", "url": "https://www.teamblind.com/users/{}", "check": "profile"},
    {"name": "Fishbowl", "url": "https://www.fishbowlapp.com/{}", "check": "profile"},
    {"name": "Jodel", "url": "https://jodel.com/u/{}", "check": "profile"},
    {"name": "Whisper", "url": "https://whisper.sh/{}", "check": "profile"},
    {"name": "ASKfm", "url": "https://ask.fm/{}", "check": "profile"},
    {"name": "CuriousCat", "url": "https://curiouscat.me/{}", "check": "profile"},
    {"name": "Tellonym", "url": "https://tellonym.me/{}", "check": "profile"},
    {"name": "Retrospring", "url": "https://retrospring.net/@{}", "check": "profile"},
    {"name": "Vent", "url": "https://www.vent.co/{}", "check": "profile"},
    {"name": "7Cups", "url": "https://www.7cups.com/@{}", "check": "profile"},
    {"name": "DailyMotion", "url": "https://www.dailymotion.com/{}", "check": "profile"},
    {"name": "Veoh", "url": "https://www.veoh.com/users/{}", "check": "profile"},
    {"name": "Podbean", "url": "https://www.podbean.com/{}", "check": "profile"},
    {"name": "Spreaker", "url": "https://www.spreaker.com/user/{}", "check": "profile"},
    {"name": "Castbox", "url": "https://castbox.fm/va/{}", "check": "profile"},
    {"name": "Podchaser", "url": "https://www.podchaser.com/creators/{}", "check": "profile"},
    {"name": "Audius", "url": "https://audius.co/{}", "check": "profile"},
    {"name": "RateYourMusic", "url": "https://rateyourmusic.com/~{}", "check": "profile"},
    {"name": "Discogs", "url": "https://www.discogs.com/user/{}", "check": "profile"},
    {"name": "Planet Minecraft", "url": "https://www.planetminecraft.com/member/{}/", "check": "profile"},
    {"name": "SpigotMC", "url": "https://www.spigotmc.org/members/{}/", "check": "profile"},
    {"name": "Bukkit", "url": "https://dev.bukkit.org/members/{}/projects", "check": "profile"},
    {"name": "Scratch", "url": "https://scratch.mit.edu/users/{}/", "check": "profile"},
    {"name": "VRChat", "url": "https://vrchat.com/home/user/{}", "check": "profile"},
    {"name": "RecRoom", "url": "https://rec.net/user/{}", "check": "profile"},
    {"name": "IMVU", "url": "https://www.imvu.com/next/av/{}/", "check": "profile"},
    {"name": "Second Life", "url": "https://my.secondlife.com/{}", "check": "profile"},
    {"name": "Huya", "url": "https://www.huya.com/{}", "check": "profile"},
    {"name": "Douyu", "url": "https://www.douyu.com/{}", "check": "profile"},
    {"name": "NimoTV", "url": "https://www.nimo.tv/{}", "check": "profile"},
    {"name": "YouNow", "url": "https://www.younow.com/{}", "check": "profile"},
    {"name": "Picarto", "url": "https://picarto.tv/{}", "check": "profile"},
    {"name": "Mildom", "url": "https://www.mildom.com/{}", "check": "profile"},
    {"name": "Jamendo", "url": "https://www.jamendo.com/artist/{}", "check": "profile"},
    {"name": "Resonate", "url": "https://resonate.is/artist/{}", "check": "profile"},
    {"name": "Fountain", "url": "https://www.fountain.fm/{}", "check": "profile"},
    {"name": "Ravelry", "url": "https://www.ravelry.com/people/{}", "check": "profile"},
    {"name": "Crowdcast", "url": "https://www.crowdcast.io/{}", "check": "profile"},
    {"name": "Hopin", "url": "https://hopin.com/{}", "check": "profile"},
    {"name": "Restream", "url": "https://restream.io/{}", "check": "profile"},
    {"name": "StreamElements", "url": "https://streamelements.com/{}", "check": "profile"},
    {"name": "Flarum", "url": "https://discuss.flarum.org/u/{}", "check": "profile"},
    {"name": "Vanilla Forums", "url": "https://vanilla.com/profile/{}", "check": "profile"},
    {"name": "Discourse", "url": "https://meta.discourse.org/u/{}", "check": "profile"},
    {"name": "NodeBB", "url": "https://community.nodebb.org/user/{}", "check": "profile"},
    {"name": "XenForo", "url": "https://xenforo.com/community/members/{}/", "check": "profile"},
    {"name": "ProBoards", "url": "https://{}.proboards.com", "check": "profile"},
    {"name": "Forumotion", "url": "https://{}.forumotion.com", "check": "profile"},
    {"name": "Tapatalk", "url": "https://www.tapatalk.com/groups/{}/", "check": "profile"},
    {"name": "Nextdoor", "url": "https://nextdoor.com/profile/{}", "check": "profile"},
    {"name": "Yubo", "url": "https://yubo.live/{}", "check": "profile"},
    {"name": "Tagged", "url": "https://www.tagged.com/{}", "check": "profile"},
    {"name": "Badoo", "url": "https://badoo.com/profile/{}", "check": "profile"},
    {"name": "Weverse", "url": "https://weverse.io/artist/{}", "check": "profile"},
    {"name": "Zepeto", "url": "https://web.zepeto.me/{}", "check": "profile"},
    {"name": "BeReal", "url": "https://bereal.com/{}", "check": "profile"},
    {"name": "Poparazzi", "url": "https://poparazzi.com/{}", "check": "profile"},
    {"name": "Renren", "url": "http://www.renren.com/{}", "check": "profile"},
    {"name": "Vero", "url": "https://vero.co/{}", "check": "profile"},
    {"name": "Investing.com", "url": "https://www.investing.com/members/{}", "check": "profile"},
    {"name": "ForexFactory", "url": "https://www.forexfactory.com/showthread.php?u={}", "check": "profile"},
    {"name": "MyFxBook", "url": "https://www.myfxbook.com/members/{}", "check": "profile"},
    {"name": "Creative Market", "url": "https://creativemarket.com/{}", "check": "profile"},
    {"name": "ThemeForest", "url": "https://themeforest.net/user/{}", "check": "profile"},
    {"name": "CodeCanyon", "url": "https://codecanyon.net/user/{}", "check": "profile"},
    {"name": "Envato", "url": "https://envato.com/{}", "check": "profile"},
    {"name": "LemonSqueezy", "url": "https://app.lemonsqueezy.com/{}", "check": "profile"},
    {"name": "Stripe", "url": "https://dashboard.stripe.com/{}", "check": "profile"},
    {"name": "Wise", "url": "https://wise.com/user/{}", "check": "profile"},
    {"name": "Revolut", "url": "https://www.revolut.com/{}", "check": "profile"},
    {"name": "Rentry", "url": "https://rentry.co/{}", "check": "profile"},
    {"name": "Telegraph", "url": "https://telegra.ph/{}", "check": "profile"},
    {"name": "Write.as", "url": "https://write.as/{}", "check": "profile"},
    {"name": "Read.cv", "url": "https://read.cv/{}", "check": "profile"},
    {"name": "Squarespace", "url": "https://{}.squarespace.com", "check": "profile"},
    {"name": "Khan Academy", "url": "https://www.khanacademy.org/profile/{}", "check": "profile"},
    {"name": "Codecademy", "url": "https://www.codecademy.com/profiles/{}", "check": "profile"},
    {"name": "Memrise", "url": "https://www.memrise.com/user/{}/", "check": "profile"},
    {"name": "HackerEarth", "url": "https://www.hackerearth.com/@{}", "check": "profile"},
    {"name": "Bugzilla", "url": "https://bugzilla.mozilla.org/user_profile?login={}", "check": "profile"},
    {"name": "Jira", "url": "https://jira.atlassian.com/secure/ViewProfile.jspa?name={}", "check": "profile"},
    {"name": "Trello", "url": "https://trello.com/{}", "check": "profile"},
    {"name": "Asana", "url": "https://app.asana.com/-/user/{}", "check": "profile"},
    {"name": "Monday.com", "url": "https://{}.monday.com", "check": "profile"},
    {"name": "ClickUp", "url": "https://app.clickup.com/u/{}", "check": "profile"},
    {"name": "Figshare", "url": "https://figshare.com/authors/{}/", "check": "profile"},
    {"name": "Zenodo", "url": "https://zenodo.org/search?q=owners:{}", "check": "profile"},
    {"name": "OSF.io", "url": "https://osf.io/{}/", "check": "profile"},
    {"name": "SourceHut", "url": "https://sr.ht/~{}/", "check": "profile"},
    {"name": "FossHub", "url": "https://www.fosshub.com/developer/{}", "check": "profile"},
    {"name": "Modrinth", "url": "https://modrinth.com/user/{}", "check": "profile"},
    {"name": "WeHeartIt", "url": "https://weheartit.com/{}", "check": "profile"},
    {"name": "Zing Me", "url": "https://zingme.vn/{}", "check": "profile"},
    {"name": "Cyworld", "url": "https://www.cyworld.com/home/{}", "check": "profile"},
    {"name": "Gree", "url": "https://gree.jp/{}", "check": "profile"},
    {"name": "KakaoStory", "url": "https://story.kakao.com/{}", "check": "profile"},
    {"name": "Band.us", "url": "https://band.us/{}", "check": "profile"},
    {"name": "Naver Cafe", "url": "https://cafe.naver.com/{}", "check": "profile"},
    {"name": "Dcard", "url": "https://www.dcard.tw/@{}", "check": "profile"},
    {"name": "Komica", "url": "https://komica.org/{}", "check": "profile"},
    {"name": "QQ Zone", "url": "https://user.qzone.qq.com/{}", "check": "profile"},
    {"name": "Mafengwo", "url": "https://www.mafengwo.cn/u/{}.html", "check": "profile"},
    {"name": "YikYak", "url": "https://yikyak.com/{}", "check": "profile"},
    {"name": "Urban Dictionary", "url": "https://www.urbandictionary.com/author.php?author={}", "check": "profile"},
    {"name": "FunnyJunk", "url": "https://funnyjunk.com/user/{}", "check": "profile"},
    {"name": "Memedroid", "url": "https://www.memedroid.com/user/{}", "check": "profile"},
    {"name": "OpenVK", "url": "https://openvk.su/{}", "check": "profile"},
    {"name": "Sharkey", "url": "https://shonk.social/@{}", "check": "profile"},
    {"name": "Calckey", "url": "https://calckey.social/@{}", "check": "profile"},
    {"name": "Akkoma", "url": "https://akkoma.social/users/{}", "check": "profile"},
    {"name": "Firefish", "url": "https://firefish.social/@{}", "check": "profile"},
    {"name": "Friendica", "url": "https://friendica.social/profile/{}", "check": "profile"},
    {"name": "Hubzilla", "url": "https://hubzilla.org/channel/{}", "check": "profile"},
    {"name": "GNU Social", "url": "https://gnusocial.net/{}", "check": "profile"},
    {"name": "WriteFreely", "url": "https://write.as/{}", "check": "profile"},
    {"name": "Prismo", "url": "https://prismo.news/u/{}", "check": "profile"},
    {"name": "Pleroma", "url": "https://pleroma.social/users/{}", "check": "profile"},
    {"name": "Misskey", "url": "https://misskey.io/@{}", "check": "profile"},
    {"name": "Bio.fm", "url": "https://bio.fm/{}", "check": "profile"},
    {"name": "Koji.bio", "url": "https://koji.to/{}", "check": "profile"},
    {"name": "Bio.link", "url": "https://bio.link/{}", "check": "profile"},
    {"name": "Lnk.bio", "url": "https://lnk.bio/{}", "check": "profile"},
    {"name": "Milkshake.bio", "url": "https://msha.ke/{}", "check": "profile"},
    {"name": "Campsite.bio", "url": "https://campsite.bio/{}", "check": "profile"},
    {"name": "Bio.site", "url": "https://bio.site/{}", "check": "profile"},
    {"name": "Taplink", "url": "https://taplink.cc/{}", "check": "profile"},
    {"name": "Stan Store", "url": "https://stan.store/{}", "check": "profile"},
    {"name": "Sellix", "url": "https://{}.selllix.io", "check": "profile"},
    {"name": "Zora", "url": "https://zora.co/{}", "check": "profile"},
    {"name": "Sound.xyz", "url": "https://www.sound.xyz/{}", "check": "profile"},
    {"name": "Lens Protocol", "url": "https://www.lensfrens.xyz/{}", "check": "profile"},
    {"name": "Farcaster", "url": "https://warpcast.com/{}", "check": "profile"},
    {"name": "Nostr", "url": "https://snort.social/p/{}", "check": "profile"},
    {"name": "Damus", "url": "https://damus.io/{}", "check": "profile"},
    {"name": "Session", "url": "https://getsession.org/{}", "check": "profile"},
    {"name": "Element", "url": "https://app.element.io/#/user/{}", "check": "profile"},
    {"name": "Revolt.chat", "url": "https://app.revolt.chat/profile/{}", "check": "profile"},
    {"name": "Manyverse", "url": "https://www.manyver.se/{}", "check": "profile"},
    {"name": "Scuttlebutt", "url": "https://viewer.scuttlebot.io/{}", "check": "profile"},
    {"name": "Retroshare", "url": "https://retroshare.cc/{}", "check": "profile"},
    {"name": "Aether", "url": "https://getaether.net/u/{}", "check": "profile"},
    {"name": "Raddle", "url": "https://raddle.me/user/{}", "check": "profile"},
    {"name": "Post.News", "url": "https://post.news/{}", "check": "profile"},
    {"name": "WT.Social", "url": "https://wt.social/{}", "check": "profile"},
    {"name": "CounterSocial", "url": "https://counter.social/@{}", "check": "profile"},
    {"name": "Soapbox", "url": "https://soapbox.pub/{}", "check": "profile"},
    {"name": "Micro.blog", "url": "https://micro.blog/{}", "check": "profile"},
    {"name": "Posthaven", "url": "https://{}.posthaven.com", "check": "profile"},
    {"name": "Bear Blog", "url": "https://{}.bearblog.dev", "check": "profile"},
    {"name": "Koo", "url": "https://www.kooapp.com/profile/{}", "check": "profile"},
    {"name": "Taringa", "url": "https://www.taringa.net/{}", "check": "profile"},
    {"name": "Skyrock", "url": "https://{}.skyrock.com", "check": "profile"},
    {"name": "Hi5", "url": "https://hi5.com/{}", "check": "profile"},
    {"name": "MyLife", "url": "https://www.mylife.com/{}", "check": "profile"},
    {"name": "Netlog", "url": "https://netlog.com/{}", "check": "profile"},
    {"name": "Friendster", "url": "https://profiles.friendster.com/{}", "check": "profile"},
    {"name": "Cloob", "url": "https://www.cloob.com/{}", "check": "profile"},
    {"name": "Tuenti", "url": "https://www.tuenti.com/{}", "check": "profile"},
    {"name": "Kwai", "url": "https://www.kwai.com/@{}", "check": "profile"},
    {"name": "Lapse", "url": "https://www.lapse.app/{}", "check": "profile"},
    {"name": "Sarahah", "url": "https://sarahah.com/{}", "check": "profile"},
    {"name": "NGL", "url": "https://ngl.link/{}", "check": "profile"},
    {"name": "Sina Weibo", "url": "https://weibo.com/u/{}", "check": "profile"},
    {"name": "Meituan", "url": "https://www.meituan.com/user/{}", "check": "profile"},
    {"name": "PTT.cc", "url": "https://www.ptt.cc/bbs/{}/index.html", "check": "profile"},
    {"name": "Blender Artists", "url": "https://blenderartists.org/u/{}", "check": "profile"},
    {"name": "Krita Artists", "url": "https://krita-artists.org/u/{}", "check": "profile"},
    {"name": "GIMP Chat", "url": "https://www.gimp-forum.net/User-{}", "check": "profile"},
    {"name": "CGTrader", "url": "https://www.cgtrader.com/{}", "check": "profile"},
    {"name": "TurboSquid", "url": "https://www.turbosquid.com/Search/Artists/{}", "check": "profile"},
    {"name": "Shapeways", "url": "https://www.shapeways.com/designer/{}", "check": "profile"},
    {"name": "Adobe Community", "url": "https://community.adobe.com/t5/user/viewprofilepage/user-id/{}", "check": "profile"},
    {"name": "PeoplePerHour", "url": "https://www.peopleperhour.com/freelancer/{}", "check": "profile"},
    {"name": "Guru", "url": "https://www.guru.com/freelancers/{}", "check": "profile"},
    {"name": "Amazon Seller", "url": "https://www.amazon.com/sp?seller={}", "check": "profile"},
    {"name": "AliExpress", "url": "https://www.aliexpress.com/store/{}", "check": "profile"},
    {"name": "Alibaba", "url": "https://www.alibaba.com/profile/{}", "check": "profile"},
    {"name": "Creative Fabrica", "url": "https://www.creativefabrica.com/designer/{}/", "check": "profile"},
    {"name": "Paddle", "url": "https://vendors.paddle.com/{}", "check": "profile"},
    {"name": "PayPal", "url": "https://www.paypal.me/{}", "check": "profile"},
    {"name": "CashApp", "url": "https://cash.app/${}", "check": "profile"},
    {"name": "Venmo", "url": "https://venmo.com/{}", "check": "profile"},
    {"name": "Ghostbin", "url": "https://ghostbin.com/user/{}", "check": "profile"},
    {"name": "ControlC", "url": "http://controlc.com/user/{}", "check": "profile"},
    {"name": "Hastebin", "url": "https://hastebin.com/{}", "check": "profile"},
    {"name": "JustPaste", "url": "https://justpaste.it/{}", "check": "profile"},
    {"name": "PrivateBin", "url": "https://privatebin.net/{}", "check": "profile"},
    {"name": "ZeroBin", "url": "https://zerobin.net/{}", "check": "profile"},
    {"name": "Proton", "url": "https://proton.me/{}", "check": "profile"},
    {"name": "Tutanota", "url": "https://tutanota.com/{}", "check": "profile"},
    {"name": "edX", "url": "https://profile.edx.org/u/{}", "check": "profile"},
    {"name": "Notion", "url": "https://notion.so/{}", "check": "profile"},
    {"name": "Groups.io", "url": "https://groups.io/g/{}", "check": "profile"},
    {"name": "Nabble", "url": "http://nabble.com/{}", "check": "profile"},
    {"name": "Slack", "url": "https://{}.slack.com", "check": "profile"},
    {"name": "Discord", "url": "https://discord.com/users/{}", "check": "profile"},
    {"name": "Matrix", "url": "https://matrix.to/#/@{}:matrix.org", "check": "profile"},
    {"name": "Telegram", "url": "https://t.me/{}", "check": "profile"},
    {"name": "RocketChat", "url": "https://open.rocket.chat/direct/{}", "check": "profile"},
    {"name": "Mattermost", "url": "https://mattermost.com/{}", "check": "profile"},
    {"name": "Zulip", "url": "https://zulipchat.com/{}", "check": "profile"},
    {"name": "Signal", "url": "https://signal.org/{}", "check": "profile"},
    {"name": "QQ", "url": "https://user.qzone.qq.com/{}", "check": "profile"},
    {"name": "Line", "url": "https://line.me/ti/p/{}", "check": "profile"},
    {"name": "Kakao", "url": "https://open.kakao.com/{}", "check": "profile"},
    {"name": "WeChat", "url": "https://weixin.qq.com/{}", "check": "profile"},
    {"name": "WhatsApp", "url": "https://wa.me/{}", "check": "profile"},
    {"name": "Gitter", "url": "https://gitter.im/{}", "check": "profile"},
    {"name": "SimpleX", "url": "https://simplex.chat/{}", "check": "profile"},
    {"name": "TeamSpeak", "url": "https://www.teamspeak.com/user/{}", "check": "profile"},
    {"name": "Mumble", "url": "https://www.mumble.com/{}", "check": "profile"},
    {"name": "Ventrilo", "url": "https://www.ventrilo.com/{}", "check": "profile"},
    {"name": "RaidCall", "url": "https://www.raidcall.com/{}", "check": "profile"},
    {"name": "Twitter Spaces", "url": "https://twitter.com/i/spaces/{}", "check": "profile"},
    {"name": "Reddit Talk", "url": "https://www.reddit.com/talk/{}", "check": "profile"},
    {"name": "Fireside", "url": "https://fireside.fm/{}", "check": "profile"},
    {"name": "Airchat", "url": "https://www.airchat.com/{}", "check": "profile"},
    {"name": "StageIt", "url": "https://www.stageit.com/{}", "check": "profile"},
    {"name": "Livestorm", "url": "https://app.livestorm.co/{}", "check": "profile"},
    {"name": "BigMarker", "url": "https://www.bigmarker.com/{}", "check": "profile"},
    {"name": "Digg", "url": "https://digg.com/users/{}", "check": "profile"},
    {"name": "ElkArte", "url": "https://www.elkarte.net/community/index.php?action=profile;u={}", "check": "profile"},
    {"name": "bbPress", "url": "https://bbpress.org/forums/profile/{}", "check": "profile"},
    {"name": "PunBB", "url": "https://punbb.informer.com/user/{}", "check": "profile"},
    {"name": "FluxBB", "url": "https://fluxbb.org/forums/profile.php?id={}", "check": "profile"},
    {"name": "Phorum", "url": "https://www.phorum.org/profile.php?id={}", "check": "profile"},
    {"name": "WoltLab", "url": "https://www.woltlab.com/user/{}", "check": "profile"},
    {"name": "IP.Board", "url": "https://invisioncommunity.com/profile/{}", "check": "profile"},
    {"name": "Invision", "url": "https://invisionpower.com/clients/{}", "check": "profile"},
    {"name": "MyBB", "url": "https://community.mybb.com/user-{}.html", "check": "profile"},
    {"name": "SMF", "url": "https://www.simplemachines.org/community/index.php?action=profile;u={}", "check": "profile"},
    {"name": "Burning Board", "url": "https://www.woltlab.com/user/{}", "check": "profile"},
    {"name": "Zetaboards", "url": "https://{}.zetaboards.com", "check": "profile"},
    {"name": "Lefora", "url": "https://{}.lefora.com", "check": "profile"},
    {"name": "Snitz", "url": "https://forum.snitz.com/forum/members/{}", "check": "profile"},
    {"name": "Forumer", "url": "https://forumer.com/{}", "check": "profile"},
    {"name": "GroupServer", "url": "https://groupserver.org/r/{}", "check": "profile"},
    {"name": "Google Groups", "url": "https://groups.google.com/u/0/g/{}", "check": "profile"},
    {"name": "Yahoo Groups", "url": "https://groups.yahoo.com/neo/groups/{}", "check": "profile"},
    {"name": "Mailman", "url": "https://mail.python.org/pipermail/{}", "check": "profile"},
    {"name": "Usenet", "url": "https://groups.google.com/g/{}", "check": "profile"},
    {"name": "GitHub Discussions", "url": "https://github.com/{}/discussions", "check": "profile"},
    {"name": "GitLab Discussions", "url": "https://gitlab.com/{}/discussions", "check": "profile"},
    {"name": "StackOverflow Teams", "url": "https://stackoverflow.com/teams/{}", "check": "profile"},
    {"name": "StackOverflow Meta", "url": "https://meta.stackoverflow.com/users/{}", "check": "profile"},
    {"name": "StackOverflow Chat", "url": "https://chat.stackoverflow.com/users/{}", "check": "profile"},
    {"name": "Hive Social", "url": "https://hivesocial.app/{}", "check": "profile"},
    {"name": "Fritter", "url": "https://fritter.cc/{}", "check": "profile"},
    {"name": "SocialHub", "url": "https://socialhub.activitypub.rocks/u/{}", "check": "profile"},
    {"name": "Movim", "url": "https://movim.eu/{}", "check": "profile"},
    {"name": "Librem Social", "url": "https://social.librem.one/@{}", "check": "profile"},
    {"name": "Fediverse", "url": "https://fediverse.party/{}", "check": "profile"},
    {"name": "StatusNet", "url": "https://status.net/{}", "check": "profile"},
    {"name": "Parodify", "url": "https://parodify.com/{}", "check": "profile"},
    {"name": "Soapbox.pub", "url": "https://soapbox.pub/{}", "check": "profile"},
    {"name": "OpenDiary", "url": "https://www.opendiary.com/{}", "check": "profile"},
    {"name": "FriendProject", "url": "https://friendproject.net/{}", "check": "profile"},
    {"name": "Piczo", "url": "https://{}.piczo.com", "check": "profile"},
    {"name": "StudiVZ", "url": "https://www.studivz.net/{}", "check": "profile"},
    {"name": "Facecast", "url": "https://facecast.io/{}", "check": "profile"},
    {"name": "Fanbase", "url": "https://www.fanbase.app/{}", "check": "profile"},
    {"name": "BuzzFeed", "url": "https://www.buzzfeed.com/{}", "check": "profile"},
    {"name": "Slashdot Journal", "url": "https://slashdot.org/~{}/journal", "check": "profile"},
    {"name": "Minds Plus", "url": "https://www.minds.com/{}", "check": "profile"},
    {"name": "Telegraph Profile", "url": "https://t.me/{}", "check": "profile"},
    {"name": "Known CMS", "url": "https://withknown.com/{}", "check": "profile"},
    {"name": "SocialHome", "url": "https://socialhome.network/u/{}", "check": "profile"},
    {"name": "Locals", "url": "https://locals.com/{}", "check": "profile"},
    {"name": "TruthCommunity", "url": "https://communities.win/c/{}", "check": "profile"},
    {"name": "Talkyard", "url": "https://www.talkyard.io/-{}", "check": "profile"},
    {"name": "Coral Talk", "url": "https://coralproject.net/users/{}", "check": "profile"},
    {"name": "Hyvor Talk", "url": "https://talk.hyvor.com/users/{}", "check": "profile"},
    {"name": "Isso", "url": "https://posativ.org/isso/{}", "check": "profile"},
    {"name": "Commento", "url": "https://commento.io/{}", "check": "profile"},
    {"name": "Muut", "url": "https://muut.com/{}", "check": "profile"},
    {"name": "Enjin", "url": "https://www.enjin.com/{}", "check": "profile"},
    {"name": "Stackprinter", "url": "https://www.stackprinter.com/export?service={}", "check": "profile"},
    {"name": "Quip", "url": "https://quip.com/{}", "check": "profile"},
    {"name": "Kialo", "url": "https://www.kialo.com/user/{}", "check": "profile"},
    {"name": "DebateArt", "url": "https://www.debateart.com/users/{}", "check": "profile"},
    {"name": "Change.org", "url": "https://www.change.org/u/{}", "check": "profile"},
    {"name": "Avaaz", "url": "https://secure.avaaz.org/page/en/profile/{}", "check": "profile"},
    {"name": "Care2", "url": "https://www.care2.com/c2c/people/profile/{}", "check": "profile"},
    {"name": "OpenPetition", "url": "https://www.openpetition.de/user/{}", "check": "profile"},
    {"name": "ProductHunt Comments", "url": "https://www.producthunt.com/@{}/comments", "check": "profile"},
    {"name": "Indie Hackers Posts", "url": "https://www.indiehackers.com/{}/history", "check": "profile"},
    {"name": "GitLab Snippets", "url": "https://gitlab.com/snippets?username={}", "check": "profile"},
    {"name": "Bitbucket Issues", "url": "https://bitbucket.org/{}/issues/", "check": "profile"},
    {"name": "SourceForge Discussions", "url": "https://sourceforge.net/u/{}/activity/", "check": "profile"},
    {"name": "Launchpad Bugs", "url": "https://bugs.launchpad.net/~{}", "check": "profile"},
    {"name": "Bugzilla Comments", "url": "https://bugzilla.mozilla.org/user_profile?user_id={}", "check": "profile"},
    {"name": "Trac Tickets", "url": "https://trac.edgewall.org/query?reporter={}", "check": "profile"},
    {"name": "Phabricator Tasks", "url": "https://secure.phabricator.com/p/{}/", "check": "profile"},
    {"name": "OpenCollective", "url": "https://opencollective.com/{}", "check": "profile"},
    {"name": "Ghost", "url": "https://{}.ghost.io", "check": "profile"},
    {"name": "Anchor", "url": "https://anchor.fm/{}", "check": "profile"},
    {"name": "Tidal", "url": "https://tidal.com/{}", "check": "profile"},
    {"name": "Mixlr", "url": "https://mixlr.com/{}", "check": "profile"},
    {"name": "Streamlabs", "url": "https://streamlabs.com/{}", "check": "profile"},
    {"name": "OBS Community", "url": "https://obsproject.com/forum/members/{}/", "check": "profile"},
    {"name": "Caffeine", "url": "https://www.caffeine.tv/{}", "check": "profile"},
    {"name": "Vimm", "url": "https://www.vimm.tv/{}", "check": "profile"},
    {"name": "Brightcove", "url": "https://studio.brightcove.com/{}", "check": "profile"},
    {"name": "Vevo", "url": "https://www.vevo.com/artist/{}", "check": "profile"},
    {"name": "TikTok Live", "url": "https://www.tiktok.com/@{}/live", "check": "profile"},
    {"name": "Facebook Gaming", "url": "https://www.facebook.com/gaming/{}", "check": "profile"},
    {"name": "Twitch Clips", "url": "https://www.twitch.tv/{}/clips", "check": "profile"},
    {"name": "Kick Clips", "url": "https://kick.com/{}/clips", "check": "profile"},
    {"name": "Callin", "url": "https://www.callin.com/{}", "check": "profile"},
    {"name": "Stationhead", "url": "https://stationhead.com/{}", "check": "profile"},
    {"name": "ConcertWindow", "url": "https://concertwindow.com/{}", "check": "profile"},
    {"name": "DTube", "url": "https://d.tube/#!/c/{}", "check": "profile"},
    {"name": "Zerion", "url": "https://app.zerion.io/{}", "check": "profile"},
    {"name": "CryptoPanic", "url": "https://cryptopanic.com/user/{}/", "check": "profile"},
    {"name": "Bitfinex", "url": "https://www.bitfinex.com/u/{}", "check": "profile"},
    {"name": "KuCoin", "url": "https://www.kucoin.com/ucenter/user/{}", "check": "profile"},
    {"name": "Bitstamp", "url": "https://www.bitstamp.net/user/{}", "check": "profile"},
    {"name": "LocalBitcoins", "url": "https://localbitcoins.com/accounts/profile/{}/", "check": "profile"},
    {"name": "CryptoCompare", "url": "https://www.cryptocompare.com/profile/{}/", "check": "profile"},
    {"name": "Robinhood", "url": "https://robinhood.com/{}", "check": "profile"},
    {"name": "BitcoinTalk Market", "url": "https://bitcointalk.org/index.php?action=profile;u={};sa=showPosts", "check": "profile"},
    {"name": "Polygonscan", "url": "https://polygonscan.com/address/{}", "check": "profile"},
    {"name": "LowEndTalk", "url": "https://lowendtalk.com/profile/{}", "check": "profile"},
    {"name": "WildersSecurity", "url": "https://www.wilderssecurity.com/members/{}/", "check": "profile"},
    {"name": "MajorGeeks", "url": "https://forums.majorgeeks.com/members/{}/", "check": "profile"},
    {"name": "MalwareTips", "url": "https://malwaretips.com/members/{}/", "check": "profile"},
    {"name": "Sysnative", "url": "https://www.sysnative.com/forums/members/{}/", "check": "profile"},
    {"name": "Gentoo Forum", "url": "https://forums.gentoo.org/profile.php?mode=viewprofile&u={}", "check": "profile"},
    {"name": "Kali Forum", "url": "https://forums.kali.org/member.php?u={}", "check": "profile"},
    {"name": "Offensive Security", "url": "https://forums.offensive-security.com/member.php?u={}", "check": "profile"},
    {"name": "WebHostingTalk", "url": "https://www.webhostingtalk.com/member/{}", "check": "profile"},
    {"name": "DigitalPoint", "url": "https://forums.digitalpoint.com/members/{}/", "check": "profile"},
    {"name": "WarriorForum", "url": "https://www.warriorforum.com/members/{}.html", "check": "profile"},
    {"name": "SitePoint", "url": "https://www.sitepoint.com/community/u/{}", "check": "profile"},
    {"name": "PrivacyGuides", "url": "https://discuss.privacyguides.net/u/{}", "check": "profile"},
    {"name": "PenTesters", "url": "https://pentesters.forum/members/{}/", "check": "profile"},
    {"name": "KiwiFarms", "url": "https://kiwifarms.net/members/{}/", "check": "profile"},
    {"name": "Lolcow", "url": "https://lolcow.farm/{}", "check": "profile"},
    {"name": "Voat Archive", "url": "https://searchvoat.co/u/{}", "check": "profile"},
    {"name": "Amino Communities", "url": "https://aminoapps.com/c/{}", "check": "profile"},
    {"name": "VK Clips", "url": "https://vk.com/{}/clips", "check": "profile"},
    {"name": "OK.ru Communities", "url": "https://ok.ru/group/{}", "check": "profile"},
    {"name": "Apple Music", "url": "https://music.apple.com/profile/{}", "check": "profile"},
    {"name": "Spotify Community", "url": "https://community.spotify.com/t5/user/viewprofilepage/user-id/{}", "check": "profile"},
    {"name": "IEEE", "url": "https://ieee-collabratec.ieee.org/app/p/{}", "check": "profile"},
    {"name": "SteamRep", "url": "https://steamrep.com/profiles/{}", "check": "profile"},
    {"name": "TwitchTracker", "url": "https://twitchtracker.com/{}", "check": "profile"},
    {"name": "KickTracker", "url": "https://kick-tracker.com/{}", "check": "profile"},
    {"name": "Confluence", "url": "https://confluence.atlassian.com/display/~{}", "check": "profile"}
]

def print_banner():
    banner = f"""{Colors.CYAN}
    ██████╗ ██╗     ██╗███╗   ██╗██████╗ ███████╗██╗   ██╗███████╗
    ██╔══██╗██║     ██║████╗  ██║██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝
    ██████╔╝██║     ██║██╔██╗ ██║██║  ██║█████╗   ╚████╔╝ █████╗  
    ██╔══██╗██║     ██║██║╚██╗██║██║  ██║██╔══╝    ╚██╔╝  ██╔══╝  
    ██████╔╝███████╗██║██║ ╚████║██████╔╝███████╗   ██║   ███████╗
    ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
    {Colors.ENDC}"""
    
    print(banner)
    print(f"{Colors.MAGENTA}{'='*70}{Colors.ENDC}")
    print(f"{Colors.YELLOW}{LANG['banner'].center(70)}{Colors.ENDC}")
    print(f"{Colors.WHITE}{LANG['author'].center(70)}: {Colors.GREEN}@tc4dy{Colors.ENDC}".center(80))
    print(f"{Colors.GRAY}{LANG['legal'].center(70)}{Colors.ENDC}")
    print(f"{Colors.MAGENTA}{'='*70}{Colors.ENDC}\n")

def select_language():
    global LANG, CURRENT_LANG
    
    print(f"{Colors.CYAN}{Colors.BOLD}[?] {LANG.get('select_lang', 'Select Language / Dil Seçin')}{Colors.ENDC}")
    print(f"{Colors.WHITE}[1] English")
    print(f"[2] Türkçe{Colors.ENDC}\n")
    
    choice = input(f"{Colors.GREEN}> {Colors.ENDC}").strip()
    
    if choice == "2":
        CURRENT_LANG = 'tr'
    else:
        CURRENT_LANG = 'en'
    
    LANG = TRANSLATIONS[CURRENT_LANG]

def signal_handler(sig, frame):
    print(f"\n\n{Colors.YELLOW}[!] {LANG['interrupted']}{Colors.ENDC}")
    print(f"{Colors.CYAN}[*] {LANG['saving_progress']}{Colors.ENDC}\n")
    
    stop_flag.set()
    
    if global_results['accounts'] or global_results['comments']:
        save_results(global_results)
    
    print(f"\n{Colors.RED}[!] Exiting BlindEye...{Colors.ENDC}")
    sys.exit(0)

def generate_variations(name):
    variations = set()
    variations.add(name)
    variations.add(name.lower())
    variations.add(name.upper())
    variations.add(name.capitalize())
    variations.add(name.title())
    
    if len(name) > 1:
        variations.add(name[0].upper() + name[1:].lower())
        variations.add(name[0].lower() + name[1:].upper())
        
    words = name.split()
    if len(words) > 1:
        for word in words:
            variations.add(word.lower())
            variations.add(word.upper())
            variations.add(word.capitalize())
    
    return list(variations)

def check_url(platform, username, mode, results, lock):
    if stop_flag.is_set():
        return
        
    try:
        url = platform['url'].format(username)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if stop_flag.is_set():
            return
        
        status = None
        if response.status_code == 200:
            if 'profile' in platform['check']:
                content_checks = [
                    'profile' in response.text.lower(),
                    'user' in response.text.lower(),
                    username.lower() in response.text.lower(),
                    len(response.content) > 500
                ]
                if any(content_checks):
                    status = LANG['active']
        elif response.status_code == 404:
            status = LANG['not_found']
        
        if status == LANG['active'] and not stop_flag.is_set():
            with lock:
                results['accounts'].append({
                    'platform': platform['name'],
                    'url': url,
                    'status': status
                })
                global_results['accounts'].append({
                    'platform': platform['name'],
                    'url': url,
                    'status': status
                })
                print(f"{Colors.GREEN}[+] {LANG['found_accounts']}: {Colors.WHITE}{platform['name']} {Colors.CYAN}→ {url}{Colors.ENDC}")
        
    except requests.Timeout:
        pass
    except Exception:
        pass

def search_comments_mentions(username, results, lock):
    if stop_flag.is_set():
        return
        
    search_engines = [
        f'https://www.google.com/search?q="@{username}"',
        f'https://www.google.com/search?q="{username}"+comment',
        f'https://www.google.com/search?q="{username}"+mentioned'
    ]
    
    for engine in search_engines:
        if stop_flag.is_set():
            return
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(engine, headers=headers, timeout=10)
            
            if stop_flag.is_set():
                return
            
            if response.status_code == 200:
                links = re.findall(r'https?://[^\s<>"]+', response.text)
                for link in links[:5]:
                    if stop_flag.is_set():
                        return
                    if any(platform in link for platform in ['twitter', 'instagram', 'reddit', 'facebook', 'youtube']):
                        with lock:
                            results['comments'].append({
                                'platform': 'Web Search',
                                'url': link,
                                'type': 'Mention/Comment'
                            })
                            global_results['comments'].append({
                                'platform': 'Web Search',
                                'url': link,
                                'type': 'Mention/Comment'
                            })
        except Exception:
            pass

def deep_search(targets, mode, results, lock):
    for target in targets:
        if stop_flag.is_set():
            break
            
        variations = generate_variations(target)
        
        for variation in variations:
            if stop_flag.is_set():
                break
                
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = []
                for platform in PLATFORMS:
                    if stop_flag.is_set():
                        break
                        
                    if mode == 1:
                        futures.append(executor.submit(check_url, platform, variation, mode, results, lock))
                    elif mode == 2:
                        futures.append(executor.submit(check_url, platform, variation, mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"{variation}_", mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"{variation}123", mode, results, lock))
                    elif mode == 3:
                        futures.append(executor.submit(check_url, platform, variation, mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"{variation}_", mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"_{variation}", mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"{variation}123", mode, results, lock))
                        futures.append(executor.submit(check_url, platform, f"{variation}_official", mode, results, lock))
                
                for future in as_completed(futures):
                    if stop_flag.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    future.result()
            
            if not stop_flag.is_set():
                search_comments_mentions(variation, results, lock)

def save_results(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blindeye_results_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("BlindEye OSINT Tool - Search Results\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"\n{LANG['found_accounts']}\n")
        f.write("-"*70 + "\n")
        for acc in results['accounts']:
            f.write(f"{LANG['platform']}: {acc['platform']}\n")
            f.write(f"{LANG['url']}: {acc['url']}\n")
            f.write(f"{LANG['status']}: {acc['status']}\n")
            f.write("-"*70 + "\n")
        
        f.write(f"\n{LANG['found_comments']}\n")
        f.write("-"*70 + "\n")
        for com in results['comments']:
            f.write(f"{LANG['platform']}: {com['platform']}\n")
            f.write(f"{LANG['url']}: {com['url']}\n")
            f.write(f"{LANG['type']}: {com['type']}\n")
            f.write("-"*70 + "\n")
        
        f.write(f"\n{LANG['total_found']}: {len(results['accounts'])} {LANG['accounts']}, {len(results['comments'])} {LANG['comments']}\n")
    
    print(f"\n{Colors.GREEN}[✓] {LANG['file_saved']}: {filename}{Colors.ENDC}")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    select_language()
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    
    while True:
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.CYAN}{Colors.BOLD}║{Colors.ENDC} {LANG['main_menu'].center(64)} {Colors.CYAN}{Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")
        
        print(f"{Colors.YELLOW}{LANG['search_type']}:{Colors.ENDC}")
        print(f"{Colors.WHITE}[1] {LANG['mode_1']}")
        print(f"[2] {LANG['mode_2']}")
        print(f"[3] {LANG['mode_3']}")
        print(f"[4] {LANG['mode_4']}{Colors.ENDC}\n")
        
        mode = input(f"{Colors.GREEN}[{LANG['enter_choice']}]> {Colors.ENDC}").strip()
        
        if mode == '4':
            print(f"\n{Colors.RED}[!] Exiting BlindEye...{Colors.ENDC}")
            sys.exit(0)
        
        if mode not in ['1', '2', '3']:
            print(f"{Colors.RED}[!] {LANG['invalid_choice']}{Colors.ENDC}")
            continue
        
        mode = int(mode)
        
        if mode != 3:
            print(f"\n{Colors.YELLOW}{LANG['input_type']}:{Colors.ENDC}")
            print(f"{Colors.WHITE}[1] {LANG['input_username']}")
            print(f"[2] {LANG['input_realname']}")
            print(f"[3] {LANG['input_both']}{Colors.ENDC}\n")
            
            input_type = input(f"{Colors.GREEN}> {Colors.ENDC}").strip()
            
            targets = []
            if input_type in ['1', '3']:
                username = input(f"\n{Colors.CYAN}[{LANG['enter_username']}]> {Colors.ENDC}").strip()
                targets.append(username)
            
            if input_type in ['2', '3']:
                realname = input(f"{Colors.CYAN}[{LANG['enter_realname']}]> {Colors.ENDC}").strip()
                targets.append(realname)
        else:
            targets_input = input(f"\n{Colors.CYAN}[{LANG['enter_targets']}]> {Colors.ENDC}").strip()
            targets = [t.strip() for t in targets_input.split(',')]
            
            if len(targets) < 3 or len(targets) > 12:
                print(f"{Colors.RED}[!] {LANG['invalid_targets']}{Colors.ENDC}")
                continue
        
        global global_results, stop_flag
        stop_flag.clear()
        global_results = {
            'accounts': [],
            'comments': [],
            'other': []
        }
        
        results = {
            'accounts': [],
            'comments': [],
            'other': []
        }
        lock = threading.Lock()
        
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] {LANG['searching']}...{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Press Ctrl+C to stop and save results{Colors.ENDC}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.ENDC}\n")
        
        deep_search(targets, mode, results, lock)
        
        if stop_flag.is_set():
            print(f"\n{Colors.YELLOW}[!] {LANG['search_stopped']}{Colors.ENDC}")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner()
            continue
        
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.ENDC}")
        print(f"{Colors.GREEN}[✓] {LANG['search_complete']}{Colors.ENDC}")
        print(f"{Colors.CYAN}[*] {LANG['total_found']}: {len(results['accounts'])} {LANG['accounts']}, {len(results['comments'])} {LANG['comments']}{Colors.ENDC}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.ENDC}\n")
        
        save_choice = input(f"{Colors.YELLOW}[?] {LANG['save_results']} {Colors.ENDC}").strip().lower()
        if save_choice in ['y', 'yes', 'e', 'evet']:
            save_results(results)
        
        input(f"\n{Colors.GRAY}{LANG['press_continue']}{Colors.ENDC}")
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Interrupted by user. Exiting...{Colors.ENDC}")
        sys.exit(0)