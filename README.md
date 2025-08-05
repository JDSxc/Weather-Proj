A simple single-page web application for displaying the current weather and 8-day forecast for a given location (based on Country, State, and City). 
Defaults to San Antonio, TX, US, if no input is provided. Location and Weather data are provided via Open Weather Map and Open-Meteo API's, respectively.

Powered by Google Cloud and Google App Engine.

Set up and use the project:
1. Create project folder 
2. Clone the repository into the project folder:
```git clone https://github.com/JDSxc/Weather-Proj.git```
4. Create a virtual environment in PowerShell or CMD:
```python -m venv venv```
5. Activate the virtual environment:
```.\venv\Scripts\Activate``` (in PowerShell)
```venv\Scripts\activate.bat``` (in CMD)
6. If the venv is activated, the terminal should show ```(venv)``` in front of the directory path
7. If you get a message saying "running scripts is disabled", run ```Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
``` and then try ```.\venv\Scripts\Activate.ps1```
8. Install dependencies within the virtual environment:
```pip install -r reqirements.txt```
9. Create a .env file in within the root of the project folder and populate the following API keys:
```OWM_API_KEY=```
```GROQ_API_KEY=```
10. Run the web app locally using the development server:
```python main.py``` (end with ```CTRL+C```)
11. Access the web app remotely (providing input to the text field in the upper right-hand corner):
[https://elegant-canto-467120-n6.uc.r.appspot.com/](https://elegant-canto-467120-n6.uc.r.appspot.com/)
