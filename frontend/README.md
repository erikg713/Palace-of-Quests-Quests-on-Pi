Palace of Quests Frontend

This is the frontend codebase for Palace of Quests, a Web3-based application that integrates the Pi Network SDK for secure payments and user authentication.


---

Features

React Framework: Modern UI built with React.

Pi Network Integration: Supports user authentication and payments through the Pi Network SDK.

Responsive Design: Optimized for various devices.

REST API Communication: Connects with the backend via secure API endpoints.

Environment-Specific Configurations: Environment variables for managing different setups (development, staging, production).



---

Prerequisites

Before setting up the frontend, ensure the following are installed:

Node.js: v16+ recommended.

npm or yarn: Package managers for dependency installation.

A valid Pi Network App ID and API Key registered on the Pi Developer Portal.



---

Installation

1. Clone the Repository:

git clone https://github.com/your-repo/palace-of-quests-frontend.git
cd palace-of-quests-frontend


2. Install Dependencies: Run the following command to install all necessary packages:

npm install


3. Set Up Environment Variables: Create a .env file in the root of your project and include the necessary keys:

REACT_APP_API_BASE_URL=<your-backend-url>
REACT_APP_PI_APP_ID=<your-pi-app-id>
REACT_APP_PI_ENV=development

Replace <your-backend-url> and <your-pi-app-id> with actual values.




---

Development

1. Start the Development Server:

npm start

By default, the app runs at http://localhost:3000.


2. Pi Network Integration: Ensure your Pi Network App is registered and linked to the correct domain via the Pi Developer Portal.




---

Production Build

To create a production-ready build:

npm run build

The build files will be located in the build/ directory, ready for deployment.


---

Directory Structure

palace-of-quests-frontend/
├── public/         # Static files (index.html, images, etc.)
├── src/            # Application source code
│   ├── components/ # Reusable UI components
│   ├── pages/      # Main application pages
│   ├── hooks/      # Custom React hooks
│   ├── services/   # API service calls
│   ├── utils/      # Utility functions
│   └── App.js      # Root application component
├── .env            # Environment variables
├── package.json    # Project dependencies
└── README.md       # Project documentation


---

Dependencies

Key dependencies for the frontend include:

React - UI framework.

Axios - HTTP client for API requests.

React Router - Routing library for navigation.

Pi Network SDK - Payment and authentication SDK.



---

Deployment

To deploy the frontend:

1. Create a production build:

npm run build


2. Deploy the build/ directory to your hosting platform (e.g., Netlify, Vercel, AWS S3).




---

Contributing

Contributions are welcome! Please follow the steps below:

1. Fork the repository.


2. Create a feature branch:

git checkout -b feature/your-feature


3. Commit your changes and push the branch.


4. Open a pull request.




---

License

This project is licensed under the MIT License.


---

Feel free to modify this template further to suit your project's specifics! Let me know if you'd like to add more details.

