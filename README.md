# 🚗 Vehicle Service Web App

A Django-based web application that allows users to register, book vehicle services, describe vehicle issues, and reset their password via email OTP. Users can also browse service menus before booking. Admins can manage bookings and update service statuses.

---

## 🌟 Key Features

- 🔐 **User Authentication**
  - Sign up, log in, and log out securely
  - Forgot password with OTP-based email reset

- 🛠️ **Service Booking**
  - Book vehicle service appointments
  - Add description of vehicle problems
  - View booking history and current status

- 📋 **Service Menu**
  - Browse available service categories and pricing before booking

- 🧑‍💻 **Admin Panel**
  - View and manage all user bookings
  - Update service status

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML and CSS.
- **Database:** SQLite (default, can be upgraded)
- **Email Service:** SMTP (for OTP-based password reset)

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/vehicle_service.git
cd vehicle_service
python manage.py migrate
python manage.py runserver
