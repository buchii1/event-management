# Overview

EventsPro is a comprehensive event scheduling and booking system developed using Django, a Python Web Development Framework, and SQL. The platform caters to event organizers, enabling them to list their events efficiently, while providing regular users with the ability to browse and book events seamlessly. Key features include user authentication, event creation and management, event booking, ticket generation, and calendar integration for added convenience. 

This project serves as a learning experience for me as an aspiring software engineer, helping me further my understanding of web development concepts and frameworks.

## Features
- **User Authentication**: Secure registration and login functionality for users and administrators.
- **User Profile**: Personalized user profiles displaying booking history and event preferences.
- **Event Management**: Add, update, delete, and retrieve events with ease.
- **Organizer Management**: Administrative control to add and retrieve event organizers.
- **Event Booking**: Streamlined booking process for users, ensuring a hassle-free experience.
- **Ticket Generation**: Downloadable event tickets with unique booking IDs for enhanced security.
- **Calendar Integration**: Ability to add booked events to calendar applications for efficient planning.

You can watch a demonstration of the software running and a walkthrough of the code in this 
[Software Demo Video.](https://youtu.be/Lya2RwyY7SE)

# Web Pages
- **Sign Up Page**: Allows new users to register on the platform.
- **Log In Page**: Enables existing users to log in to their accounts securely.
- **Add Events Page**: Exclusive access for administrators to create new events.
- **Edit Events Page**: Exclusive access for administrators to edit events.
- **Events Page**: Displays a comprehensive list of all available events to users.
- **Event Detail Page**: Provides detailed information about a selected event, including description, location, date, and time.
- **Booking Page**: Facilitates event booking for logged-in users, redirecting guests to the login page if necessary.
- **Add Organizers Page**: Administrative interface to add and manage event organizers.
- **Profile Page**:
    - Displays user information and preferences.
    - Lists all events booked by the user.
    - Allows users to download event tickets and add event details to their calendar apps for easy access.

# Development Environment
To set up and run the project successfully, follow these installation steps:

1. Download and extract the project files to your local machine.
2. Install Python 3.x and ensure that both `python` and `pip` are added to your system's environmental variables.
3. (Optional) Set up a virtual environment for the project:
    - Navigate to the project directory in your terminal.
    - Create a virtual environment using `python -m venv venv`.
    - Activate the virtual environment:
        - On Windows: `venv\Scripts\activate`
        - On Unix-based systems (MacOS / Linux): `source venv/bin/activate`
4. Install project dependencies using `pip install -r requirements.txt`.
5. Apply database migrations with `python manage.py migrate`.
6. Start the development server by running `python manage.py runserver`.
7. Access the application in your web browser at `http://localhost:8000`.

# Useful Websites
Here are some helpful resources that aided in the development process:
* [Html2Canvas Documentation](https://html2canvas.hertzen.com/documentation) - Documentation for Html2Canvas library, used for generating event tickets.
* [Django Documentation](https://docs.djangoproject.com/en/5.0/) - Official documentation for the Django web framework, offering comprehensive guides and references.

# Future Work
To further enhance the application and address additional requirements, consider the following improvements and additions:
* Develop a custom dashboard for event organizers to streamline event creation and management processes.
* Implement functionality for users to delete booked events and update their profile information.
* Integrate a payment gateway to facilitate secure online transactions for event bookings.