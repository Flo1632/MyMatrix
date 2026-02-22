# MyMatrix – Eisenhower Matrix Task Manager

A task management application built with Python and [Flet](https://flet.dev/) that helps you prioritize tasks using the **Eisenhower Matrix** (Urgent–Important Matrix). Available as both a **desktop app** and a **web app**.

---

## What is the Eisenhower Matrix?

The Eisenhower Matrix is a productivity framework that divides tasks into four quadrants based on their urgency and importance:

| Quadrant | Strategy | Description |
|---|---|---|
| 🔴 **Important & Urgent** | **Do First** | Critical tasks requiring immediate attention. Deadlines, crises, pressing problems. |
| 🔵 **Not Important, but Urgent** | **Delegate** | Pressing tasks that are actually not your responsibility. Often interruptions or others' work. |
| 🟠 **Important, but not Urgent** | **Schedule** | Long-term growth tasks. Vital for success but without an immediate deadline. |
| ⚫ **Not Important, Not Urgent** | **Eliminate** | Time-wasting activities with no real value. Minimize or remove them entirely. |

---

## Features

- ✅ Add tasks to any of the four quadrants
- ✅ Each task is automatically timestamped when created
- ✅ Check off completed tasks and remove them with one click
- ✅ Click on any quadrant to open a full detail view of its tasks
- ✅ Persistent storage – your tasks are saved and restored between sessions
- ✅ Info screen explaining each quadrant's strategy
- ✅ Responsive layout: adapts to both mobile and desktop screen sizes

---

## Tech Stack

- **Language:** Python 3
- **UI Framework:** [Flet](https://flet.dev/) (`>= 0.80.0`)
- **Persistence:** `ft.SharedPreferences`
- **Deployment:** [Render](https://render.com/) (web app)

---

## Project Structure

```
MyMatrix/
├── main_matrix_desktop.py  # Desktop application entry point
├── main_matrix_webapp.py   # Web application entry point (deployed on Render)
├── requirements.txt        # Python dependencies
└── render.yaml             # Render deployment configuration
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Flo1632/MyMatrix.git
   cd MyMatrix
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Or directly via .EXE

1. Download the .exe.
2. Choose: Trusted File
3. After downloading open the file like any Windows application with a double click

### Run the Desktop App

```bash
python main_matrix_desktop.py
```

### Run the Web App Locally

```bash
python main_matrix_webapp.py
```

Then open your browser at `http://localhost:8080`.

---

## How to Use

1. **Enter a task** in the text field at the top.
2. **Select a category** from the dropdown menu (Important & Urgent, Not Important but Urgent, etc.).
3. Click **Submit** to add the task to the corresponding quadrant.
4. **Click on a quadrant** to open a detail view of all tasks in that category.
5. **Check the checkbox** next to a task to mark it as done.
6. Select the category in the dropdown and click **Remove Task** to delete all checked tasks in that category.
7. Click the **Info** button to read a description of each quadrant's strategy.

---

## Deployment

The web app is configured for deployment on [Render](https://render.com/) via `render.yaml`:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `python main_matrix_webapp.py`
- **Port:** `8080`

---

## License

This project is open source. Feel free to use, modify, and distribute it.
