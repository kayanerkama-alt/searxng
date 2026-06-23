# ⚛ Atomic Search

**Privacy-first metasearch engine with intelligent ranking, like Kagi but completely free and open source.**

## 🚀 Features

### 1. **Intelligent Ranking System**
- Learns from your clicks and preferences
- Automatically ranks trusted sites higher
- Time-decay algorithm (preferences fade after 7 days)
- All data stored locally in browser (100% private)

### 2. **Advanced Spam Detection**
- Filters SEO spam and low-quality domains
- Detects affiliate spam and dropship sites
- Identifies clickbait and misleading content
- One-click spam reporting

### 3. **Weather Integration**
- Detects weather queries automatically
- Extracts location from search terms
- Provides weather context for relevant searches

### 4. **Modern Kagi-like UI**
- Dark theme with glassmorphism effects
- Smooth animations and transitions
- Responsive design for all devices
- Fast and lightweight

### 5. **Privacy & Security**
✅ No tracking cookies  
✅ No user profiling  
✅ No ads or sponsored results  
✅ All preferences stored locally  
✅ Open source & transparent  

## 🎨 UI Features

- **Beautiful dark theme** with gradient accents
- **Result ranking display** showing trusted sources
- **Action buttons** to prefer or report spam
- **Smooth animations** on page load
- **Mobile-responsive** design
- **Fast search** with instant results

## 🛠️ Technical Stack

- **Backend**: Python + Flask
- **Frontend**: Vanilla JavaScript (no tracking libraries)
- **Storage**: Browser localStorage (client-side only)
- **Build**: Docker + Railway

## 📦 Deployment

### Railway
```bash
# Deploy directly from GitHub
# Service: atomic-search
# Branch: main
# Port: 8888
```

### Docker
```bash
docker build -t atomic-search .
docker run -p 8888:8888 atomic-search
```

### Local Development
```bash
pip install -r requirements.txt
python -m searx.webapp
```

## 🔧 Configuration

Edit `searx/settings.yml` to customize:
- Search engines
- UI theme
- Privacy settings
- Performance options

## 📊 Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Spam detection accuracy
- UI/UX enhancements
- Performance optimization
- New features

## 📄 License

AGPL-3.0 (same as SearXNG)

## 🔗 Links

- [GitHub](https://github.com/kayanerkama-alt/searxng)
- [Issues](https://github.com/kayanerkama-alt/searxng/issues)
- [Discussions](https://github.com/kayanerkama-alt/searxng/discussions)

---

**Made with ❤️ for privacy-conscious users**

