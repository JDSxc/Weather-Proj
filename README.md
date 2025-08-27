# 🌤️ Nimbus – Your Weather App, But Cooler

**Nimbus** is a single-page web application that displays the current weather and 8-day forecast for any user-provided location. It supports natural language input, renders temperature trend charts, and displays the local time based on the city queried.

> **Default Location:** San Antonio, TX, US (if no input is provided)

---

## 🔗 Live Demo & Source Code

- 🌐 **Live App:** [https://elegant-canto-467120-n6.uc.r.appspot.com/](https://elegant-canto-467120-n6.uc.r.appspot.com/) (no longer working)
- 📂 **GitHub Repository:** [https://github.com/JDSxc/Weather-Proj](https://github.com/JDSxc/Weather-Proj)

---

## 🚀 Setup Instructions (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/JDSxc/Weather-Proj.git
cd Weather-Proj
```
### 2. Create and Activate Virtual Environment
in PowerShell
```PowerShell
python -m venv venv
.\venv\Scripts\Activate
```
or in CMD
```CMD 
python -m venv venv
venv\Scripts\activate.bat
```
If activation is blocked, run:
```Set-ExecutionPolicy RemoteSigned -Scope CurrentUser```
Then try activating again.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Add your API keys
Create a .env file in the project root:
```
OWM_API_KEY=your_openweathermap_key
GROQ_API_KEY=your_groq_api_key (optional)
```
### 5. Run the application locally

```
python3 main.py
```
Then open your browser to:
```
http://127.0.0.1:8080/
```


## 🛠️ Tech Stack
- Backend: Flask, Python 3.12, Jinja2
- Frontend: HTML, CSS, JS
- APIs: Groq (LLM), OpenWeatherMap, Open-Meteo
- Graphing: Matplotlib
- Hosting: Google Cloud App Engine
- Secrets Management: dotenv (local), Google Cloud Secret Manager (prod)
## 📄 License
- This project is open-source. Feel free to fork, modify, and use it.

## 👤 Author
Developed by [JDSxc](https://github.com/JDSxc), [Jaime1108](https://github.com/Jaime1108) and [NamNguyenUTSA](https://github.com/NamNguyenUTSA)
