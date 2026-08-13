# FlowForge Frontend

This is the frontend component of FlowForge, built with HTML, CSS, and vanilla JavaScript.

## Features
- Workflow builder interface for describing workflows in plain English
- Real-time parsing and visualization of workflow structure
- Responsive design for mobile and desktop
- Placeholder for API integration with the backend

## Project Structure
```
src/
├── index.html      # Main HTML file
├── css/
│   └── styles.css  # Styling for the application
�└── js/
    └── app.js      # Application logic
```

## Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/varun05126/FlowForge.git
   ```

2. **Checkout the frontend branch**:
   ```bash
   git checkout frontend
   ```

3. **Install dependencies**: 
   *This frontend uses only HTML/CSS/JS, so no npm dependencies are required.*
   However, if you wish to use a development server, you can install a simple one like `serve`:
   ```bash
   npm install -g serve
   ```

4. **Start the development server**:
   ```bash
   serve src
   ```
   Then open your browser to `http://localhost:3000` (or the port shown in the terminal).

   Alternatively, you can simply open `src/index.html` directly in your browser.

## API Integration
The frontend is designed to communicate with the FlowForge backend API. 
To enable API integration:

1. Ensure the backend is running (see backend branch instructions)
2. Update the `src/js/app.js` file to make actual API calls to the backend endpoints
3. The placeholder API client would typically be in `src/api/client.js` (to be implemented)

## Folder Explanation
- `src/index.html`: The main entry point of the application
- `src/css/styles.css`: Contains all styling for the application
- `src/js/app.js`: Contains the interactive logic for the workflow builder

## Customization
- Modify the styles in `src/css/styles.css` to change the look and feel
- Update the workflow parsing logic in `src/js/app.js` to connect to the actual backend
- Add more components as needed in separate JavaScript files

## Browser Support
This frontend works in all modern browsers (Chrome, Firefox, Safari, Edge).

## License
This project is part of FlowForge and is licensed under the MIT License.
