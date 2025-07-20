# Coffee Bean Roast Level Detector

This project is a web application that uses a YOLOv5 model to detect the roast level of coffee beans from uploaded images. The application consists of a frontend (HTML/JavaScript) hosted on GitHub Pages and a backend (FastAPI with YOLOv5) hosted on Azure Web Apps.

## Project Structure
```
coffee-bean-detector/
├── frontend/
│   ├── index.html        # Frontend HTML/JavaScript
├── backend/
│   ├── main.py           # FastAPI backend code
│   ├── best.pt           # Trained YOLOv5 model
│   ├── requirements.txt  # Backend dependencies
│   ├── yolov5/           # Cloned YOLOv5 repository
├── .github/
│   ├── workflows/
│   │   ├── main_coffee-bean-detector-api.yml  # GitHub Actions for Azure deployment
├── .gitignore            # Git ignore file
├── README.md             # This file
```

## Features
- **Frontend**: A simple web interface for uploading coffee bean images and displaying roast level predictions with annotated images.
- **Backend**: A FastAPI server that processes images using a trained YOLOv5 model (`best.pt`) and returns detection results.
- **Hosting**: Frontend on GitHub Pages (free static hosting) and backend on Azure Web Apps (Free tier).

## Prerequisites
- **Git**: For cloning and pushing to GitHub (https://git-scm.com/downloads).
- **Python ≥3.8**: For running the backend (https://www.python.org/downloads/).
- **Azure CLI**: For deploying to Azure Web Apps (https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
- **Azure Account**: Free tier account (https://azure.microsoft.com/free/).
- **GitHub Account**: For hosting the repository and frontend.

## Setup Instructions

### Local Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/coffee-bean-detector.git
   cd coffee-bean-detector
   ```

2. **Set Up Backend**
   Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install fastapi uvicorn pillow
   ```
   Ensure `best.pt` is in the `backend/` folder. If not, update the path in `main.py`.

3. **Test Backend Locally**
   Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   Access `http://localhost:8000/docs` to test the `/health`, `/detect`, and `/detect-image` endpoints.

4. **Test Frontend Locally**
   Serve `frontend/index.html` using a local server (e.g., Python’s HTTP server):
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Access `http://localhost:8080` and test image uploads (update `apiUrl` in `index.html` to `http://localhost:8000`).

### Deployment

#### Frontend (GitHub Pages)
1. **Configure GitHub Pages**
   - Go to **Settings > Pages** in your GitHub repository.
   - Set **Source** to `main` and **Folder** to `/frontend`.
   - Save, and the frontend will be available at `https://<your-username>.github.io/coffee-bean-detector`.

2. **Update API URL**
   Update `frontend/index.html` with the deployed backend URL (e.g., `https://coffee-bean-detector-api.azurewebsites.net`):
   ```javascript
   const apiUrl = "https://coffee-bean-detector-api.azurewebsites.net";
   ```
   Commit and push:
   ```bash
   git add frontend/index.html
   git commit -m "Update API URL"
   git push origin main
   ```

#### Backend (Azure Web Apps)
1. **Log in to Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name myResourceGroup --location eastus
   ```

3. **Create App Service Plan (Free Tier)**
   ```bash
   az appservice plan create --name myAppServicePlan --resource-group myResourceGroup -- SKU F1 --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create --resource-group myResourceGroup --plan=myAppServicePlan --name coffee-bean-detector-api --runtime "PYTHON|3.8"
   ```

5. **Configure Deployment**
   - In the Azure Portal, go to **Deployment Center** for `coffee-bean-detector-api`.
   - Select **GitHub**, authenticate, and choose your repository (`coffee-bean-detector`) and branch (`main`).
   - Set **Path** to `backend` to deploy only the backend folder.
   - Save, and Azure will create a GitHub Actions workflow (`.github/workflows/main_coffee-bean-detector-api.yml`).

6. **Set Startup Command**
   ```bash
   az webapp config set --resource-group myResourceGroup --name coffee-bean-detector-api --startup-file "uvicorn main:app --host 0.0.0.0 --port 8000"
   ```

7. **Enable Build Automation**
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name coffee-bean-detector-api --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
   ```

8. **Verify Deployment**
   - Push changes to trigger deployment:
     ```bash
     git add .
     git commit -m "Deploy backend to Azure"
     git push origin main
     ```
   - Check GitHub Actions logs and test the API at `https://coffee-bean-detector-api.azurewebsites.net/docs`.

## Usage
1. Open the frontend at `https://<your-username>.github.io/coffee-bean-detector`.
2. Upload a coffee bean image.
3. View the roast level predictions and annotated image returned by the backend.

## Troubleshooting
- **Backend Errors**: Check logs with `az webapp log tail --resource-group myResourceGroup --name coffee-bean-detector-api`.
- **CORS Issues**: Ensure `backend/main.py` allows your GitHub Pages URL (e.g., `origins=["https://<your-username>.github.io"]`).
- **Resource Limits**: Azure Free tier (F1) has 60 CPU minutes/day. Monitor usage in the Azure Portal (**Metrics**).
- **Model Performance**: If slow, use a smaller YOLOv5 model (e.g., `yolov5s.pt`) or upgrade to a paid tier.

## Contributing
Feel free to submit issues or pull requests to improve the project. Ensure changes are tested locally before pushing.

## License
This project is licensed under the MIT License.

## Resources
- [YOLOv5 Documentation](https://docs.ultralytics.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/)
- [GitHub Pages](https://docs.github.com/en/pages)