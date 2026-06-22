# Atomic Search - Feature Documentation

## Core Features

### 1. Privacy-First Design
- **No Tracking**: Zero analytics, zero profiling
- **No Cookies**: Minimal cookies, only for preferences
- **No Accounts**: No user registration or login
- **No Logs**: Search queries not stored
- **Encrypted**: HTTPS-only connections
- **Open Source**: Fully auditable code

### 2. Advanced Search Filters
```
Date Range:
- Last day
- Last week
- Last month
- Last year
- Custom date range

Result Types:
- All results
- News articles
- Images
- Videos
- Documents

Language:
- Auto-detect
- 50+ languages supported

Region:
- Auto-detect
- US, UK, EU, Asia, etc.
```

### 3. Quick Actions
```
Calculator:
  Input: "2+2"
  Output: 4

Unit Converter:
  Input: "100 km to mi"
  Output: 62.14 miles

Currency Converter:
  Input: "100 USD to EUR"
  Output: ~92 EUR

Weather:
  Input: "weather London"
  Output: Current weather for London
```

### 4. Search Suggestions
- Wikipedia suggestions
- DuckDuckGo suggestions
- Google suggestions
- Configurable sources
- Caching for performance

### 5. Accessibility Features
- **High Contrast Mode**: Better visibility
- **Large Text Mode**: 1.5x text scaling
- **Dyslexia-Friendly Font**: OpenDyslexic font option
- **Keyboard Navigation**: Full keyboard support
  - `/` - Focus search
  - `j` - Next result
  - `k` - Previous result
  - `o` - Open result
- **Screen Reader Support**: Full ARIA labels

### 6. Theme System
- **Atomic (Modern)**: Default theme with modern design
- **Atomic Dark**: Dark mode for night use
- **Atomic Minimal**: Minimal design
- **Atomic Compact**: Space-efficient layout
- **Auto Dark Mode**: Respects system preferences

### 7. Performance Features
- **Result Caching**: Faster repeated searches
- **Connection Pooling**: Efficient HTTP connections
- **Compression**: Gzip and Brotli support
- **Lazy Loading**: Images load on demand
- **Service Worker**: Offline support
- **Performance Monitoring**: Built-in metrics

### 8. Security Features
- **CSP Headers**: XSS protection
- **HSTS**: Secure connections
- **Referrer Policy**: No referrer leaks
- **Permissions Policy**: Blocks tracking APIs
- **Secure Cookies**: HttpOnly, Secure, SameSite
- **Query Sanitization**: Removes PII

### 9. Search History (Client-Side)
- **Local Storage**: Stored on device only
- **Auto-Deletion**: 30-day retention
- **No Sync**: Never sent to server
- **Searchable**: Quick access to past searches
- **Deletable**: Clear history anytime

### 10. Result Enhancements
- **Metadata**: Timestamp, relevance score
- **Source Info**: Engine and reliability
- **Content Type**: Webpage, PDF, image, etc.
- **Previews**: Quick preview of results
- **Snippets**: Relevant text excerpts

## Configuration

### Privacy Settings
```yaml
privacy:
  enable_image_proxy: true
  enable_referrer_policy: true
  enable_csp: true
  sanitize_queries: true
  hash_ips: true
  secure_cookies_only: true
  httponly_cookies: true
  samesite_cookies: Strict
```

### Performance Settings
```yaml
performance:
  enable_result_cache: true
  cache_ttl: 3600
  enable_gzip: true
  enable_brotli: true
  enable_http2: true
  request_timeout: 5
```

### Feature Flags
```yaml
features:
  search_filters: true
  suggestions: true
  quick_actions: true
  accessibility: true
  search_history: true
  result_enhancements: true
```

## API Endpoints

### Search
```
GET/POST /search?q=query&format=html|json|csv|rss
```

### Suggestions
```
GET /suggestions?q=query
```

### Preferences
```
GET /preferences
POST /preferences (save preferences)
```

### Health Check
```
GET /healthz
```

## Browser Support
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Benchmarks
- Page load: < 1s
- Search results: < 2s
- Suggestion response: < 500ms
- CSS size: < 50KB
- JS size: < 100KB

## Accessibility Compliance
- WCAG 2.1 AA
- Keyboard navigation
- Screen reader support
- Color contrast ratio 4.5:1
- Focus indicators
- ARIA labels

## Privacy Compliance
- GDPR compliant
- CCPA compliant
- No third-party tracking
- No data collection
- No cookies for tracking
- Transparent data handling

## Future Features (Planned)
- [ ] Advanced search operators
- [ ] Custom search engines
- [ ] Browser extensions
- [ ] Mobile app
- [ ] AI-powered suggestions
- [ ] Multi-language UI
- [ ] Custom themes
- [ ] Search analytics (privacy-respecting)
- [ ] Saved searches
- [ ] Search collections

