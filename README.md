# Python Weather App — Docker & Kubernetes

A simple weather web application built with **Python and Flask** that displays the current Indian Standard Time (IST) and current weather conditions for a city entered by the user.

The application uses the free [Open-Meteo API](https://open-meteo.com/) and is containerized with Docker, uploaded to Docker Hub, and deployed as a Kubernetes Pod.

## Features

* Displays current time in IST.
* Retrieves current weather for a user-entered city.
* Shows temperature, feels-like temperature, humidity, wind speed, and weather conditions.
* Uses Flask for the web interface.
* Containerized using Docker.
* Supports deployment on Kubernetes.
* Supports application log monitoring using `kubectl logs`.

## Tech Stack

* Python
* Flask
* Requests
* Open-Meteo API
* Docker
* Docker Hub
* Kubernetes
* YAML

## Project Structure

```text
weather-app/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── k8s-pod.yaml
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-app.git
cd weather-app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app/main.py
```

Open your browser at:

http://localhost:5000

Enter a city name to view its current weather.

## Build and Run with Docker

### 1. Build the Docker image

```bash
docker build -t weather-app:1.0 .
```

### 2. Run the container

```bash
docker run -d --name weather-test -p 5000:5000 weather-app:1.0
```

### 3. View container logs

```bash
docker logs weather-test
```

Open http://localhost:5000 to access the application.

## Push Image to Docker Hub

Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.

```bash
docker login
docker tag weather-app:1.0 YOUR_DOCKERHUB_USERNAME/weather-app:1.0
docker push YOUR_DOCKERHUB_USERNAME/weather-app:1.0
```

## Deploy on Kubernetes

Update the image field in `k8s-pod.yaml` with your Docker Hub image:

```yaml
image: YOUR_DOCKERHUB_USERNAME/weather-app:1.0
```

Apply the Kubernetes Pod configuration:

```bash
kubectl apply -f k8s-pod.yaml
```

Check the Pod status:

```bash
kubectl get pods
kubectl describe pod weather-app-pod
```

### Access the application

Forward the Pod's port to your local machine:

```bash
kubectl port-forward pod/weather-app-pod 5000:5000
```

Open http://localhost:5000 in your browser.

### Monitor Kubernetes logs

Display application logs:

```bash
kubectl logs weather-app-pod
```

Follow logs continuously:

```bash
kubectl logs -f weather-app-pod
```

## Configuration

* **Application port:** 5000
* **Time zone:** Asia/Kolkata (IST)
* **Weather provider:** Open-Meteo
* **API key:** Not required
* **Deployment:** Kubernetes Pod

An internet connection is required to retrieve weather data.

## Learning Objectives

This project demonstrates the fundamentals of:

* Building a Python web application.
* Managing Python dependencies.
* Creating Docker images and containers.
* Publishing container images to Docker Hub.
* Deploying applications using Kubernetes YAML.
* Accessing applications through port forwarding.
* Troubleshooting applications using container and Kubernetes logs.

## Future Improvements

* Add a Kubernetes Deployment and Service.
* Improve weather descriptions and error handling.
* Add automated testing and CI/CD using GitHub Actions.
* Add a weather forecast for upcoming days.

## License

This project is available for learning and educational purposes. Add a license file if you intend to distribute it under specific terms.
