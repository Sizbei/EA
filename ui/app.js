/**
 * Composio EA Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const aiInput = document.getElementById('ai-command');
    const sendBtn = document.getElementById('send-command');
    const terminalBody = document.getElementById('terminal-output');
    const syncBtn = document.getElementById('sync-btn');
    const navItems = document.querySelectorAll('.nav-links li');
    const pageTitle = document.getElementById('page-title');

    // Navigation logic
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const page = item.getAttribute('data-page');
            pageTitle.innerText = page.charAt(0).toUpperCase() + page.slice(1) + ' Center';
            
            logToTerminal(`[NAV] Switched to ${page} view.`);
        });
    });

    // Simple terminal logger
    function logToTerminal(message, type = '') {
        const p = document.createElement('p');
        p.className = 'log' + (type ? ' ' + type : '');
        const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        p.innerText = `[${time}] ${message}`;
        terminalBody.appendChild(p);
        terminalBody.scrollTop = terminalBody.scrollHeight;
    }

    // AI Command handling
    function handleCommand() {
        const cmd = aiInput.value.trim();
        if (!cmd) return;

        logToTerminal(`> ${cmd}`, 'user-msg');
        aiInput.value = '';
        
        // Simulate AI Thinking
        setTimeout(() => {
            if (cmd.toLowerCase().includes('flight')) {
                logToTerminal('Searching for flight updates...', 'info');
                setTimeout(() => {
                    logToTerminal('Success: DL123 is currently on schedule. Departure terminal verified.', 'green');
                }, 1000);
            } else if (cmd.toLowerCase().includes('expense') || cmd.toLowerCase().includes('buy')) {
                logToTerminal('Analyzing spending patterns...', 'info');
                setTimeout(() => {
                    logToTerminal('Projected monthly total: $5,120. Alert: Travel category is 15% above budget.', 'warning');
                }, 1200);
            } else {
                logToTerminal('Processing request via Composio Toolset...', 'info');
                setTimeout(() => {
                    logToTerminal('Action complete. Check your primary inbox for details.', 'green');
                }, 1500);
            }
        }, 500);
    }

    sendBtn.addEventListener('click', handleCommand);
    aiInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleCommand();
    });

    // Sync Button
    syncBtn.addEventListener('click', () => {
        syncBtn.disabled = true;
        const originalText = syncBtn.innerHTML;
        syncBtn.innerHTML = '<span>⏳</span> Syncing...';
        
        logToTerminal('Initiating global sync with Google Apps & Notion...', 'info');
        
        setTimeout(() => {
            logToTerminal('[SYNC] 14 new emails processed.', 'green');
            logToTerminal('[SYNC] Calendar events aligned.', 'green');
            logToTerminal('[SYNC] Notion database updated.', 'green');
            
            syncBtn.innerHTML = originalText;
            syncBtn.disabled = false;
        }, 2000);
    });

    // Initial greeting
    setTimeout(() => {
        logToTerminal('Ready for instructions. How can I assist you today?', 'green');
    }, 1000);
});
