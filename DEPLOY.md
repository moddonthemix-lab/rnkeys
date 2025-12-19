# Deploying RNKeys to Railway

## Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## Step-by-Step Deployment

### 1. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### 2. Deploy from GitHub

**Option A: Use Railway Button**
1. Click the "Deploy on Railway" button above
2. Connect your GitHub repository
3. Railway will automatically detect the configuration and deploy

**Option B: Manual Deploy**
1. Go to [railway.app/new](https://railway.app/new)
2. Click "Deploy from GitHub repo"
3. Select your `rnkeys` repository
4. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Run the app using `gunicorn app:app`

### 3. Get Your URL

Once deployed:
1. Go to your Railway project dashboard
2. Click on your deployment
3. Go to "Settings" tab
4. Under "Domains", click "Generate Domain"
5. Your app will be available at: `https://your-app-name.up.railway.app`

### 4. Environment Variables (Optional)

If you need to set any environment variables:
1. Go to "Variables" tab
2. Add variables like:
   - `PORT` (automatically set by Railway)
   - `FLASK_ENV=production`

## Deployment Configuration Files

This repository includes:
- `Procfile` - Tells Railway how to run the app
- `railway.json` - Railway-specific configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies

## Using the Deployed App

Once deployed, visit your Railway URL to:
1. Generate 90s R&B MIDI patterns
2. Download MIDI files directly
3. Choose different styles and settings
4. Export separate tracks

## Custom Domain (Optional)

To use your own domain:
1. Go to Railway project settings
2. Click "Domains"
3. Add your custom domain
4. Update your DNS settings as shown

## Troubleshooting

### Build Fails
- Check that all files are committed to GitHub
- Verify `requirements.txt` is correct
- Check Railway logs for errors

### App Won't Start
- Ensure `Procfile` is correct
- Check that `gunicorn` is in `requirements.txt`
- Verify app.py exists and is correct

### Memory Issues
- Railway free tier has memory limits
- Consider upgrading plan if generating many patterns
- Files auto-cleanup after 1 hour

## Free Tier Limits

Railway free tier includes:
- $5 credit per month
- 512 MB RAM
- 1 GB storage
- Unlimited projects

This is enough for moderate RNKeys usage!

## Monitoring

View your app's:
- Logs: Railway dashboard → Logs tab
- Metrics: CPU, Memory usage
- Deployments: History of all deploys

## Updates

To update your deployed app:
1. Make changes to your code
2. Commit and push to GitHub
3. Railway automatically redeploys

## Support

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- RNKeys Issues: GitHub Issues page

---

**Your 90s R&B beat generator is now live!** 🎵🔥
