# FlowForge Frontend

This is the frontend component of FlowForge, built with HTML, CSS, and vanilla JavaScript.

## Features
- Workflow builder interface for describing workflows in plain English
- Real-time parsing and visualization of workflow structure via backend API
- Responsive design for mobile and desktop
- Integrated with Django backend API for workflow parsing

## Project Structure
```
src/
├── index.html      # Main HTML file
├── css/
│   └── styles.css  # Styling for the application
���└── js/
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

3. **Start the development server**:
   - Install `serve` if you don't have it: `npm install -g serve`
   - Run: `serve src`
   - Then open your browser to `http://localhost:3000` (or the port shown in the terminal).

   Alternatively, you can simply open `src/index.html` directly in your browser.

## API Integration
The frontend communicates with the FlowForge backend API to parse natural language requests into structured workflows.

To enable API integration:

1. Ensure the backend is running (see backend branch instructions)
2. The frontend is pre-configured to call `http://localhost:8000/api/parse/` for parsing
3. If your backend runs on a different host/port, edit the `BACKEND_URL` constant in `src/js/app.js`

## Folder Explanation
- `src/index.html`: The main entry point of the application
- `src/css/styles.css`: Contains all styling for the application
- `src/js/app.js`: Contains the interactive logic for the workflow builder, including API calls to the backend

## Customization
- Modify the styles in `src/css/styles.css` to change the look and feel
- Update the workflow parsing logic in `src/js/app.js` to change the API endpoint or handle different responses
- Add more components as needed in separate JavaScript files

## Browser Support
This frontend works in all modern browsers (Chrome, Firefox, Safari, Edge).

## License
This project is part of FlowForge and is licensed under the MIT License.
