# 📱 Creating a Framework for Static Analysis of Vulnerabilities in Android Applications

![Static Analysis](https://img.shields.io/badge/Security-Android%20Vulnerability%20Detection-critical?style=for-the-badge&color=red)
![Language](https://img.shields.io/badge/Written%20In-Python-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Containerized-Docker-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Project%20Status-Completed-brightgreen?style=for-the-badge)


---

## 🧠 Overview

This project focuses on building a **robust framework for static analysis** of Android applications to detect potential security vulnerabilities. It leverages tools like **AndroGuard** and integrates custom Python logic to scan APKs for issues, providing a report that assists developers and security researchers in securing mobile apps.

> ⚠️ The goal: **To create an automated, efficient, and extensible static analysis framework for Android apps.**

---

## 🚀 Features

- **Static Analysis**: Scan Android APKs for vulnerabilities using Androguard.
- **Interactive Reports**: Get detailed reports of vulnerabilities.
- **Visualization**: View vulnerabilities through intuitive charts and graphs.
- **Easy Setup**: Run the application with Docker or build it locally.
- **Upload & Process**: Upload APK files for analysis and automatically generate results.

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| **Python** | Core scripting and automation |
| **AndroGuard** | Static analysis engine |
| **Kali Linux** | Development environment |
| **Shell scripting** | Automation of scan flows |
| **Git & GitHub** | Version control and collaboration |

---

## 📂 Project Structure

```bash
static-analysis-vinay/
│
├── venv/                   # Python virtual environment
├── scripts/                # Custom scripts for automation
├── results/                # Scan results (PDF, JSON, etc.)
├── sample_apks/            # Test APK files
├── README.md               # You're here!
└── main.py                 # Main controller script


```
## 🐳 **Run with Docker**

The easiest way to run the framework is by using the pre-built Docker image. This eliminates the need for setup and dependency management.

### 📥 **Pull the Docker Image**

```bash
docker pull vinu890/apk-analyzer:02
```

### ▶️ **Run the Container**
```bash
docker run -p 5000:5000 vinu890/apk-analyzer:02
```
Access the App: After running the container, the application will be accessible at http://localhost:5000.

### 📄 **How to Use**

**Upload APK Files**
Navigate to the web interface and upload the APK files you want to analyze.

**Analysis Begins**
The framework uses Androguard to perform static analysis on the uploaded APK files. This includes detecting security vulnerabilities and generating detailed results.

**View Reports & Visualizations**
After the analysis, view the vulnerability reports and visualizations. Graphical representations of vulnerabilities will be displayed, such as charts of findings categorized by type and severity.

### 📋 **License**

[MIT](https://choosealicense.com/licenses/mit/)

## 📞 **Contact**

If you have any questions, feel free to open an issue or reach out to me directly:

- GitHub: https://github.com/vinaypatil-132

- Email: vinaycp50@gmail.com

