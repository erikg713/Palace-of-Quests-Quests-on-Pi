Frontend README (React)

Overview

The frontend for PiQuest is a React application designed to be mobile-friendly and optimized for performance. It integrates with the Pi Network, has 3D components, and features a responsive layout for a seamless experience across devices.

Installation

1. Clone the Repository:

git clone https://github.com/username/piquest-frontend.git
cd piquest-frontend


2. Install Dependencies:

npm install


3. Run the Development Server:

npm start


4. Build for Production:

npm run build



Project Structure

piquest-frontend/
├── public/
│   ├── index.html        # Main HTML file
│   ├── manifest.json     # PWA manifest for Pi Network compatibility
│   └── icons/            # Icons for mobile devices and PWA
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── MobileNav.js      # Bottom navigation for mobile
│   │   └── ThreeDScene.js    # 3D scene component using Three.js
│   ├── pages/            # Pages for routing
│   │   ├── Home.js           # Home screen of the app
│   │   ├── Marketplace.js    # In-game marketplace page
│   │   └── Profile.js        # User profile page
│   ├── styles/           # Global and component-specific CSS
│   │   ├── global.css        # Global styling, including responsive layout
│   │   └── MobileNav.css     # Styles for MobileNav component
│   ├── App.js            # Root component with routing
│   ├── index.js          # Entry point, renders App component
│   └── setupProxy.js      # Proxy setup for backend API requests
├── .env                  # Environment variables
└── README.md

Explanation of Key Files

App.js: The main application component, sets up routing to different pages.

components/ThreeDScene.js: Contains 3D rendering with Three.js, optimized for mobile.

pages/Marketplace.js: The marketplace page where users can browse and purchase items.

setupProxy.js: Configures proxying of API requests to avoid CORS issues.

global.css: Contains global styles for responsive and mobile-friendly layout.
