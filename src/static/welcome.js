// boot.js
const feedList = document.getElementById('feed-list');
let selectedFeeds = [];

// Fetch available feeds from the server
fetch('/get_available_feeds')
    .then(response => response.json())
    .then(feeds => {
        feeds.forEach(feed => {
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `feed-${feed.index}`; 
            checkbox.value = feed.index;

            const label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = `Feed ${feed.index}`;

            const listItem = document.createElement('div');
            listItem.appendChild(checkbox);
            listItem.appendChild(label);

            feedList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching feeds:', error));

function confirmFeeds() {
    selectedFeeds = []; 
    const checkboxes = document.querySelectorAll('#feed-list input[type="checkbox"]:checked');

    checkboxes.forEach(checkbox => {
        selectedFeeds.push(parseInt(checkbox.value)); 
    });

    fetch('/select_feeds', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(selectedFeeds)
})
.then(response => {
    if (!response.ok) {
        console.error('Error selecting feeds:', response.statusText);
    } else {
        // Handle successful response, even if empty
        console.log("Server selection update successful!");
        showMainPage();
    }
})
.catch(error => console.error('Error sending feed selection:', error));
}