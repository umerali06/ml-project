# Complete Hostinger Deployment Guide for Flask ML App

## Prerequisites
- Hostinger hosting account with Python support
- Access to cPanel or File Manager
- Your Flask application files ready

## Step 1: Prepare Your Files for Upload

### Files to Upload:
```
your-domain.com/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point (created for deployment)
├── requirements.txt      # Python dependencies
├── .htaccess            # Apache configuration (created for deployment)
├── templates/
│   └── index.html       # Your HTML template
├── static/
│   └── styles.css       # Your CSS file
├── dispatch_list.csv    # Your data files
├── top_50_dispatch.csv
├── synthetic_gbfs.csv
└── reference/           # Reference files (optional)
```

## Step 2: Hostinger Setup

### 2.1 Access Your Hostinger Control Panel
1. Log into your Hostinger account
2. Go to **hPanel** (Hostinger's control panel)
3. Find your domain and click **Manage**

### 2.2 Enable Python Support
1. In hPanel, go to **Advanced** → **Python**
2. Enable Python support for your domain
3. Select Python version (3.8 or higher recommended)
4. Note down the Python path (usually `/usr/bin/python3`)

### 2.3 Upload Your Files
1. Go to **File Manager** in hPanel
2. Navigate to `public_html` folder
3. Upload all your application files
4. Make sure `wsgi.py` is in the root directory

## Step 3: Configure Python Environment

### 3.1 Install Dependencies
1. In hPanel, go to **Advanced** → **Terminal**
2. Navigate to your domain directory:
   ```bash
   cd public_html
   ```
3. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### 3.2 Set Up Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Configure Web Server

### 4.1 Create Python App Configuration
1. In hPanel, go to **Advanced** → **Python**
2. Create a new Python application:
   - **App Name**: `flask-ml-app`
   - **Python Version**: 3.8+ (latest available)
   - **App Directory**: `/public_html`
   - **Startup File**: `wsgi.py`

### 4.2 Configure WSGI
The `wsgi.py` file should be configured as your startup file. Hostinger will automatically detect it.

## Step 5: Set Environment Variables

### 5.1 In hPanel Python Settings:
1. Go to **Advanced** → **Python** → **Your App**
2. Add environment variables:
   - `FLASK_DEBUG=False`
   - `FLASK_ENV=production`
   - `PORT=5000` (or the port assigned by Hostinger)

## Step 6: Test Your Deployment

### 6.1 Check Application Status
1. In hPanel Python section, check if your app is running
2. Look for any error messages in the logs

### 6.2 Access Your Application
1. Visit your domain: `https://yourdomain.com`
2. Test all functionality:
   - Load the dashboard
   - Run ML simulation
   - Download CSV files
   - Check charts and visualizations

## Step 7: Troubleshooting Common Issues

### Issue 1: Application Not Loading
**Solution:**
- Check if `wsgi.py` is in the root directory
- Verify Python version compatibility
- Check error logs in hPanel

### Issue 2: Import Errors
**Solution:**
- Ensure all dependencies are installed
- Check Python path configuration
- Verify file permissions

### Issue 3: Static Files Not Loading
**Solution:**
- Check `.htaccess` configuration
- Verify static file paths
- Ensure proper file permissions

### Issue 4: ML Libraries Not Working
**Solution:**
- Install scikit-learn and numpy specifically
- Check Python version compatibility
- Verify memory limits

## Step 8: Performance Optimization

### 8.1 Enable Caching
The `.htaccess` file includes caching rules for static files.

### 8.2 Monitor Resource Usage
- Check CPU and memory usage in hPanel
- Monitor disk space usage
- Set up monitoring alerts if available

## Step 9: Security Considerations

### 9.1 File Permissions
Set appropriate permissions:
```bash
chmod 644 *.py
chmod 755 templates/
chmod 755 static/
chmod 644 *.csv
```

### 9.2 Environment Security
- Keep `FLASK_DEBUG=False` in production
- Don't expose sensitive data in logs
- Use HTTPS (usually enabled by default on Hostinger)

## Step 10: Maintenance

### 10.1 Regular Updates
- Keep dependencies updated
- Monitor application performance
- Check error logs regularly

### 10.2 Backup Strategy
- Regular backups of your application files
- Backup database/data files
- Test restore procedures

## Alternative Deployment Methods

### Method 1: Using Hostinger's Python App Manager
1. Create Python app in hPanel
2. Upload files via File Manager
3. Configure startup file as `wsgi.py`
4. Install dependencies via Terminal

### Method 2: Using Git Deployment (if available)
1. Push your code to a Git repository
2. Connect Hostinger to your repository
3. Enable auto-deployment

## Support and Resources

### Hostinger Support
- **Documentation**: https://support.hostinger.com/
- **Live Chat**: Available 24/7 in hPanel
- **Knowledge Base**: Search for Python/Flask deployment guides

### Application-Specific Support
- Check Flask documentation for production deployment
- Review scikit-learn compatibility with your Python version
- Monitor application logs for specific errors

## Final Checklist

- [ ] All files uploaded to `public_html`
- [ ] Python support enabled
- [ ] Dependencies installed
- [ ] WSGI configuration set up
- [ ] Environment variables configured
- [ ] Application tested and working
- [ ] Security settings applied
- [ ] Performance monitoring enabled
- [ ] Backup strategy implemented

## Expected Results

After successful deployment, you should have:
- A working Flask ML dashboard accessible via your domain
- Interactive charts and visualizations
- ML simulation functionality
- CSV download capabilities
- Responsive design on all devices
- Fast loading times with proper caching

Your Mini AI Pilot simulation dashboard will be live and accessible to users worldwide!
