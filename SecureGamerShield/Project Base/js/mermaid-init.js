if (window.mermaid) {
    mermaid.initialize({
        startOnLoad: true,
        theme: 'neutral',
        securityLevel: 'loose',
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true
        }
    });
} else {
    console.error("Mermaid library not loaded!");
}