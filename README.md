
  ██████╗ ██╗     ██╗███╗   ██╗██████╗ ███████╗██╗   ██╗███████╗
  ██╔══██╗██║     ██║████╗  ██║██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝
  ██████╔╝██║     ██║██╔██╗ ██║██║  ██║█████╗   ╚████╔╝ █████╗  
  ██╔══██╗██║     ██║██║╚██╗██║██║  ██║██╔══╝    ╚██╔╝  ██╔══╝  
  ██████╔╝███████╗██║██║ ╚████║██████╔╝███████╗   ██║   ███████╗

  👁️ BlindEye OSINT Tool
  🔍 Advanced OSINT Intelligence Gathering Tool
  
Hunt down digital footprints across 580+ platforms with 50+ search combinations

**🔍 Advanced OSINT Intelligence Gathering Tool**

*Hunt down digital footprints across 580+ platforms with 50+ search combinations*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Platforms](#-supported-platforms) • [Examples](#-examples)


---

## 📋 Overview

**BlindEye** is a powerful Open Source Intelligence (OSINT) tool designed for security researchers, penetration testers, and digital investigators. With support for **580+ platforms** and **50+ username/name variations**, BlindEye helps you discover digital footprints across the internet in seconds.

### 🎯 What Makes BlindEye Special?

- 🌐 **580+ Platforms** - From social media to developer communities
- 🔄 **50+ Combinations** - Intelligent username variation generation
- ⚡ **Multi-threaded** - Lightning-fast concurrent scanning
- 🌍 **Bilingual** - Full English & Turkish language support
- 💾 **Auto-save** - Interrupt anytime with Ctrl+C, results are saved
- 🎨 **Beautiful UI** - Colored terminal output for better readability
- 📊 **Detailed Reports** - Comprehensive TXT reports with timestamps

---

## ✨ Features

### 🔍 Search Modes

#### 1. **Exact Match Search** 🎯
- Direct username lookup across all platforms
- Fast and precise results
- Perfect for known usernames

#### 2. **Partial Match Search** 🔎
- Includes common variations (_username, username123)
- Broader coverage
- Catches modified usernames

#### 3. **RAGE MODE** 💥
- Multi-target deep search (3-12 targets)
- Maximum variations per target
- Comprehensive digital footprint analysis
- Official account variations included

### 🌐 Platform Categories

| Category | Platforms |
|----------|-----------|
| 🎮 **Gaming** | Steam, Xbox, PlayStation, Twitch, Roblox, Epic Games |
| 💻 **Developer** | GitHub, GitLab, StackOverflow, CodePen, HackerRank |
| 🔐 **Security** | HackTheBox, TryHackMe, Bugcrowd, HackerOne, Root-Me |
| 🎨 **Creative** | Behance, Dribbble, ArtStation, DeviantArt, Pixiv |
| 💰 **Crypto** | Binance, Coinbase, OpenSea, Etherscan, Rarible |
| 📱 **Social Media** | Twitter, Instagram, TikTok, Reddit, LinkedIn, Threads |
| 🎵 **Music** | Spotify, SoundCloud, Bandcamp, Last.fm, Mixcloud |
| 📚 **Learning** | Coursera, Udemy, Khan Academy, edX, Skillshare |
| 🛍️ **Marketplace** | Etsy, eBay, Fiverr, Upwork, Gumroad |
| 🎬 **Media** | YouTube, Vimeo, DailyMotion, TikTok, Twitch |

**And 500+ more platforms!**

---

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Quick Install

```bash
# Clone the repository
git clone https://github.com/tc4dy/BlindEye

# Navigate to directory
cd blindeye

# Install dependencies
pip install -r requirements.txt

# Run BlindEye
python blindeye.py
```

### Windows Users

```cmd
git clone https://github.com/tc4dy/BlindEye
cd blindeye
pip install -r requirements.txt
python blindeye.py
```

### Linux/macOS Users

```bash
git clone https://github.com/tc4dy/BlindEye
cd blindeye
pip3 install -r requirements.txt
python3 blindeye.py
```

---

## 📖 Usage

### Step-by-Step Guide

#### 1️⃣ Launch BlindEye
```bash
python blindeye.py
```

#### 2️⃣ Select Language
```
Select Language / Dil Seçin
[1] English
[2] Türkçe
```

#### 3️⃣ Choose Search Mode
```
[1] Exact Match Search
[2] Partial Match Search (contains)
[3] RAGE MODE (Multi-target Deep Search)
[4] Exit
```

#### 4️⃣ Enter Target Information
- **Username/Nickname** - Social media handles
- **Real Name** - Person's actual name
- **Both** - Search using both username and real name

#### 5️⃣ Wait for Results
- Results appear in real-time
- Press **Ctrl+C** to stop and save current progress
- All findings are automatically categorized

#### 6️⃣ Save Results
- Option to save results to timestamped TXT file
- Format: `blindeye_results_YYYYMMDD_HHMMSS.txt`

---

## 💡 Examples

### Example 1: Single Username Search

```bash
$ python blindeye.py

Select Search Type: [1] Exact Match Search

Enter username/nickname: johndoe

[+] FOUND ACCOUNTS: GitHub → https://github.com/johndoe
[+] FOUND ACCOUNTS: Twitter/X → https://twitter.com/johndoe
[+] FOUND ACCOUNTS: Instagram → https://instagram.com/johndoe/

Total Found: 3 accounts
```

### Example 2: RAGE MODE Multi-Target

```bash
$ python blindeye.py

Select Search Type: [3] RAGE MODE

Enter target names (min 3, max 12): alice, bob, charlie, david

[+] FOUND ACCOUNTS: alice - GitHub → https://github.com/alice
[+] FOUND ACCOUNTS: alice_official - Instagram → https://instagram.com/alice_official/
[+] FOUND ACCOUNTS: bob123 - Reddit → https://reddit.com/user/bob123
[+] FOUND ACCOUNTS: charlie - Steam → https://steamcommunity.com/id/charlie

Total Found: 47 accounts, 12 comments/mentions
```

### Example 3: Real Name Search

```bash
$ python blindeye.py

Select Search Type: [2] Partial Match Search

Select Input Type: [2] Real Name

Enter real name: John Smith

[+] FOUND ACCOUNTS: LinkedIn → https://linkedin.com/in/johnsmith
[+] FOUND ACCOUNTS: Academia → https://independent.academia.edu/JohnSmith
[+] FOUND ACCOUNTS: ResearchGate → https://researchgate.net/profile/John-Smith

Total Found: 8 accounts
```

---

## 📊 Supported Platforms

<details>
<summary>🎮 Gaming Platforms (50+)</summary>

- Steam
- Xbox Live
- PlayStation Network
- Epic Games
- Battle.net
- Riot Games
- EA
- Roblox
- Minecraft Forums
- Twitch
- Kick
- And 40+ more...

</details>

<details>
<summary>💻 Developer Platforms (80+)</summary>

- GitHub
- GitLab
- Bitbucket
- StackOverflow
- CodePen
- Replit
- HackerRank
- LeetCode
- Kaggle
- Docker Hub
- And 70+ more...

</details>

<details>
<summary>📱 Social Media (60+)</summary>

- Twitter/X
- Facebook
- Instagram
- TikTok
- Reddit
- LinkedIn
- Threads
- Mastodon
- Bluesky
- Tumblr
- And 50+ more...

</details>

<details>
<summary>🔐 Security & CTF (30+)</summary>

- HackTheBox
- TryHackMe
- Root-Me
- Bugcrowd
- HackerOne
- PentesterLab
- Exploit-DB
- OWASP
- And 22+ more...

</details>

<details>
<summary>🎨 Creative Platforms (40+)</summary>

- Behance
- Dribbble
- ArtStation
- DeviantArt
- Pixiv
- Unsplash
- 500px
- Flickr
- And 32+ more...

</details>

<details>
<summary>💰 Crypto & NFT (25+)</summary>

- Binance
- Coinbase
- OpenSea
- Rarible
- Etherscan
- Foundation
- Mirror.xyz
- And 18+ more...

</details>

**Total: 580+ platforms and growing!**

---

## 🎨 Screenshots

### Main Menu
```
    ██████╗ ██╗     ██╗███╗   ██╗██████╗ ███████╗██╗   ██╗███████╗
    ██╔══██╗██║     ██║████╗  ██║██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝
    ██████╔╝██║     ██║██╔██╗ ██║██║  ██║█████╗   ╚████╔╝ █████╗  
    ██╔══██╗██║     ██║██║╚██╗██║██║  ██║██╔══╝    ╚██╔╝  ██╔══╝  
    ██████╔╝███████╗██║██║ ╚████║██████╔╝███████╗   ██║   ███████╗
    ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
```

### Search Results
```
[+] FOUND ACCOUNTS: GitHub → https://github.com/target
[+] FOUND ACCOUNTS: Twitter/X → https://twitter.com/target
[+] FOUND ACCOUNTS: LinkedIn → https://linkedin.com/in/target
```

---

## ⚙️ Configuration

### Search Variations

BlindEye automatically generates 50+ variations including:

- Original username
- Lowercase/Uppercase variations
- Capitalized forms
- With underscores: `_username`, `username_`
- With numbers: `username123`, `username1`
- Official variants: `username_official`
- And many more intelligent combinations

### Threading

- Default: 20 concurrent threads
- Adjustable for different system capabilities
- Automatic timeout handling (10 seconds per request)

---

## 🛡️ Legal Disclaimer

**BlindEye** is designed for:
- ✅ Legal security research
- ✅ Authorized penetration testing
- ✅ Educational purposes
- ✅ Personal OSINT investigations
- ✅ Digital footprint analysis

**NOT for:**
- ❌ Unauthorized access attempts
- ❌ Harassment or stalking
- ❌ Privacy violations
- ❌ Illegal activities

**Users are responsible for complying with applicable laws and regulations.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution

- 🌐 Add more platforms
- 🌍 Add more languages
- 🎨 Improve UI/UX
- 🐛 Report bugs
- 📝 Improve documentation

---

## 📝 Changelog

### v1.0.0 (Current)
- ✨ Initial release
- 🌐 580+ platforms support
- 🔄 50+ username variations
- 🌍 English & Turkish language support
- 💾 Auto-save on Ctrl+C interrupt
- ⚡ Multi-threaded scanning
- 📊 Detailed TXT reports

---

## 🙏 Acknowledgments

- Inspired by various OSINT tools in the community
- Thanks to all contributors
- Built with ❤️ for the security research community

---

## 📧 Contact

- **Developer**: @tc4dy
- **Issues**: [GitHub Issues](https://github.com/yourusername/blindeye/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/blindeye/discussions)

---

## ⭐ Star History

If you find BlindEye useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with 🔍 and ☕ by @tc4dy**

[⬆ Back to Top](#-blindeye-osint-tool)

</div>

---

# 🇹🇷 Türkçe Döküman

## 📋 Genel Bakış

**BlindEye**, güvenlik araştırmacıları, penetrasyon testçileri ve dijital araştırmacılar için tasarlanmış güçlü bir Açık Kaynak İstihbarat (OSINT) aracıdır. **580+ platform** ve **50+ kullanıcı adı/isim varyasyonu** desteği ile BlindEye, saniyeler içinde internet genelinde dijital ayak izlerini keşfetmenize yardımcı olur.

## 🚀 Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/yourusername/blindeye.git

# Klasöre gidin
cd blindeye

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# BlindEye'ı çalıştırın
python blindeye.py
```

## 📖 Kullanım

1. **Dil Seçin**: Türkçe için [2] seçeneğini seçin
2. **Arama Modu**: İstediğiniz arama modunu seçin
3. **Hedef Girin**: Kullanıcı adı veya gerçek isim girin
4. **Sonuçları İnceleyin**: Gerçek zamanlı sonuçları görün
5. **Kaydedin**: Sonuçları TXT dosyasına kaydedin

## ⚡ Özellikler

- 🌐 **580+ Platform** - Sosyal medyadan geliştirici topluluklarına
- 🔄 **50+ Kombinasyon** - Akıllı kullanıcı adı varyasyon üretimi
- ⚡ **Çok Thread'li** - Yıldırım hızında eşzamanlı tarama
- 💾 **Otomatik Kayıt** - Ctrl+C ile durdurun, sonuçlar kaydedilir

---


**Lisans**: MIT License - Detaylar için LICENSE dosyasına bakın


