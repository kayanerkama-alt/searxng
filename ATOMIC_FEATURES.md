# Atomic Search - Advanced Features

Atomic Search is a privacy-first metasearch engine with intelligent ranking, spam detection, and user preference learning.

## Features

### 1. **Intelligent User Preference Ranking**
- Tracks your clicks on search results
- Learns which websites you prefer
- Automatically ranks preferred sites higher in future searches
- Time-decay algorithm: preferences fade after 7 days of non-use
- All data stored locally in browser cookies (no server tracking)

**How it works:**
- Click on a result → Atomic learns you like that domain
- Each click increases the domain's ranking score by 10 points
- Domains you haven't clicked in 7+ days gradually lose ranking boost
- Completely private: data never leaves your browser

### 2. **Spam Detection & Filtering**
- Automatically detects and demotes SEO spam
- Filters low-quality domains (free TK/ML/GA/CF domains)
- Identifies affiliate spam and dropship sites
- Detects clickbait and misleading content
- Spam score: 0-100 (higher = more spam)

**Spam patterns detected:**
- Free domain extensions (.tk, .ml, .ga, .cf)
- Social media spam (Pinterest, Quora, Reddit, Medium)
- Affiliate spam (Amazon with tracking tags)
- Dropship sites (AliExpress, Wish, DHgate)
- Clickbait keywords (limited offer, act now, guaranteed, etc.)

**User controls:**
- Mark any result as spam with one click
- Spammed domains are hidden and deprioritized
- Spam list stored locally in your browser

### 3. **Weather Integration**
- Detects weather-related queries
- Extracts location from search query
- Provides weather context for relevant searches
- Supports queries like: "weather in London", "NYC forecast", "temperature in Tokyo"

### 4. **Modern Kagi-like UI**
- Clean, minimalist dark theme
- Gradient accents (blue → cyan)
- Smooth animations and transitions
- Responsive design for all devices
- Fast, lightweight interface

**Design features:**
- Glassmorphism effects with backdrop blur
- Gradient text for branding
- Hover effects on results
- Color-coded action buttons
- Privacy-focused aesthetic

## Technical Details

### Architecture
- **Frontend:** Vanilla JavaScript (no tracking libraries)
- **Backend:** Python with Flask
- **Storage:** Browser localStorage (client-side only)
- **Privacy:** No server-side user tracking

### Files Modified
- `searx/templates/simple/base.html` - New UI with Atomic branding
- `searx/templates/simple/results.html` - Result ranking and spam controls
- `searx/templates/simple/search.html` - Search interface redesign
- `searx/atomic_features.py` - Core feature implementations

### Key Classes

#### SpamDetector
```python
SpamDetector.is_spam(url, title, snippet)  # Boolean check
SpamDetector.get_spam_score(url, title, snippet)  # 0-100 score
```

#### UserPreferences
```python
UserPreferences.calculate_ranking_boost(domain, user_prefs)
UserPreferences.serialize_prefs(prefs)
UserPreferences.deserialize_prefs(prefs_json)
```

#### WeatherIntegration
```python
WeatherIntegration.extract_weather_query(query)
WeatherIntegration.get_weather_context(query)
```

#### ResultRanker
```python
ResultRanker.calculate_score(result, user_prefs, spam_detector)
ResultRanker.rerank_results(results, user_prefs)
```

## Privacy & Security

✅ **100% Private**
- No tracking cookies
- No user profiling
- No data sent to servers
- All preferences stored locally

✅ **Open Source**
- Full source code available
- Community-driven development
- Transparent algorithms

✅ **No Ads**
- No sponsored results
- No affiliate links
- No tracking pixels

## Browser Compatibility
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Enhancements
- [ ] Custom ranking weights
- [ ] Result preview on hover
- [ ] Advanced search operators
- [ ] Search history (local)
- [ ] Custom themes
- [ ] Dark/light mode toggle
- [ ] Multi-language support
- [ ] Result clustering
- [ ] Source credibility scoring

## Contributing
Contributions welcome! Please submit PRs to improve:
- Spam detection accuracy
- UI/UX improvements
- Performance optimizations
- Feature additions

## License
AGPL-3.0 (same as SearXNG)

