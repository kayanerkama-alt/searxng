# Atomic Search - Setup & Installation Guide

## Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kayanerkama-alt/searxng.git
cd searxng
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-server.txt
```

3. **Initialize settings**
```bash
cp container/settings.template.yml settings.yml
```

4. **Run the application**
```bash
python -m searx.webapp
```

The application will be available at `http://localhost:8888`

## Configuration

### Basic Settings
Edit `settings.yml`:

```yaml
general:
  instance_name: "Atomic Search"
  debug: false
  enable_metrics: true

ui:
  default_theme: "atomic"
  default_locale: "en"
  theme_args:
    simple_style: "auto"

server:
  port: 8888
  bind_address: "127.0.0.1"
  secret_key: "your-secret-key-here"
```

### Privacy Settings
```yaml
server:
  image_proxy: true
  public_instance: false

outgoing:
  verify: true
  enable_http2: true
```

### Performance Settings
```yaml
search:
  autocomplete: "duckduckgo"
  autocomplete_min: 4
  ban_time_on_fail: 5
  max_ban_time_on_fail: 120
```

## Theme Selection

### Available Themes
1. **atomic** - Modern default theme
2. **atomic-dark** - Dark mode variant
3. **atomic-minimal** - Minimal design
4. **atomic-compact** - Space-efficient
5. **atomic-google** - Google-inspired
6. **atomic-kagi** - Kagi-inspired
7. **atomic-nord** - Nord color palette
8. **atomic-dracula** - Dracula color palette

### Changing Theme
In `settings.yml`:
```yaml
ui:
  default_theme: "atomic-dark"
```

Or in user preferences at `/preferences`

## Docker Deployment

### Build Docker Image
```bash
docker build -t atomic-search .
```

### Run Docker Container
```bash
docker run -p 8888:8888 \
  -e SEARXNG_SECRET="your-secret-key" \
  -e SEARXNG_BIND_ADDRESS="0.0.0.0" \
  atomic-search
```

### Docker Compose
```yaml
version: '3'
services:
  atomic-search:
    image: atomic-search
    ports:
      - "8888:8888"
    environment:
      SEARXNG_SECRET: "your-secret-key"
      SEARXNG_BIND_ADDRESS: "0.0.0.0"
    volumes:
      - ./settings.yml:/etc/searx/settings.yml
```

## Railway Deployment

### Prerequisites
- Railway account
- GitHub repository

### Steps

1. **Connect GitHub Repository**
   - Go to Railway dashboard
   - Create new project
   - Connect your GitHub repo

2. **Configure Environment Variables**
   ```
   SEARXNG_SECRET=your-secret-key
   SEARXNG_BIND_ADDRESS=0.0.0.0
   SEARXNG_PORT=8080
   ```

3. **Set Build Command**
   ```
   pip install -r requirements.txt && pip install -r requirements-server.txt
   ```

4. **Set Start Command**
   ```
   python -m searx.webapp
   ```

5. **Configure Health Check**
   - Path: `/healthz`
   - Timeout: 30s

6. **Deploy**
   - Push to main branch
   - Railway will automatically deploy

## Development

### Setup Development Environment
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linter
pylint searx/

# Format code
black searx/
```

### Running in Development Mode
```bash
export SEARXNG_DEBUG=1
python -m searx.webapp
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in settings.yml
server:
  port: 8889
```

### Module Not Found
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Theme Not Loading
```bash
# Check theme directory exists
ls -la searx/static/themes/atomic/
ls -la searx/templates/atomic/
```

### Performance Issues
```yaml
# Increase cache TTL
search:
  ban_time_on_fail: 10
  max_ban_time_on_fail: 300

# Enable compression
server:
  enable_gzip: true
```

## Security Hardening

### HTTPS Setup
```yaml
server:
  base_url: "https://your-domain.com"
  secret_key: "generate-strong-key"
```

### Rate Limiting
```yaml
server:
  limiter: true
  public_instance: false
```

### CORS Configuration
```yaml
server:
  default_http_headers:
    X-Content-Type-Options: "nosniff"
    X-Frame-Options: "DENY"
    X-XSS-Protection: "1; mode=block"
```

## Monitoring

### Health Check
```bash
curl http://localhost:8888/healthz
```

### Metrics
```bash
curl http://localhost:8888/stats
```

### Logs
```bash
# View application logs
tail -f logs/searx.log
```

## Updating

### Update from GitHub
```bash
git pull origin master
pip install --upgrade -r requirements.txt
```

### Database Migration
```bash
python manage migrate
```

## Support

- **Documentation**: https://docs.searxng.org
- **Issues**: https://github.com/kayanerkama-alt/searxng/issues
- **Community**: https://matrix.to/#/#searxng:matrix.org

## License
AGPL-3.0-or-later

