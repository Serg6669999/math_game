function get_chart(chart_data) {

    console.log("chart_data", chart_data)
    const data = {
        labels: chart_data.map(row => "lvl-" + row.level + ", MA-" + row.math_action),
        datasets: [
            {
                label: "Arithmetic",
                data: chart_data.map(row => {
                if (row.game_name === "Arithmetic") {return row.time;}
                            }),
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2
            },
            {
                label: "Memory+Arithmetic",
                data: chart_data.map(row => {
                if (row.game_name === "Memory+Arithmetic") {return row.time;}
                            }),
                fill: false,
                borderColor: 'rgba(192, 75, 192, 1)',
                borderWidth: 2
            },
            {
                label: "Memory",
                data: chart_data.map(row => {
                if (row.game_name === "Memory") {return row.time;}
                            }),
                fill: false,
                borderColor: 'rgba(238,233,35,0.98)',
                borderWidth: 2
            },
            {
                label: "Words",
                data: chart_data.map(row => {
                if (row.game_name === "Words") {return row.time;}
                            }),
                fill: false,
                borderColor: 'rgb(75,87,192)',
                borderWidth: 2
            },
        ]
    };

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Дата'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Время, с'
                    }
                }
            }
        }
    });

}
function httpGet(path, body)
{

    let url = window.location.origin + "/"

    const options = {
        headers: {"Content-Type":"application/json"},
        method: "POST",
        body: JSON.stringify( body )
        };
    let responseData
    return fetch( url + path, options )
        .then( (response) => response.json())

        ;
}
httpGet("stats_data", "").then(data => {get_chart(data)})
