# 💰 Budget Tracker Web Application

A modern, responsive budget tracking web application built with Flask and Bootstrap 5. This application helps users manage their finances with a beautiful glassmorphic UI and intuitive features.

![Budget Tracker Screenshot](static/images/screenshot.png)

## ✨ Features

- **Expense Tracking**: Add and categorize your income and expenses
- **Visual Analytics**: Interactive pie chart showing expense distribution
- **Monthly Overview**: Track your income, expenses, and savings
- **Budget Limits**: Set spending limits for different categories
- **Transaction History**: View and search through your transaction history
- **Data Export**: Export your transaction data to CSV
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Beautiful glassmorphic design with dark theme

## 🛠️ Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Data Storage**: CSV (no database required)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/budget-tracker.git
cd budget-tracker
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## 📝 Usage

1. **Adding Transactions**

   - Enter the amount
   - Select a category
   - Choose transaction type (Income/Expense)
   - Click "Add Entry"

2. **Setting Budget Limits**

   - Select a category
   - Enter the limit amount
   - Click "Save Limit"

3. **Viewing Analytics**

   - The pie chart automatically updates to show expense distribution
   - Monthly overview shows total income, expenses, and savings

4. **Managing Transactions**
   - Search through transaction history
   - Delete individual transactions
   - Export data to CSV

## 🎨 UI Features

- **Glassmorphic Design**: Modern, translucent UI elements
- **Dark Theme**: Easy on the eyes
- **Responsive Layout**: Adapts to all screen sizes
- **Interactive Charts**: Visual representation of spending patterns
- **Animated Statistics**: Smooth animations for better user experience

## 🔒 Data Management

- All data is stored locally in CSV format
- No database required
- Easy to backup and restore
- Export functionality for data portability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Bootstrap 5 for the UI framework
- Chart.js for the interactive charts
- Font Awesome for the icons
- Flask for the backend framework
