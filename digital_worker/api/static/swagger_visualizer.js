// Swagger UI Response Visualizer
(function() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                const jsonBlocks = document.querySelectorAll('.microlight');
                jsonBlocks.forEach(block => {
                    if (block.innerText.includes('"thread_id"') && !block.parentElement.querySelector('.visualize-btn')) {
                        addVisualizeButton(block);
                    }
                });
            }
        });
    });

    function addVisualizeButton(block) {
        const btn = document.createElement('button');
        btn.innerText = '✨ Visualize State';
        btn.className = 'visualize-btn';
        btn.style = `
            background: #4f46e5;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            cursor: pointer;
            margin-bottom: 8px;
            font-weight: 600;
        `;
        
        btn.onclick = () => {
             try {
                 const data = JSON.parse(block.innerText);
                 alert(`Workflow: ${data.intent || 'Unknown'}\nStatus: ${data.validation_score ? (data.validation_score * 100).toFixed(0) + '%' : 'Processing'}\nSteps: ${data.audit_trail ? data.audit_trail.length : 0}`);
             } catch(e) { console.error("Parse fail", e); }
        };

        block.parentElement.insertBefore(btn, block);
    }

    observer.observe(document.body, { childList: true, subtree: true });
})();
