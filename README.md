# 📅 Calendar Automation App

## Motivation 

I track my daily activities on my Google calendar and keep it updated. I used to perform weekly analysis on this data manually, and suggest changes for time management/ optimization. I decided to automate this process. 
This project has 3 parts to it: 
1. Data Collection - Collecting data and storing it locally (done)
2. Analysis - Performing daily analysis and track key metrics over time 
3. Suggestions - Using historical data, provides recommendations to optimize time management (in progress)

## 🚀 Prerequisites

### 1️⃣ Setting Up OAuth 2.0 Credentials

Follow these steps to configure OAuth 2.0 credentials and download the necessary `credentials.json` file:

#### 🔹 Access Google Cloud Console:
- Navigate to the [Google Cloud Console](https://console.cloud.google.com/).

#### 🔹 Create or Select a Project:
- Use the project selector at the top of the page to either create a new project or select an existing one.

#### 🔹 Enable the Google Calendar API:
1. Navigate to **API & Services** > **Library**.
2. Search for **Google Calendar API**.
3. Click on **Google Calendar API** and select **Enable**.

#### 🔹 Create OAuth 2.0 Client ID:
1. Go to **API & Services** > **Credentials**.
2. Click **Create Credentials** and select **OAuth 2.0 Client ID**.
3. If prompted, configure the consent screen by providing the necessary application details.
4. Choose **Desktop App** as the application type.
5. Click **Create** and download the `credentials.json` file.
6. Save the file in the base directory and rename it to `credentials.json`.

---

## 📦 Installing Dependencies

Before running the application, ensure all required dependencies are installed by running:

```sh
pip install -r requirements.txt
```

---

## 🔧 Running the Scripts

The following scripts are required to set up and update credentials:

- **01_create_id.py** – Initializes and creates OAuth credentials.
- **02_google_auth.py** – Handles authentication and token generation.

To fetch calendar data and save it as a CSV file in the directory, run:

```sh
python 03_google_cal_to_csv.py
```

This will retrieve events from the last 7 days up to the current time and store them in a CSV file.

---

## 🤖 Automating the Process

### 🖥️ For macOS Users

To automate the script execution on macOS, **LaunchD** is used. Follow these steps:

1. Retrieve your user ID by running:

   ```sh
   id -u
   ```

   This will return a number (e.g., `501` or `502`), referred to as `xxx` in the following commands.

2. Load the LaunchD plist file:

   ```sh
   launchctl bootstrap gui/xxx scripts/com.google.cal2csv.plist
   ```
   
   Alternatively, use the absolute path of the plist file.

3. Start the scheduled task:

   ```sh
   launchctl kickstart gui/xxx/com.google.cal2csv
   ```

4. Verify the job status:

   ```sh
   launchctl list | grep com.google.cal2csv
   ```

   If successful, you should see output in three columns, indicating the job is running (e.g., `0 com.google.cal2csv`).

### 🖥️ For Windows Users

Cron jobs work fine on Windows. To schedule the script to run daily at 9 PM and store logs, open the crontab by running:

```sh
crontab -e
```

Then, add the following line:

```sh
0 21 * * * python /path/to/03_google_cal_to_csv.py >> /path/to/scripts/log/out.log 2>> /path/to/scripts/log/error.log
```

Replace `/path/to/` with the absolute path to your script directory. Save the file by typing `:wq` and exiting.

To verify that the job is scheduled, list active cron jobs by running:

```sh
crontab -l
```

### 📝 Debugging and Logs

Log files are automatically created in a subfolder named `logs` within the `scripts` directory. Check these logs for any issues related to the automation process.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🤝 Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue for any improvements or bug fixes.

---

## 📧 Contact
For any queries or support, feel free to reach out via **GitHub Issues** or email.

