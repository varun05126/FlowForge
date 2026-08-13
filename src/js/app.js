// JavaScript for the workflow builder
document.addEventListener('DOMContentLoaded', function() {
    const nlRequest = document.getElementById('nl-request');
    const parseBtn = document.getElementById('parse-btn');
    const previewContent = document.getElementById('preview-content');
    
    // Backend URL - change this if your backend is running on a different host/port
    const BACKEND_URL = 'http://localhost:8000';
    
    parseBtn.addEventListener('click', async function() {
        const requestText = nlRequest.value.trim();
        
        if (requestText === '') {
            previewContent.innerHTML = '<p style="color: #e74c3c;">Please enter a workflow description</p>';
            return;
        }
        
        // Show a loading state
        previewContent.innerHTML = '<p>Parsing your request...</p>';
        
        try {
            // Call the backend API to parse the natural language request
            const response = await fetch(`${BACKEND_URL}/api/parse/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: requestText })
            });
            
            if (!response.ok) {
                throw new Error(`Backend error: ${response.status}`);
            }
            
            const workflowData = await response.json();
            
            // Display the workflow as a formatted JSON
            previewContent.innerHTML = `
                <h3>Generated Workflow:</h3>
                <pre>${JSON.stringify(workflowData, null, 2)}</pre>
            `;
        } catch (error) {
            console.error('Error:', error);
            previewContent.innerHTML = `
                <p style="color: #e74c3c;">Error parsing request: ${error.message}</p>
                <p>Make sure the backend is running on ${BACKEND_URL}</p>
                <p>Showing mock data instead:</p>
                <h3>Mock Workflow:</h3>
                <pre>${JSON.stringify({
                    trigger: "Schedule",
                    source: "College ERP",
                    condition: "Daily at 8:00 AM",
                    action: "Email summary",
                    details: "Fetch attendance data from college ERP system and send email summary"
                }, null, 2)}</pre>
            `;
        }
    });
    
    // Also parse on Enter key in textarea
    nlRequest.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            parseBtn.click();
        }
    });
});
