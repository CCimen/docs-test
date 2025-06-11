# Deployment Configuration Files

This directory contains production-ready deployment configurations for Eneo.

---

## 📁 File Overview

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Production Docker Compose configuration |
| `env_backend.template` | Backend environment variables template |
| `env_frontend.template` | Frontend environment variables template |
| `env_db.template` | Database environment variables template |

---

## 🚀 Quick Deployment

### 1. Copy Templates
```bash
cp env_backend.template env_backend.env
cp env_frontend.template env_frontend.env  
cp env_db.template env_db.env
```

### 2. Configure Environment Variables

**Required Configuration:**
- Replace `your-domain.com` with your actual domain
- Replace `your-email@domain.com` with your email for SSL certificates
- Add at least one AI provider API key
- Generate secure JWT secrets: `openssl rand -hex 32`
- Set secure database password

### 3. Update Docker Compose
```bash
# Edit docker-compose.yml
# Replace placeholder domain names with your actual domain
sed -i 's/your-domain.com/yourdomain.com/g' docker-compose.yml
sed -i 's/your-email@domain.com/admin@yourdomain.com/g' docker-compose.yml
```

### 4. Deploy
```bash
docker network create proxy_tier
docker compose up -d
```

---

## ⚙️ Configuration Details

### Backend Configuration (`env_backend.env`)

**Critical Settings:**
```bash
# AI Provider (at least one required)
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...

# Security (MUST be changed)
JWT_SECRET=64-character-hex-string
POSTGRES_PASSWORD=secure-database-password

# Database
POSTGRES_HOST=db
POSTGRES_DB=eneo
```

### Frontend Configuration (`env_frontend.env`)

**Critical Settings:**
```bash
# Public URLs
ORIGIN=https://yourdomain.com
INTRIC_BACKEND_URL=https://yourdomain.com

# Security (must match backend)
JWT_SECRET=same-as-backend-jwt-secret

# Internal communication
INTRIC_BACKEND_SERVER_URL=http://backend:8000
```

### Database Configuration (`env_db.env`)

**Critical Settings:**
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=same-as-backend-postgres-password
POSTGRES_DB=eneo
```

---

## 🔒 Security Considerations

### SSL Certificates
- Traefik automatically manages Let's Encrypt certificates
- Ensure domain DNS points to your server
- Certificate email must be valid for notifications

### Environment Variables
- Never commit `.env` files to version control
- Use strong, unique passwords for all services
- Rotate secrets regularly
- Restrict file permissions: `chmod 600 *.env`

### Network Security
- External network `proxy_tier` isolates services
- Only Traefik exposes ports to the internet
- Internal services communicate over Docker network

---

## 📊 Production Checklist

### Pre-Deployment
- [ ] Domain DNS configured
- [ ] SSL email configured  
- [ ] All environment variables set
- [ ] AI provider API keys tested
- [ ] Secure passwords generated
- [ ] Firewall configured (ports 80, 443)

### Post-Deployment
- [ ] All services running: `docker compose ps`
- [ ] HTTPS working with valid certificate
- [ ] Backend API responding: `curl https://yourdomain.com/version`
- [ ] Verify production uses port 8000 (not 8123 like development)
- [ ] Frontend accessible: `https://yourdomain.com`
- [ ] Default user login working
- [ ] AI assistant creation and chat working

### Ongoing Maintenance
- [ ] Regular container updates: `docker compose pull && docker compose up -d`
- [ ] Log monitoring: `docker compose logs -f`
- [ ] Backup strategy implemented
- [ ] Security updates applied

---

## 🛠️ Customization

### Domain Configuration
Update all instances of placeholder domains:
```bash
# In docker-compose.yml
traefik.http.routers.eneo-frontend.rule=Host(`your-domain.com`)
traefik.http.routers.eneo-backend.rule=Host(`your-domain.com`) && ...

# In env_frontend.env
ORIGIN=https://your-domain.com
INTRIC_BACKEND_URL=https://your-domain.com
```

### Additional AI Providers
Add more AI provider configurations in `env_backend.env`:
```bash
# Additional providers
MISTRAL_API_KEY=...
VLLM_API_KEY=...
VLLM_MODEL_URL=...
```

### Resource Limits
Add resource constraints to docker-compose.yml:
```yaml
backend:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '0.5'
```

---

## 🔧 Troubleshooting

### Common Issues

**SSL Certificate Issues:**
```bash
# Check Traefik logs
docker compose logs traefik

# Verify domain resolves to server
nslookup your-domain.com
```

**Service Startup Issues:**
```bash
# Check all service status
docker compose ps

# View specific service logs
docker compose logs backend
docker compose logs frontend
```

**Database Issues:**
```bash
# Check database initialization
docker compose logs db-init

# Access database directly
docker compose exec db psql -U postgres -d eneo
```

### Getting Help
- See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for detailed solutions
- Check [DEPLOYMENT.md](../DEPLOYMENT.md) for comprehensive deployment guide
- Contact support: digitalisering@sundsvall.se

---

This deployment configuration enables rapid, secure deployment of Eneo in production environments while maintaining the platform's democratic AI principles and public sector focus.