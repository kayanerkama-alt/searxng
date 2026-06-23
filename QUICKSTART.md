# Quick Start Guide - SearXNG Enhanced

## 🚀 Get Started in 5 Minutes

### Option 1: Local Development

```bash
# 1. Clone repository
git clone https://github.com/kayanerkama-alt/searxng.git
cd searxng
git checkout sandbox/1cf1a314-25ad-4bac-81be--3gm2

# 2. Install dependencies
pip install -r requirements.txt -r requirements-server.txt
pip install -e .

# 3. Run application
granian --interface wsgi --host 0.0.0.0 --port 8080 searx.webapp:app

# 4. Open browser
# Visit: http://localhost:8080
```

### Option 2: Docker

```bash
# 1. Build image
docker build -t searxng-enhanced .

# 2. Run container
docker run -p 8080:8080 searxng-enhanced

# 3. Open browser
# Visit: http://localhost:8080
```

### Option 3: Railway (Recommended)

1. Go to https://railway.app
2. Create new project
3. Connect GitHub repository
4. Select branch: `sandbox/1cf1a314-25ad-4bac-81be--3gm2`
5. Click "Deploy"
6. Wait for build to complete
7. Access via provided URL

## 🎨 Using Themes

### Dark Mode
```
https://your-instance.com/?theme=dark
```

### Light Mode
```
https://your-instance.com/?theme=light
```

### Auto Mode (System Preference)
```
https://your-instance.com/?theme=auto
```

## 🔍 API Examples

### Search
```bash
curl 'http://localhost:8080/search?q=python&format=json'
```

### Health Check
```bash
curl 'http://localhost:8080/health'
```

### Metrics
```bash
curl 'http://localhost:8080/metrics'
```

## 📊 Key Features

| Feature | Status | Details |
|---------|--------|---------|
| Dark/Light Themes | ✅ | Auto-switching available |
| Security Headers | ✅ | CSP, HSTS, X-Frame-Options |
| Privacy | ✅ | No tracking, no cookies |
| Caching | ✅ | Multi-level with LRU |
| Rate Limiting | ✅ | 60 req/min, 1000 req/hour |
| Monitoring | ✅ | Metrics, health checks |
| API Docs | ✅ | OpenAPI/Swagger |
| Compression | ✅ | GZIP (60-80% reduction) |

## 🔒 Security Features

✅ Content Security Policy (CSP)
✅ HTTPS Enforcement (HSTS)
✅ Clickjacking Protection
✅ XSS Protection
✅ MIME Type Sniffing Prevention
✅ No External Tracking
✅ No Third-Party Cookies
✅ Privacy-First Design

## ⚡ Performance

- **Page Load**: < 500ms
- **Search**: < 2s
- **Static Assets**: < 100ms (cached)
- **Bandwidth**: 60-80% reduction with GZIP

## 📚 Documentation

- **FEATURES.md**: Complete feature list
- **ENHANCEMENTS.md**: Technical details
- **DEPLOYMENT_GUIDE.md**: Deployment instructions
- **CHANGELOG_ENHANCEMENTS.md**: What's new

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Use different port
granian --interface wsgi --host 0.0.0.0 --port 8081 searx.webapp:app
```

### Python Version Error
```bash
# Check version (need 3.11+)
python --version

# Install correct version
python3.11 -m pip install -r requirements.txt
```

### Build Fails
```bash
# Clear cache and retry
pip cache purge
pip install -r requirements.txt -r requirements-server.txt
```

## 🎯 Next Steps

1. **Customize Settings**: Edit `searx/settings.yml`
2. **Configure Engines**: Add/remove search engines
3. **Set Theme**: Choose dark, light, or auto
4. **Monitor Performance**: Check `/metrics` endpoint
5. **Review Security**: Check security headers

## 📞 Support

- **Issues**: https://github.com/kayanerkama-alt/searxng/issues
- **Discussions**: https://github.com/kayanerkama-alt/searxng/discussions
- **Documentation**: See included .md files

## 🚀 Deploy to Production

### Railway
1. Connect GitHub repo
2. Select branch
3. Set environment variables
4. Click Deploy
5. Done!

### Docker
```bash
docker build -t searxng-enhanced .
docker run -d -p 8080:8080 searxng-enhanced
```

### Manual
```bash
pip install -r requirements.txt -r requirements-server.txt
pip install -e .
granian --interface wsgi --host 0.0.0.0 --port 8080 searx.webapp:app
```

---

**Ready to go!** 🎉

Visit your instance and enjoy a fast, private, secure search engine.

