# Kisan Project Deployment Checklist

## Pre-deployment Checklist

- [ ] Update `SECRET_KEY` in environment variables (never use the default one in production)
- [ ] Set `DEBUG=False` in production environment
- [ ] Update `ALLOWED_HOSTS` with your domain names
- [ ] Configure database settings for production (PostgreSQL recommended)
- [ ] Set up email backend for production (SMTP, SendGrid, etc.)
- [ ] Configure static and media file storage (AWS S3, Cloudinary, etc.)
- [ ] Set up SSL/HTTPS
- [ ] Configure caching (Redis/Memcached)
- [ ] Set up logging for production
- [ ] Run security checks: `python manage.py check --deploy`

## Deployment Steps

### 1. Environment Setup
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`

### 2. Database Setup
- [ ] Configure database settings in environment variables
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Load initial data if needed

### 3. Static Files
- [ ] Collect static files: `python manage.py collectstatic --noinput`

### 4. Environment Variables
- [ ] Set `SECRET_KEY` (generate a new one)
- [ ] Set `DEBUG=False`
- [ ] Set `ALLOWED_HOSTS` (comma-separated list)
- [ ] Set database credentials
- [ ] Set email settings

### 5. Web Server Configuration
- [ ] Configure Gunicorn: `gunicorn kisan_project.wsgi:application`
- [ ] Set up reverse proxy (Nginx/Apache)
- [ ] Configure SSL certificate

### 6. Process Monitoring
- [ ] Set up process manager (systemd, supervisor, etc.)
- [ ] Configure log rotation
- [ ] Set up health checks

## Platform-Specific Deployment

### Heroku
- [ ] Create Heroku app
- [ ] Add PostgreSQL addon
- [ ] Set config vars in Heroku dashboard
- [ ] Deploy using Git: `git push heroku main`

### Render
- [ ] Use the provided `render.yaml` file
- [ ] Set environment variables in Render dashboard
- [ ] Deploy using Git

### DigitalOcean App Platform
- [ ] Connect GitHub repository
- [ ] Set environment variables
- [ ] Configure build and run commands

### AWS Elastic Beanstalk
- [ ] Install EB CLI
- [ ] Initialize application: `eb init`
- [ ] Create environment: `eb create`
- [ ] Deploy: `eb deploy`

### Manual Server Deployment
- [ ] Set up Ubuntu/Debian server
- [ ] Install Python, PostgreSQL, Nginx
- [ ] Configure Gunicorn and systemd service
- [ ] Set up domain and SSL with Let's Encrypt

## Post-deployment Checklist

- [ ] Test all pages and functionality
- [ ] Verify admin panel access
- [ ] Test user registration and login
- [ ] Verify database connections
- [ ] Test file uploads (if applicable)
- [ ] Check email functionality
- [ ] Monitor application logs
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy

## Troubleshooting

### Common Issues
1. **500 Internal Server Error**: Check logs, ensure DEBUG=False, verify environment variables
2. **Static files not loading**: Check STATIC_ROOT, run collectstatic, verify web server config
3. **Database connection errors**: Verify database credentials and connectivity
4. **Permission denied errors**: Check file permissions and ownership

### Useful Commands
```bash
# Check for deployment issues
python manage.py check --deploy

# View application logs
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Check service status
sudo systemctl status gunicorn
sudo systemctl status nginx
```

## Security Best Practices

- [ ] Use strong, unique passwords
- [ ] Keep Django and dependencies updated
- [ ] Use HTTPS everywhere
- [ ] Implement proper user authentication and authorization
- [ ] Sanitize user inputs
- [ ] Use CSRF protection
- [ ] Set secure headers
- [ ] Implement rate limiting
- [ ] Regular security audits