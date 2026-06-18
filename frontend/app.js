console.log("app.js loaded");
const API_BASE = "https://b5899fk3l6.execute-api.us-east-1.amazonaws.com";

async function findRestaurant() {

const style = document.getElementById("style").value;
const vegetarian = document.getElementById("vegetarian").checked;
const delivery = document.getElementById("delivery").checked;

let url = `${API_BASE}/recommendation?`;

if (style) {
    url += `style=${style}&`;
}

url += `vegetarian=${vegetarian}&`;
url += `delivery=${delivery}`;

const resultDiv = document.getElementById("result");

try {

    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
        resultDiv.innerHTML =
            `<div class="result-card">
                <h3>No Restaurant Found</h3>
                <p>${data.message}</p>
            </div>`;
        return;
    }

    const restaurant = data.restaurantRecommendation;

    resultDiv.innerHTML =
        `<div class="result-card">
            <h2>${restaurant.name}</h2>
            <p><strong>Style:</strong> ${restaurant.style}</p>
            <p><strong>Address:</strong> ${restaurant.address}</p>
            <p><strong>Open:</strong> ${restaurant.openHour} - ${restaurant.closeHour}</p>
            <p><strong>Vegetarian:</strong> ${restaurant.vegetarian}</p>
            <p><strong>Delivery:</strong> ${restaurant.delivery}</p>
        </div>`;

} catch (err) {

    resultDiv.innerHTML =
        `<div class="result-card">
            <h3>Error</h3>
            <p>${err.message}</p>
        </div>`;
}

}
