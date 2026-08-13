// Simple JavaScript for the workflow builder
document.addEventListener('DOMContentLoaded', function() {
    const nlRequest = document.getElementById('nl-request');
    const parseBtn = document.getElementById('parse-btn');
    const previewContent = document.getElementById('preview-content');
    
    parseBtn.addEventListener('click', function() {
        const requestText = nlRequest.value.trim();
        
        if (requestText === '') {
            previewContent.innerHTML = '<p style="color: #e74c3c;">Please enter a workflow description</p>';
            return;
        }
        
        // Show a loading state
        previewContent.innerHTML = '<p>Parsing your request...</p>';
        
        // Simulate parsing delay
        setTimeout(() => {
            // In a real app, this would call the backend API
            // For now, we'll show a mock structured workflow
            const mockWorkflow = {
                trigger: "Schedule",
                source: "College ERP",
                condition: "Daily at 8:00 AM",
                action: "Email summary",
                details: "Fetch attendance data from college ERP system and send email summary"
            };
            
            // Display the workflow as a formatted JSON
            previewContent.innerHTML = `
                <h3>Generated Workflow:</h3>
                <pre>${JSON.stringify(mockWorkflow, null, 2)}</pre>
            `;
        }, 1000);
    });
    
    // Also parse on Enter key in textarea
    nlRequest.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            parseBtn.click();
        }
    });
});
