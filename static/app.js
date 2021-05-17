// Converts Unix timestamp values into HH:MM:SS format+++++++++++++++
function convertUnix(range, timestamp){
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds.
    let date = new Date(timestamp * 1000);
    // Hours part from the timestamp
    let hours = date.getHours();
    // Minutes part from the timestamp
    let minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    let seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    if (range === "5d"){
        const data = date.toLocaleString("en-US", {weekday: "long"});
        return data;
    }
    if (range === "1mo" || range === "3mo" || range === "6mo" || range === "1y"){
        const data = date.toLocaleString("en-US", {day: "numeric"});
        const mon = date.toLocaleString("en-US", {month: "long"})
        return `${mon.slice(0,3)} ${data}`;
    }
    if (range === "2y" || range === "5y" || range ==="10y" || range === "max"){
        const mon = date.toLocaleString("en-US", {month: "long"})
        const data = date.toLocaleString("en-US", {year: "numeric"});
        return `${mon.slice(0,3)} ${data}`;
    }
    let formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

    return formattedTime;
}
function skipNums(arr){
    const final = [];
    for (let i = 0; i < arr.length; i++){
        if (final.includes(arr[i])){
            arr[i] = " ";
            final.push(arr[i]);
        }
        else{
            final.push(arr[i]);
        }
    }
    return final;
}

if(document.getElementById('chart-form-user')){
    document.getElementById('chart-form-user').addEventListener('submit', chartTimeUser);
}


// Users stock/crypto chart+++++++++++++++++
async function chartTimeUser(e){
    e.preventDefault();
    const symbolDataUser = document.querySelector('.chartData-symbol-user').dataset.symbol;
    const regionDataUser = document.querySelector('.chartData-region-user').dataset.region;
    let intervalFinalUser;
    let rangeFinalUser;

    const interval = document.getElementById('interval-user').value;
    const range = document.getElementById('range-user').value;
    intervalFinalUser = interval;
    rangeFinalUser = range;
    const inputData = {
        method: 'GET',
        url: 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts',
        params: {
          symbol: symbolDataUser,
          interval: intervalFinalUser,
          range: rangeFinalUser,
          region: regionDataUser
        },
        headers: {
          'x-rapidapi-key': '1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654',
          'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
        }
    };
    const chartData =await axios.request(inputData).then(function (response) {
        return {"closedPrice" : response.data.chart.result[0].indicators.quote[0].close,
            "timeStamop": response.data.chart.result[0].timestamp}
        }).catch(function (error) {
            console.error(error);
        });

    let yFormatted = chartData.timeStamop.map(t =>
        {return convertUnix(inputData.params.range,t)});
    showChartUser(chartData.closedPrice, yFormatted);  
}

function showChartUser(xdata, ydata){
    let element = document.getElementById('myChartUser');
    if (element){
        element.remove();
    }
    const chartDiv = document.getElementById('chart-user');
    const canvas = document.createElement('canvas');
    canvas.setAttribute('id','myChartUser');
    chartDiv.appendChild(canvas);
    const ctx = document.getElementById('myChartUser').getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: ydata,
          datasets: [{
              label: 'Stock/Crypto Chart',
              data: xdata,
              backgroundColor: [
                  'rgba(54, 162, 235, 0.2)'
              ],
              borderColor: [
                  'rgba(54, 162, 235, 0.2))'
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: false
              }
          }
      }
  });
}


// Follow a stock pr crypto+++++++++++++++++
document.querySelector("#follow-me-form") && document.querySelector("#follow-me-form").addEventListener('submit', followFunc);; 
const marketData = {};
let follow = false;

function followFunc(e){
    e.preventDefault();
    follow = !follow;
    marketData["id"] = document.getElementById('hidden-id').value;
    marketData["type"] = document.getElementById('hidden-type').value;
    marketData["name"] = document.getElementById('hidden-name').value;
    marketData["region"] = document.getElementById('hidden-region').value;
    marketData["price"] = document.getElementById('hidden-price').value;
    const btn = document.getElementById('follow-me-btn');
    if (follow){
        btn.innerHTML = "<span>Following</span>";
        btn.className = "btn btn-primary btn-lg mt-3 py-2";
        btn.classList.toggle("unfollow");
        axios.post("/api/users/profile/add", {marketData}).then(res => {
            console.log(res)});
    }else {
        btn.innerHTML = "<span>Follow</span>";
        btn.className = "btn btn-primary btn-lg mt-3 py-2";
        btn.classList.toggle("follow-cls");
        
        axios.delete("/api/users/profile/delete", {data: marketData}).then(res =>{
            console.log(res);
        });
    }
}

// refresh button to update latest changes in stock or crypto+++++++++++++++
document.querySelector('#refresh-form') && document.querySelector('#refresh-form').addEventListener('submit', refreshStockFunc);
const updateData = {};

function refreshStockFunc(e){
    e.preventDefault();
    updateData["username"] = document.getElementById('refresh-username').value;
    updateData["id"] = document.getElementById('refresh-id').value;
    updateData["type"] = document.getElementById('refresh-type').value;
    updateData["name"] = document.getElementById('refresh-name').value;
    updateData["symbol"] = document.getElementById('refresh-symbol').value;
    updateData["region"] = document.getElementById('refresh-region').value;
    axios.patch("/api/stock-crypto/refresh", {updateData})
    .then(res=>{console.log(res)});
    setTimeout(()=>{location.reload()}, 2000);
}

// remove stock or crypto from user's watchlist+++++++++++++
function removebtns(){
    if (document.querySelectorAll(".remove-form")){
        const forms = document.querySelectorAll(".remove-form");
        for (let form of forms){
            form.addEventListener('submit', removeFunc);
        }
    }
}

removebtns();
function removeFunc(e){
    e.preventDefault();
    const removeData = {}
    removeData["id"] = e.target.children[0].value.split("-")[0]
    removeData["type"] = e.target.children[0].value.split("-")[1]
    axios.delete("/api/users/profile/delete", {data: removeData}).then(res=>{
        // console.log(res);
    e.target.parentElement.parentElement.remove();
    
    });
}