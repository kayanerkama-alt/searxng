# Atomic Search - Phase 1 Changelog

## Overview
Atomic Search is a modern rebrand of SearXNG with enhanced privacy, performance, and user experience.

## Phase 1: Stabilization & Rebrand (Complete)

### 🎨 UI/UX Improvements
- **New Modern Theme**: Atomic theme with clean, minimalist design
- **Theme Variants**: 
  - Atomic (Modern) - Default with rounded corners and shadows
  - Atomic Dark - Dark mode optimized for night use
  - Atomic Minimal - Minimal design with no shadows
  - Atomic Compact - Space-efficient compact layout
- **Responsive Design**: Mobile-first approach, works on all devices
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation
- **Performance**: Optimized CSS with minimal file size

### 🔒 Privacy Enhancements
- **Privacy Headers**: Comprehensive HTTP security headers
  - Referrer-Policy: no-referrer
  - Permissions-Policy: Blocks geolocation, microphone, camera
  - CSP: Content Security Policy for XSS protection
  - HSTS: Strict Transport Security
- **Query Sanitization**: Removes PII from search queries
- **IP Hashing**: Anonymizes IP addresses
- **Image Proxy**: Prevents referrer leaks
- **Secure Cookies**: HttpOnly, Secure, SameSite=Strict
- **No Tracking**: Zero analytics, zero profiling

### ⚡ Performance Optimizations
- **Performance Monitoring**: Built-in performance metrics
- **Query Optimization**: Removes extra whitespace, limits length
- **Caching**: Result caching with configurable TTL
- **Connection Pooling**: Efficient HTTP connection management
- **Compression**: Gzip and Brotli support
- **Lazy Loading**: Images load on demand
- **Service Worker**: Offline support and caching

### ✨ New Features
1. **Advanced Search Filters**
   - Date range filtering
   - Result type filtering (news, images, videos, documents)
   - Language selection
   - Region selection

2. **Search Suggestions**
   - Autocomplete from multiple sources
   - Wikipedia suggestions
   - DuckDuckGo suggestions
   - Google suggestions

3. **Quick Actions**
   - Calculator: `2+2` → instant result
   - Unit Converter: `100 km to mi`
   - Currency Converter: `100 USD to EUR`
   - Weather: `weather London`

4. **Accessibility Features**
   - High contrast mode
   - Large text mode
   - Dyslexia-friendly font option
   - Keyboard shortcuts (/, j, k, o)
   - Screen reader support

5. **Search History** (Client-side only)
   - Local storage of search history
   - 30-day auto-deletion
   - No server-side tracking

6. **Result Enhancements**
   - Result metadata and timestamps
   - Source reliability indicators
   - Content type detection
   - Result previews

### 🔧 Technical Improvements
- **Code Organization**: New modules for features
  - `privacy_hardening.py`: Privacy features
  - `performance_optimization.py`: Performance monitoring
  - `atomic_features.py`: New features
- **Error Handling**: Improved error messages
- **Logging**: Better logging for debugging
- **Configuration**: Centralized feature configuration

### 📱 Mobile Optimization
- Touch-friendly buttons and inputs
- Optimized for small screens
- Fast loading on slow connections
- Reduced data usage

### 🌍 Internationalization
- Support for 50+ languages
- RTL language support
- Locale-specific formatting
- Auto-detection of user language

### 📊 Branding Changes
- Renamed from SearXNG to Atomic Search
- New logo: ⚛ (Atomic symbol)
- Updated instance name throughout
- New color scheme (Primary: #0066ff)
- Modern typography

### 🔐 Security Hardening
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security enabled
- Cross-Origin policies configured
- CSP headers for XSS prevention

### 📈 Performance Metrics
- Faster page load times
- Reduced CSS file size
- Optimized JavaScript
- Efficient caching strategy
- Connection pooling

## Files Added/Modified

### New Files
- `searx/privacy_hardening.py` - Privacy features
- `searx/performance_optimization.py` - Performance monitoring
- `searx/atomic_features.py` - New features
- `searx/static/themes/atomic/style.css` - Main theme CSS
- `searx/static/themes/atomic/dark.css` - Dark theme variant
- `searx/static/themes/atomic/minimal.css` - Minimal theme variant
- `searx/static/themes/atomic/compact.css` - Compact theme variant
- `searx/templates/atomic/base.html` - Base template
- `searx/templates/atomic/index.html` - Home page
- `searx/templates/atomic/results.html` - Results page
- `searx/templates/atomic/preferences.html` - Preferences page

### Modified Files
- `searx/brand.py` - Updated branding
- `searx/settings_defaults.py` - Updated instance name
- `searx/webapp.py` - Added privacy headers integration
- `searx/__init__.py` - Updated references

## Compatibility
- Python 3.8+
- All modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Accessibility: WCAG 2.1 AA

## Known Limitations
- Some features require JavaScript
- Offline mode limited without Service Worker
- Some quick actions require external APIs

## Future Improvements (Phase 2+)
- 20+ additional themes
- Advanced result ranking
- Custom search operators
- Browser extensions
- Mobile app
- Advanced analytics (privacy-respecting)
- AI-powered search suggestions
- Multi-language support improvements
- Dark mode auto-detection
- Custom color schemes

## Contributing
Contributions are welcome! Please see CONTRIBUTING.rst for guidelines.

## License
AGPL-3.0-or-later

## Support
- Documentation: https://docs.searxng.org
- Issues: https://github.com/kayanerkama-alt/searxng/issues
- Community: https://matrix.to/#/#searxng:matrix.org

