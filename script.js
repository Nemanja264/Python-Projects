const INTERVAL_IN_SECONDS = 20
const TIME_INTERVAL = 1000*INTERVAL_IN_SECONDS

function drawPage(host)
{
    let searchCont = document.createElement('div');
    searchCont.className = 'search-container';
    host.appendChild(searchCont);

    const coinsCont = document.createElement('div');
    coinsCont.className = 'coinsList';
    host.appendChild(coinsCont);

    drawSearchCont(searchCont);
}

function drawSearchCont(searchCont)
{
    const searchBar = document.createElement('input');
    searchBar.type = 'text';
    searchBar.placeholder = 'Search';
    searchBar.className = 'searchBar';
    searchCont.appendChild(searchBar);

    const sortCont = document.createElement('div');
    sortCont.className = 'sort-container';
    searchCont.appendChild(sortCont);

    drawSortSelect(sortCont);
}

function drawSortSelect(sortCont)
{
    let sel = document.createElement('select');
    sel.className = 'sort-categories';
    sortCont.appendChild(sel);

    sel = document.createElement('select');
    sel.className = 'sort-order';
    sortCont.appendChild(sel);
}

function createWatcherInput(coin)
{
    const container = document.createElement('div');
    container.className = 'watcher-input-container';

    const price_input = document.createElement('input');
    price_input.className = 'price-input';
    price_input.type = "number";
    price_input.placeholder = "Enter price limit";

    const btn = document.createElement("button");
    btn.textContent = 'Notify me';
    btn.addEventListener('click', () => {
        startWatcher(price_input, coin.name.toLowerCase());
    });

    container.appendChild(price_input);
    container.appendChild(btn);

    return container;
}

function drawCoin(coinsContainer, coin)
{
    const coinCont = document.createElement('div');
    coinCont.classList.add('coin-container', coin.name.replace(/\s+/g, ""));

    const coinInfo = document.createElement('p');
    coinInfo.textContent = `${coin.name}: $${formatCoinPrice(coin.priceUsd)}`;
    coinCont.appendChild(coinInfo);
    
    const watcherInputCont = createWatcherInput(coin);

    coinCont.appendChild(watcherInputCont);
    coinsContainer.appendChild(coinCont);
}

function formatCoinPrice(coin_price)
{
    return coin_price >= 1 ? parseFloat(coin_price).toFixed(4) : parseFloat(coin_price).toFixed(8);
}

async function fetchPrices()
{
    try
    {
       const response = await fetch('/api/prices');

       if(!response.ok)
           throw new Error("Network response was not ok");

       const coinsData = await response.json();

       if(Array.isArray(coinsData) && coinsData.length != 0)
       {
            console.log("Fetched data: ", coinsData);

            const coinsContainer = document.querySelector('.coinsList');
            coinsContainer.innerHTML='';

            coinsData.forEach(coin => {
                drawCoin(coinsContainer ,coin)
            });
       } 
    }
    catch(error)
    {
        console.error("Error fetching coin data:", error);
    }
}

function autoUpdate()
{
    setInterval(async() => {
        try {
            await fetchPrices();
        }
        catch(error)
        {
            console.error("Error in setInterval", error);
        }
    }, TIME_INTERVAL);
}

async function startWatcher(price_inputEl, coin_name)
{
    if(price_inputEl.value === "")
    {
        alert("Please enter a value");
        return;
    }

    const price_limit = price_inputEl.value;
    console.log(price_limit);
    try 
    {
        const response = await fetch(`/api/price_watcher/${coin_name}/${price_limit}`);

        if(!response.ok)
            throw new Error(`Server error: ${response.status}`);
        
        const result = await response.json();

        console.log(result);
    } 
    catch (error) {
        console.error("Fetch failed:", error);
    }
}

function initSocketListener()
{
    const socket = io();

    socket.on('connect', () => {
        console.log("Socket connected");
    });

    socket.on('limit_reached', data => {
        alert(`${data.coin.toUpperCase()} has reached your set limit: $${parseFloat(data.price).toFixed(4)}`)
    })
}

drawPage(document.body);

fetchPrices();
initSocketListener();
autoUpdate();

