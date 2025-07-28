# 🌍 Climate Platform - Windows Setup Guide

## Prerequisites

1. **Python 3.11+** - Download from [python.org](https://python.org)
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Check "Install pip" during installation

2. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org)
   - ✅ This will also install npm

3. **Git** (optional) - Download from [git-scm.com](https://git-scm.com)

## Quick Start Commands

### Option 1: Automated Setup
\`\`\`cmd
# Run the automated setup script
setup_windows.bat
\`\`\`

### Option 2: Manual Setup

#### Backend Setup
\`\`\`cmd
# Navigate to backend directory
cd backend

# Run the development script
run_dev.bat
\`\`\`

#### Frontend Setup (New Command Prompt)
\`\`\`cmd
# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

## Verification Steps

1. **Backend Health Check**
   \`\`\`cmd
   curl http://127.0.0.1:5000/api/health
   \`\`\`

2. **Test Weather API**
   \`\`\`cmd
   curl "http://127.0.0.1:5000/api/weather/predictions?location=New York"
   \`\`\`

3. **Frontend Access**
   - Open browser to: http://localhost:3000

## Troubleshooting

### Python Issues
- **Error**: `'python' is not recognized`
  - **Solution**: Reinstall Python and check "Add to PATH"
  - **Alternative**: Use `py` instead of `python`

### Pandas Installation Error
- **Error**: Meson build system error
  - **Solution**: Install Visual Studio Build Tools
  - **Download**: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Port Already in Use
- **Error**: Port 5000 or 3000 already in use
  - **Solution**: Kill existing processes or change ports
  \`\`\`cmd
  netstat -ano | findstr :5000
  taskkill /PID <PID_NUMBER> /F
  \`\`\`

### API Key Issues
- **Error**: API calls failing
  - **Solution**: Check `.env` file in backend directory
  - **Verify**: All API keys are properly configured

## Your API Keys Status

✅ **OpenWeather**: Configured  
✅ **Carbon Interface**: Configured  
✅ **OpenAQ**: Configured  
✅ **Tomorrow.io**: Configured  
✅ **AirVisual**: Configured  
✅ **Telegram Bot**: Configured  

## Platform URLs

- **Backend API**: http://127.0.0.1:5000
- **Frontend**: http://localhost:3000
- **API Health**: http://127.0.0.1:5000/api/health
- **API Documentation**: http://127.0.0.1:5000/docs

## Next Steps

1. ✅ Run setup commands
2. ✅ Verify all services are running
3. ✅ Test API endpoints
4. ✅ Access frontend dashboard
5. ✅ Start analyzing climate data!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure API keys are configured correctly
4. Check Windows Defender/Firewall settings
