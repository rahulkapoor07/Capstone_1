// function convertUnix(timestamp){
//     // Create a new JavaScript Date object based on the timestamp
//     // multiplied by 1000 so that the argument is in milliseconds, not seconds.
//     let date = new Date(timestamp * 1000);
//     // Hours part from the timestamp
//     let hours = date.getHours();
//     // Minutes part from the timestamp
//     let minutes = "0" + date.getMinutes();
//     // Seconds part from the timestamp
//     let seconds = "0" + date.getSeconds();

//     // Will display time in 10:30:23 format
//     let formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

//     return formattedTime;
// }

// document.getElementById("search-form").addEventListener('submit', values);

// async function values(e){
//     e.preventDefault();
//     const options = {
//         method: 'GET',
//         url: 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts',
//         params: {
//           symbol: document.getElementById("symbol").value,
//           interval: '5m',
//           range: '1d',
//           region: document.getElementById("region").value
//         },
//         headers: {
//           'x-rapidapi-key': '1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654',
//           'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
//         }
//     };
//     const closedPrice = axios.request(options).then(function (response) {
//         return response.data.chart.result[0].indicators.quote[0].close
//       }).catch(function (error) {
//           console.error(error);
//       });
    
//     const timeStamop = axios.request(options).then(function (response) {
//         return response.data.chart.result[0].timestamp;
//       }).catch(function (error) {
//           console.error(error);
//       });

//     const xPrice = await closedPrice;
//     const yTimestamp = await timeStamop;
//     const yFormatted = yTimestamp.map(t =>
//           convertUnix(t));
//     console.log(yFormatted);
//     const ctx = document.getElementById('myChart').getContext('2d');
//     const myChart = new Chart(ctx, {
//       type: 'bar',
//       data: {
//           labels: yFormatted,
//           datasets: [{
//               label: '# of Votes',
//               data: xPrice,
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

// function postData(data){
//     axios.post("/api/stocks-crypto/post", {params: data}).then(res => {
//         const jsonData = res.config.data;
//         objData = JSON.parse(jsonData)
//         objFinalData = objData.params;
//         console.log(objFinalData.name, objFinalData.ticker.toUpperCase(), objFinalData.region.toUpperCase(), objFinalData.price)
//     })

// }


// document.getElementById("search-form").addEventListener("submit", searchForm);

// async function searchForm(e){
//     e.preventDefault();
//     const symbol = document.getElementById("symbol").value;
//     const region = document.getElementById("region").value;
//     const options = {
//         method: 'GET',
//         url: 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile',
//         params: {symbol: symbol, region: region},
//         headers: {
//           'x-rapidapi-key': '1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654',
//           'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
//         }
//     };
//     await axios.request(options).then(function (res) {
//     let quoteSource = res.data.price.quoteType;
//     if (quoteSource == "CRYPTOCURRENCY"){
//         const crypto_price = res.data.price.regularMarketPrice.raw;
//         const crypto_name = res.data.price.shortName;
//         postData({"type": "crypto", "name": crypto_name, "ticker": symbol, "price": crypto_price, "region":region})
//     } else if (quoteSource == "EQUITY"){
//         const marketOpenPrice = res.data.price.regularMarketPrice.raw;
//         const stock_name = res.data.price.shortName;
//         postData({"type": "equity", "name": stock_name, "ticker": symbol, "price": marketOpenPrice, "region":region})
//     }else{
//         console.log("not found", "not found", "not found");
//     }
//     }).catch(function (error) {
//     console.error(error);
//     });
// };

