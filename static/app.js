// Converts Unix timestamp values into HH:MM:SS format+++++++++++++++
function convertUnix(timestamp){
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
    let formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

    return formattedTime;
}


// collects data using dataset attribute and pass that data in chart API++++++++++++++++++++++++++
// const nameData = document.querySelector('.chartData-name').dataset.name;
// const symbolData = document.querySelector('.chartData-symbol').dataset.symbol;
// const regionData = document.querySelector('.chartData-region').dataset.region;
// const priceData = document.querySelector('.chartData-price').dataset.price;
// let intervalFinal;
// let rangeFinal;

const nameDataUser = document.querySelector('.chartData-name-user').dataset.name;
const symbolDataUser = document.querySelector('.chartData-symbol-user').dataset.symbol;
const regionDataUser = document.querySelector('.chartData-region-user').dataset.region;
const priceDataUser = document.querySelector('.chartData-price-user').dataset.price;
let intervalFinalUser;
let rangeFinalUser;


// document.getElementById('chart-form').addEventListener('submit', chartTime);
document.getElementById('chart-form-user').addEventListener('submit', chartTimeUser);

// async function chartTime(e){
//     e.preventDefault();
//     const interval = document.getElementById('interval').value;
//     const range = document.getElementById('range').value;
//     intervalFinal = interval;
//     rangeFinal = range;
//     const inputData = {
//         method: 'GET',
//         url: 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts',
//         params: {
//           symbol: symbolData,
//           interval: intervalFinal,
//           range: rangeFinal,
//           region: regionData
//         },
//         headers: {
//           'x-rapidapi-key': '1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654',
//           'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
//         }
//     };
//     const chartData =await axios.request(inputData).then(function (response) {
//         return {"closedPrice" : response.data.chart.result[0].indicators.quote[0].close,
//             "timeStamop": response.data.chart.result[0].timestamp}
//         }).catch(function (error) {
//             console.error(error);
//         });

//     const yFormatted = chartData.timeStamop.map(t =>
//         {return convertUnix(t)});
//     showChart(chartData.closedPrice, yFormatted);  
// }

// function showChart(xdata, ydata){
//     let element = document.getElementById('myChart');
//     if (element){
//         element.remove();
//     }
//     const chartDiv = document.getElementById('chart');
//     const canvas = document.createElement('canvas');
//     canvas.setAttribute('id','myChart');
//     canvas.className = "chart-sizing"
//     chartDiv.appendChild(canvas);
//     const ctx = document.getElementById('myChart').getContext('2d');
//     const myChart = new Chart(ctx, {
//       type: 'line',
//       data: {
//           labels: ydata,
//           datasets: [{
//               label: 'Stock/Crypto Chart',
//               data: xdata,
//               backgroundColor: [
//                   'rgba(255, 99, 132, 0.2)'
//               ],
//               borderColor: [
//                   'rgba(255, 99, 132, 1)'
//               ],
//               borderWidth: 1
//           }]
//       },
//       options: {
//           scales: {
//               y: {
//                   beginAtZero: false
//               }
//           }
//       }
//   });
// }

// Users stock/crypto chart+++++++++++++++++
async function chartTimeUser(e){
    e.preventDefault();
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

    const yFormatted = chartData.timeStamop.map(t =>
        {return convertUnix(t)});
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
                  'rgba(255, 99, 132, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)'
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



const marketData = {};
let follow = false;

document.getElementById('follow-form').addEventListener('submit', followFunc);
// Form search function++++++
function followFunc(e){
    e.preventDefault();
    follow = !follow;
    marketData["id"] = document.getElementById('hidden-id').value;
    marketData["type"] = document.getElementById('hidden-type').value;
    marketData["name"] = document.getElementById('hidden-name').value;
    marketData["region"] = document.getElementById('hidden-region').value;
    marketData["price"] = document.getElementById('hidden-price').value;
    const btn = document.getElementById('follow-btn');
    if (follow){
        btn.innerHTML = "<span>Following</span>";
        btn.className = "btn btn-primary btn-lg mt-3 py-2";
        btn.classList.toggle("unfollow");
        axios.post("/users/profile/add", {marketData}).then(res => {
            console.log(res)});
    }else {
        btn.innerHTML = "<span>Follow</span>";
        btn.className = "btn btn-primary btn-lg mt-3 py-2";
        btn.classList.toggle("follow-cls");
        
        axios.delete("/users/profile/delete", {data: marketData}).then(res =>{
            console.log(res);
        });
    }
}