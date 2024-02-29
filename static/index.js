let zoomFactor = 1.0;
const minZoom = 0.5;
const maxZoom = 2.0;
const zoomStep = 0.1; // Adjust this value to control zoom responsiveness

let isDragging = false;
let prevX = 0;
let prevY = 0;

function refreshFeed(index) {
    
    const button = document.getElementById(`refresh-button-${index}`);
    const icon = document.getElementById(`refresh-icon-${index}`);

    
    button.disabled = true;
    icon.classList.add('refreshing'); 

    
    fetch(`/refresh_feed/${index}`, {method: 'POST'})
        .then(response => {
            if (!response.ok) {
                
                console.error('Refresh operation failed');
            }
            
            const img = document.getElementById(`bg${index}`);
            const src = img.src;
            img.src = '';  // Clear the src
            img.src = src;  // Set the src again to force the browser to reload the image
        })
        .catch(error => {
            // If there was an error sending the request, print an error message
            console.error('Error sending refresh request:', error);
        })
        .finally(() => {
            // Enable the button again and restore its original text and style
            button.disabled = false;
            icon.classList.remove('refreshing'); // Remove rotating animation class
        });
}

function populateResolutionDropdowns() {
    const validResolutions = ['480', '600', '720', '768', '960']; // Your list of valid resolutions

    document.querySelectorAll('.video-feed').forEach(item => {
        const cameraIndex = item.id.split('bg')[1]; // Extract camera index
        const resolutionDropdown = document.getElementById(`resolution-dropdown-${cameraIndex}`);

        validResolutions.forEach(resolution => {
            const option = document.createElement('option');
            option.value = resolution;
            option.textContent = `${resolution}p`;
            resolutionDropdown.appendChild(option);
        });
    });
}

// Execute when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', populateResolutionDropdowns);  

document.querySelectorAll('.video-feed').forEach(item => {
    item.addEventListener('wheel', event => {
        event.preventDefault();
        const delta = Math.sign(event.deltaY);
        if (delta > 0) {
            zoomOut(item);
        } else {
            zoomIn(item, event);
        }
    });

    item.addEventListener('mousemove', event => {
        if (isDragging) {
            const dx = event.clientX - prevX;
            const dy = event.clientY - prevY;
            prevX = event.clientX;
            prevY = event.clientY;

            const container = item.parentElement;
            const rect = container.getBoundingClientRect();
            const maxX = rect.width - item.width * zoomFactor;
            const maxY = rect.height - item.height * zoomFactor;

            let newX = item.offsetLeft + dx;
            let newY = item.offsetTop + dy;

            newX = Math.min(Math.max(newX, 0), maxX);
            newY = Math.min(Math.max(newY, 0), maxY);

            item.style.left = `${newX}px`;
            item.style.top = `${newY}px`;
        }
    });
    
    item.addEventListener('mouseup', () => {
        isDragging = false;
        item.style.cursor = 'move';
    });

    item.addEventListener('mouseleave', () => {
        isDragging = false;
        item.style.cursor = 'crosshair';
    });
});

function zoomIn(element, event) {
    zoomFactor += zoomStep;
    if (zoomFactor > maxZoom) {
        zoomFactor = maxZoom;
    }
    applyZoom(element, event);
}

function zoomOut(element) {
    if (zoomFactor > 1.0) { // Check if current zoom level is greater than default
        zoomFactor -= zoomStep;
        if (zoomFactor < minZoom) {
            zoomFactor = minZoom;
        }
        applyZoom(element);
    }
}

function applyZoom(element, event) {
    const containerRect = element.parentElement.getBoundingClientRect();
    const mouseX = event ? event.clientX - containerRect.left : containerRect.width / 2;
    const mouseY = event ? event.clientY - containerRect.top : containerRect.height / 2;

    const offsetX = (mouseX - containerRect.width / 2) * (zoomFactor - 1);
    const offsetY = (mouseY - containerRect.height / 2) * (zoomFactor - 1);

    element.style.transformOrigin = `${offsetX}px ${offsetY}px`;
    element.style.transform = `scale(${zoomFactor})`;
}

document.addEventListener('mousedown', function(event) {
    if (event.button === 1) {
        event.preventDefault();
    }
});

function toggleFeed(index) {
    const button = document.getElementById(`power-button-${index}`);
    const isActive = button.classList.contains('btn-danger');

    fetch(`/turn_off_feed/${index}`, { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                console.error('Failed to turn off the feed');
            }
        })
        .catch(error => {
            console.error('Error turning off feed:', error);
        });
}

function changeResolution(cameraIndex) {
    var resolution = document.getElementById(`resolution-dropdown-${cameraIndex}`).value;

    fetch(`/change_resolution?camera=${cameraIndex}&resolution=${resolution}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            console.error('Failed to change resolution:', response.statusText);
        } else {
            console.log('Resolution changed successfully');
        }
    })
    .catch(error => {
        console.error('Error changing resolution:', error);
    });
}

