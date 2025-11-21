async function updateHunger() {
    const response = await fetch('/hunger');
    const data = await response.json();
    document.getElementById('hunger').textContent = data.hunger;
}

async function feed() {
    const response = await fetch("/hunger", {
    method: "POST"
    });

    const data = await response.json();
    console.log(data.message);

    // updates hunger right away aftewards
    updateHunger();
}

// updates the happiness count on frontend
async function updateHappiness(){
    const response = await fetch('/happiness');
    const data = await response.json();
    document.getElementById("happiness").textContent = data.happiness;
}

async function play(){
    const response = await fetch("/happiness", {
    method: "POST"
    });
    const data = await response.json();
    console.log(data.message);
    updateHappiness();
}

async function updateSleep(){
    const response = await fetch('/sleepiness');
    const data = await response.json();
    document.getElementById("sleepiness").textContent = data.sleepiness;
}

async function sleep(){
    const response = await fetch('/sleepiness', {
    method: "PUT"
    });
    const data = await response.json();
    console.log(data.message);
    updateSleep();
}

// Fetch hunger every second
setInterval(updateHunger, 1000);
setInterval(updateHappiness, 1000);
setInterval(updateSleep, 1000);